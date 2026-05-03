from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


_llm = LLM(model="ollama/gemma4:e4b", base_url="http://localhost:11434")


@CrewBase
class ComplaintDetectorCrew():
    """Crew that detects and categorizes complaints from negative YouTube comments"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def complaint_detector_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["complaint_detector_agent"],  # type: ignore[index]
            llm=_llm,
            verbose=True,
        )

    @task
    def complaint_detection_task(self) -> Task:
        return Task(
            config=self.tasks_config["complaint_detection_task"],  # type: ignore[index]
            agent=self.complaint_detector_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Complaint Detector crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )