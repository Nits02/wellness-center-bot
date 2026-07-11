# Development Skills and Guidelines

## Tech Stack
- **Backend API Framework:** FastAPI (Python)
- **Frontend (Admin Dashboard):** Streamlit (Python)
- **Frontend (Chatbot UI):** Botpress or Dialogflow web widget (via webhooks)
- **Database:** Supabase (PostgreSQL) using the `supabase-py` client
- **AI/NLP Layer:** OpenAI API (`GPT-4o-mini`) via FastAPI
- **Predictive Modeling:** Scikit-learn (Python)

## Context Grounding Rules
- All new features and prompt responses must align with the AI-Powered Scheduling & Occupancy Tracker POC specification outlined in `spec.md`.
- No code will be generated unless explicitly instructed by the user as part of the step-by-step spec-driven development process.
- The project focuses on a lightweight microservices architecture suitable for rapid prototyping and low-cost deployment.
- The focus is on building an intelligent backend that resolves complex scheduling constraints, mitigates no-shows, and provides real-time facility occupancy monitoring.
