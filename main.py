import json
import os
import random

from dotenv import load_dotenv
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from pydantic import BaseModel

from supabase_client import get_supabase_client

load_dotenv()

app = FastAPI(title="Wellness Center POC Backend")

# Setup CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class ChatbotRequest(BaseModel):
    user_id: str
    user_message: str

class ChatbotResponse(BaseModel):
    status: str
    message: str


# Endpoints
@app.get("/health")
def health_check():
    """Basic health check endpoint."""
    return {"status": "ok"}


SCHEDULING_SYSTEM_PROMPT = (
    "You are a clinical scheduling assistant for a wellness center that offers "
    "Gym, Ozone Therapy, Cryotherapy, Hyperbaric Oxygen Therapy, and Ayurvedic treatments. "
    "Extract the requested service and desired time from the user message. "
    "Output ONLY a JSON object with keys: intent, service, proposed_time. "
    "intent must be one of: 'book_appointment', 'cancel_appointment', 'check_availability', or 'unknown'. "
    "service must be the treatment/service name. "
    "proposed_time must be an ISO 8601 datetime string (use today's date if the user says 'today', "
    "tomorrow's date if they say 'tomorrow', etc.). "
    "If you cannot determine the intent, set intent to 'unknown'."
)


def _parse_scheduling_intent(user_message: str) -> dict:
    """Send user message to Gemini and parse the scheduling JSON response."""
    api_key = os.getenv("GOOGLE_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=f"{SCHEDULING_SYSTEM_PROMPT}\n\nUser message: {user_message}",
    )

    raw_text = response.text.strip()
    # Strip markdown code fences if present
    if raw_text.startswith("```"):
        raw_text = raw_text.split("\n", 1)[1] if "\n" in raw_text else raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3].strip()

    return json.loads(raw_text)


@app.post("/webhook", response_model=ChatbotResponse)
def webhook(payload: ChatbotRequest):
    """
    Webhook endpoint: sends the user message to Gemini for intent parsing,
    then books an appointment in Supabase if intent is 'book_appointment'.
    """
    try:
        parsed = _parse_scheduling_intent(payload.user_message)
    except (json.JSONDecodeError, Exception) as exc:
        return ChatbotResponse(
            status="error",
            message=f"Sorry, I couldn't understand your request. Please try rephrasing. (Details: {exc})",
        )

    intent = parsed.get("intent", "unknown")
    service = parsed.get("service", "Unknown Service")
    proposed_time = parsed.get("proposed_time")

    if intent == "unknown" or not proposed_time:
        return ChatbotResponse(
            status="error",
            message="I wasn't able to determine the service or time from your message. Could you please be more specific?",
        )

    if intent == "book_appointment":
        supabase = get_supabase_client()
        supabase.table("appointments").insert({
            "user_id": payload.user_id,
            "service_type": service,
            "appointment_time": proposed_time,
            "status": "scheduled",
        }).execute()

        return ChatbotResponse(
            status="success",
            message=f"Your {service} appointment has been booked for {proposed_time}. See you then!",
        )

    return ChatbotResponse(
        status="success",
        message=f"Understood! Intent: {intent}, Service: {service}, Time: {proposed_time}.",
    )


@app.post("/simulate-occupancy")
def simulate_occupancy():
    """Generate a random headcount (0-50) and log it to the occupancy table."""
    headcount = random.randint(0, 50)
    supabase = get_supabase_client()
    supabase.table("occupancy").insert({"current_count": headcount}).execute()
    return {"status": "success", "headcount": headcount}


@app.get("/current-occupancy")
def current_occupancy():
    """Fetch the most recent headcount and return a crowding status."""
    supabase = get_supabase_client()
    result = (
        supabase.table("occupancy")
        .select("current_count")
        .order("timestamp", desc=True)
        .limit(1)
        .execute()
    )

    if not result.data:
        return {"status": "no_data", "message": "No occupancy data available."}

    count = result.data[0]["current_count"]

    if count < 15:
        level = "Less Crowded"
    elif count <= 35:
        level = "Moderate"
    else:
        level = "Highly Crowded"

    return {"status": "success", "current_count": count, "occupancy_level": level}
