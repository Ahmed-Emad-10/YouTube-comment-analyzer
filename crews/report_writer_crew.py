from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


_llm = LLM(model="ollama/gemma4:e4b", base_url="http://localhost:11434")


@CrewBase
class ReportWriterCrew():
    """Crew that synthesizes all analysis into a final cohesive report"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def report_writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["report_writer_agent"],  # type: ignore[index]
            llm=_llm,
            verbose=True,
        )

    @task
    def report_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config["report_writing_task"],  # type: ignore[index]
            agent=self.report_writer_agent(),
            output_file="output/report.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Report Writer crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )