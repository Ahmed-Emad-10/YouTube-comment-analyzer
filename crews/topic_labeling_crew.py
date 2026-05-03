from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


_llm = LLM(model="ollama/gemma4:e4b", base_url="http://localhost:11434")


@CrewBase
class TopicLabelingCrew():
    """Crew that turns raw topic modeling output into human-readable topic labels"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def topic_labeling_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["topic_labeling_agent"],  # type: ignore[index]
            llm=_llm,
            verbose=True,
        )

    @task
    def topic_labeling_task(self) -> Task:
        return Task(
            config=self.tasks_config["topic_labeling_task"],  # type: ignore[index]
            agent=self.topic_labeling_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Topic Labeling crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )