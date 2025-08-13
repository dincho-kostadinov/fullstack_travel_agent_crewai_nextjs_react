from crewai import Agent, Task, Crew, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import yaml

_ = load_dotenv()

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.5,
)
@CrewBase
class TravelCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    """Travel Agent Crew with availability checking."""

    @agent
    def travel_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["travel_research_agent"],
            tools=[SerperDevTool()],
            llm=llm,
            verbose=True,
        )

    @agent
    def travel_availability_checker_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["travel_availability_checker_agent"],
            llm=llm,
            verbose=True,
        )

    @agent
    def travel_reporting_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["travel_reporting_agent"],
            llm=llm,
            verbose=True,
            reasoning=True,
            max_reasoning_attempts=2
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.travel_research_agent(),
        )

    @task
    def availability_check_task(self) -> Task:
        return Task(
            config=self.tasks_config["availability_check_task"],
            agent=self.travel_availability_checker_agent(),
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config["reporting_task"],
            agent=self.travel_reporting_agent(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.travel_research_agent(),
                self.travel_availability_checker_agent(),
                self.travel_reporting_agent()
            ],
            tasks=[
                self.research_task(),
                self.availability_check_task(),
                self.reporting_task()
            ],
            verbose=True,
        )