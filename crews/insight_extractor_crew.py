from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


_llm = LLM(model="ollama/gemma4:e4b", base_url="http://localhost:11434")


@CrewBase
class InsightExtractorCrew():
    """Crew that extracts insights from positive YouTube comments"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def insight_extractor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["insight_extractor_agent"],  # type: ignore[index]
            llm=_llm,
            verbose=True,
        )

    @task
    def topic_insights_task(self) -> Task:
        return Task(
            config=self.tasks_config["topic_insights_task"],  # type: ignore[index]
            agent=self.insight_extractor_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Insight Extractor crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )