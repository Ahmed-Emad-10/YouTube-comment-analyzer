# 🎯 YouTube Comment Analyzer

A multi-agent AI pipeline that scrapes YouTube comments and turns raw audience feedback into a structured, human-readable report — powered by NLP and Gen AI agents.

---

## What it does

Paste any YouTube URL and the pipeline will:

- **Scrape** all comments from the video
- **Topic Modeling** — clusters comments into topics using BERTopic and generates human-readable labels via AI
- **Sentiment Analysis** — classifies every comment as positive, neutral, or negative using a HuggingFace transformer model
- **Insight Extraction** — a Gen AI agent reads the positive comments and extracts what resonates with the audience
- **Complaint Detection** — a Gen AI agent reads the negative comments and surfaces recurring issues
- **Report Generation** — a final agent synthesizes everything into a clean markdown report

---

## Architecture

```
scrape()
   ├── topic_modeling() ──▶ TopicLabelingCrew
   │                               │
   └── sentiment_analysis()        │
           ├── InsightExtractorCrew │
           └── ComplaintDetectorCrew│
                                    ▼
                         and_() ──▶ ReportWriterCrew ──▶ output/report.md
```

Orchestrated with **CrewAI Flows** — two parallel branches run after scraping, and the report writer only triggers when all 3 crews are done.

---

## Project Structure

```
yt_comment_analyzer/
├── scraper/
│   └── youtube_scraper.py       # Fetches comments from YouTube
├── nlp/
│   ├── sentiment.py             # HuggingFace sentiment analysis
│   └── topic_modeling.py        # BERTopic topic modeling
├── crew/
│   ├── config/
│   │   ├── agents.yaml          # Agent definitions
│   │   └── tasks.yaml           # Task definitions
│   ├── topic_labeling_crew.py
│   ├── insight_extractor_crew.py
│   ├── complaint_detector_crew.py
│   └── report_writer_crew.py
├── output/                      # Generated reports (git-ignored)
├── app.py                       # Streamlit UI
├── main.py                      # CrewAI Flow entrypoint
└── requirements.txt
```

---

## Stack

| Layer | Tool |
|---|---|
| Orchestration | CrewAI Flows |
| LLM | Ollama (`gemma4:e4b`) — local, private |
| Sentiment Analysis | HuggingFace Transformers (`cardiffnlp/twitter-roberta-base-sentiment-latest`) |
| Topic Modeling | BERTopic |
| Scraping | youtube-comment-downloader |
| UI | Streamlit |

---

## Getting Started

### 1. Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- Pull the model:
  ```bash
  ollama pull gemma4:e4b
  ```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment

Create a `.env` file in the root:
```
OPENAI_API_KEY=none
```
> CrewAI requires this variable to exist even when using a local LLM.

### 4. Run via terminal

```bash
python main.py
```

### 5. Run via Streamlit UI

```bash
streamlit run app.py
```

---

## Output

The final report is saved to `output/report.md` and contains:

1. **Overview** — total comments, sentiment breakdown
2. **Topic Breakdown** — labeled topics with comment counts
3. **What Viewers Love** — insights from positive feedback
4. **Viewer Complaints** — patterns from negative feedback
5. **Recommendations** — actionable suggestions based on the analysis

---

## Notes

- All processing runs **locally** — no data is sent to external APIs
- The LLM is served by Ollama on `http://localhost:11434`
- Comments are truncated to 512 tokens before sentiment analysis to stay within model limits
- BERTopic filters out noise comments (topic = -1) before passing to the AI crew
