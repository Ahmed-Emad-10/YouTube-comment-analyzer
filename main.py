from crewai.flow.flow import Flow, listen, router, start, and_
from pydantic import BaseModel

from scraper.youtube_scraper import get_comments
from nlp.topic_modeling import run_topic_modeling
from nlp.sentiment_analysis import run_sentiment_analysis

from crews.topic_labeling_crew import TopicLabelingCrew
from crews.insight_extractor_crew import InsightExtractorCrew
from crews.complaint_detector_crew import ComplaintDetectorCrew
from crews.report_writer_crew import ReportWriterCrew
from dotenv import load_dotenv
load_dotenv(".env")


# ── Flow State ────────────────────────────────────────────────────────────────

class CommentAnalysisState(BaseModel):
    video_url: str = ""
    topic_labels: str = ""
    insights: str = ""
    complaints: str = ""


# ── Flow ──────────────────────────────────────────────────────────────────────

class CommentAnalysisFlow(Flow[CommentAnalysisState]):

    # ── Stage 1: Scrape ───────────────────────────────────────────────────────

    @start()
    def scrape(self):
        print(f"\n[FLOW] Scraping comments from: {self.state.video_url}")
        comments = get_comments(self.state.video_url)
        print(f"[FLOW] Scraped {len(comments)} comments.")
        return comments

    # ── Stage 2a: Topic Modeling branch ───────────────────────────────────────

    @listen(scrape)
    def topic_modeling(self, comments):
        print("\n[FLOW] Running topic modeling...")
        df_topic = run_topic_modeling(comments)

        df_topic = df_topic[df_topic["Topic"] > -1].copy()

        keywords =[]
        count_comments=[]
        for _, row in df_topic.iterrows():
            print(row['Representation']), row['Count']
            keywords.append(str(row['Representation']))
            count_comments.append(row['Count'])

        
        print(f"[FLOW] Topic modeling done. {len(df_topic)} valid topics found.")
        return {"keywords": keywords, "count_comments": count_comments}

    @listen(topic_modeling)
    def run_topic_labeling_crew(self, topic_data):
        print("\n[FLOW] Running Topic Labeling Crew...")
        result = TopicLabelingCrew().crew().kickoff(
            inputs={"keywords_data": topic_data["keywords"], "comment_counts": topic_data["count_comments"]}
        )
        self.state.topic_labels = str(result)
        print("[FLOW] Topic Labeling Crew done.")

    # ── Stage 2b: Sentiment Analysis branch ───────────────────────────────────

    @listen(scrape)
    def sentiment_analysis(self, comments):
        print("\n[FLOW] Running sentiment analysis...")
        df_sent = run_sentiment_analysis(comments)

        positive_comments = "\n".join(
            df_sent[df_sent["label"] == "positive"]["text"].tolist()
        )
        negative_comments = "\n".join(
            df_sent[df_sent["label"] == "negative"]["text"].tolist()
        )

        print(
            f"[FLOW] Sentiment done. "
            f"Positive: {len(df_sent[df_sent['label'] == 'positive'])} | "
            f"Neutral: {len(df_sent[df_sent['label'] == 'neutral'])} | "
            f"Negative: {len(df_sent[df_sent['label'] == 'negative'])}"
        )
        return {"positive": positive_comments, "negative": negative_comments}

    @listen(sentiment_analysis)
    def run_insight_extractor_crew(self, sentiment_data):
        print("\n[FLOW] Running Insight Extractor Crew...")
        result = InsightExtractorCrew().crew().kickoff(
            inputs={"positive_comments": sentiment_data["positive"]}
        )
        self.state.insights = str(result)
        print("[FLOW] Insight Extractor Crew done.")

    @listen(sentiment_analysis)
    def run_complaint_detector_crew(self, sentiment_data):
        print("\n[FLOW] Running Complaint Detector Crew...")
        result = ComplaintDetectorCrew().crew().kickoff(
            inputs={"negative_comments": sentiment_data["negative"]}
        )
        self.state.complaints = str(result)
        print("[FLOW] Complaint Detector Crew done.")

    # ── Stage 3: Report Writer (waits for ALL 3 crews) ────────────────────────

    @listen(and_(run_topic_labeling_crew, run_insight_extractor_crew, run_complaint_detector_crew))
    def run_report_writer_crew(self):
        print("\n[FLOW] All 3 crews finished. Running Report Writer Crew...")
        result = ReportWriterCrew().crew().kickoff(
            inputs={
                "topic_labels":   self.state.topic_labels,
                "insights":       self.state.insights,
                "complaints":     self.state.complaints,
            }
        )
        print("\n[FLOW] ✅ Report written successfully → output/report.md")
        return str(result)


# ── Entrypoint ────────────────────────────────────────────────────────────────

def main():
    video_url = input("Enter YouTube video URL: ").strip()
    flow = CommentAnalysisFlow()
    flow.state.video_url = video_url
    flow.kickoff()


if __name__ == "__main__":
    main()