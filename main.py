
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

API_KEY = "ak_8kun4nizv7jrz4yov10six4x"
EMAIL = "24f2006704@ds.study.iitm.ac.in"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["X-API-Key", "Content-Type"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: List[Event]


@app.post("/analytics")
def analytics(
    data: AnalyticsRequest,
    x_api_key: str = Header(default=None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_totals = {}
    revenue = 0.0

    for event in data.events:
        if event.amount > 0:
            revenue += event.amount
            user_totals[event.user] = (
                user_totals.get(event.user, 0.0) + event.amount
            )

    top_user = (
        max(user_totals, key=user_totals.get)
        if user_totals else None
    )

    return {
        "email": EMAIL,
        "total_events": len(data.events),
        "unique_users": len(set(e.user for e in data.events)),
        "revenue": round(revenue, 2),
        "top_user": top_user
    }
