from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import re

from travel_agent_crewai.crew import TravelCrew

app = FastAPI()

origins = ["http://localhost", "http://localhost:3000","http://localhost:3001"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

travel_crew = TravelCrew()

class ResearchRequest(BaseModel):
    city: str
    start_date: str
    end_date: str
    people: int


def parse_raw_json(raw_str: str):
    # Remove triple backticks and optional 'json' tag
    if raw_str.startswith("```json"):
        raw_str = raw_str[len("```json"):].strip()
    if raw_str.endswith("```"):
        raw_str = raw_str[:-3].strip()
    # Parse and return JSON object
    return json.loads(raw_str)

@app.post("/research")
async def research(request: ResearchRequest):
    try:
        crew_instance = travel_crew.crew()
        crew_output = crew_instance.kickoff(
            inputs={
                "city": request.city,
                "start_date": request.start_date,
                "end_date": request.end_date,
                "people": request.people
            }
        )

        raw_result = crew_output.raw
        parsed = parse_raw_json(raw_result)

        return {
            "summary": parsed.get("summary", ""),
            "hotels": parsed.get("hotels", [])
            # "test":crew_output.raw
        }

    except json.JSONDecodeError:
        return {"error": "Invalid JSON returned by AI."}
    except Exception as e:
        return {"error": str(e)}


@app.get("/")
async def root():
    return {"message": "TravelCrew API is running."}
