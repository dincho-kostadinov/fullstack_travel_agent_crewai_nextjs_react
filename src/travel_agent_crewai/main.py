from travel_agent_crewai.crew import TravelCrew


if __name__ == "__main__":
    travel_crew = TravelCrew()
    travel_crew.crew().kickoff(inputs={"city": "Paris"})