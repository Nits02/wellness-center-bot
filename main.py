from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


@app.post("/webhook", response_model=ChatbotResponse)
def webhook(payload: ChatbotRequest):
    """
    Webhook endpoint to receive incoming Chatbot requests.
    Currently just receives the payload, prints it, and returns a static response.
    """
    print(f"Received webhook payload: user_id={payload.user_id}, user_message='{payload.user_message}'")

    return ChatbotResponse(
        status="success",
        message="Message received successfully."
    )
