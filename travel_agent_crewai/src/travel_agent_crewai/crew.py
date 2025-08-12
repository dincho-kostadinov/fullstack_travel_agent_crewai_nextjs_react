from crewai import Agent, Task, Crew, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import yaml

_ = load_dotenv()

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)
@CrewBase
class TravelCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    """Travel Agent Crew."""

    @agent
    def travel_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["travel_agent"],
            tools=[SerperDevTool()],
            llm=llm,
            verbose=True,
       
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["reporting_analyst"],
            llm=llm,
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.travel_agent(),
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config["reporting_task"],
            agent=self.reporting_analyst(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.travel_agent(), self.reporting_analyst()],
            tasks=[self.research_task(), self.reporting_task()],
            verbose=True,
        )
