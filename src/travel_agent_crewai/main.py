from travel_agent_crewai.crew import TravelCrew

def main():
    travel_crew = TravelCrew()
    result = travel_crew.crew().kickoff(inputs={"city": "Paris", "start_date": "2025-08-15", "end_date": "2025-08-20", "people": 2})
    print(result)

if __name__ == "__main__":
    main()