import random
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

# ---------- Example schema ----------
class Result(BaseModel):
    destination: str
    country: str
    lat: float
    lon: float
    score: float
    confidence: float
    trend_delta: float | None = None
    tags: List[str] = []
    context_cues: Dict[str, Any] = {}
    snippets: List[str] = []
    why: Dict[str, Any] = {}

class SearchResponse(BaseModel):
    query: str
    params: Dict[str, Any]
    results: List[Result]

class SearchRequest(BaseModel):
    query: str

# ---------- Dummy corpus ----------
CITIES = [
    {"destination": "Paris", "country": "France", "lat": 48.8566, "lon": 2.3522},
    {"destination": "Tokyo", "country": "Japan", "lat": 35.6895, "lon": 139.6917},
    {"destination": "New York", "country": "USA", "lat": 40.7128, "lon": -74.0060},
    {"destination": "Sydney", "country": "Australia", "lat": -33.8688, "lon": 151.2093},
    {"destination": "Cape Town", "country": "South Africa", "lat": -33.9249, "lon": 18.4241},
]

# ---------- Mock search endpoint ----------
@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest): 
    """Return a random travel city for frontend-backend communication testing."""
    choice = random.choice(CITIES)

    result = Result(
        destination=choice["destination"],
        country=choice["country"],
        lat=choice["lat"],
        lon=choice["lon"],
        score=round(random.uniform(0.6, 0.99), 3),
        confidence=round(random.uniform(0.7, 1.0), 3),
        trend_delta=random.choice([0.1, 0.0, -0.05]),
        tags=["test", "demo", "mock"],
        context_cues={"positive": {"demo": 1}, "negative": {}},
        snippets=[f"{choice['destination']} is a popular travel destination for testing!"],
        why={"reason": "Mock result for connection testing."},
    )

    return SearchResponse(
        query=req.query,
        params={"mode": "mock"},
        results=[result],
    )
