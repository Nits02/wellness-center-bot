# AI-Powered Scheduling & Occupancy Tracker POC

## 1. Business Context & Target Audience
This Proof of Concept (POC) is designed for Chellaram Ultra Wellness Clinic, a premium 20,000-square-foot integrative healthcare facility in Pune, Maharashtra. The clinic offers a mix of modern biohacking therapies (such as Hyperbaric Oxygen Therapy, Cryotherapy, and Ozone Therapy) alongside a fully equipped gymnasium and traditional Ayurvedic treatments.

Currently, scheduling these diverse modalities is highly complex. Different treatments require specific equipment, room capacities, and practitioner skill sets. Manual scheduling often leads to operational bottlenecks, underutilized clinical hardware, and revenue leakage from appointment no-shows—a problem that costs the broader healthcare system billions annually. Additionally, prospective gym members lack visibility into real-time facility crowding, creating a barrier to entry for free trials.

## 2. Product Overview
The proposed product is a cloud-based, AI-driven scheduling and facility management platform. Cloud-based platforms are currently the dominant deployment mode in the wellness software market due to their scalable deployment and lower IT management requirements.

The application allows users to interact with a conversational AI chatbot to book specific wellness treatments or subscribe to a 1-day/2-day gym trial. It features an intelligent backend that resolves complex scheduling constraints, mitigates no-shows through predictive analytics, and provides an administrative dashboard for staff to monitor real-time facility occupancy.

## 3. Core Features & Functional Requirements
### A. Conversational AI Chatbot (User Facing)
- **Natural Language Booking:** Users can type requests in plain English (e.g., "I'd like to book an Ozone Therapy session tomorrow afternoon" or "Can I get a 2-day gym trial?").
- **Real-Time Occupancy Queries:** Users can ask, "How busy is the gym right now?" The bot will query the backend and return a status based on current capacity (e.g., "Less Crowded," "Moderate," or "Highly Crowded").
- **Automated Confirmations:** Once an appointment is secured by the AI engine, the bot returns a digital itinerary or access pass confirmation.

### B. AI-Driven Clinical Scheduling Engine (Backend Logic)
- **Intent Parsing:** Uses an LLM (Large Language Model) to extract the requested service, date, and time from the user's natural language message.
- **Constraint Resolution:** Cross-references the requested time against database availability for specific resources (e.g., checking if the Ozone Therapy room is free).
- **Proactive Optimization:** In a production environment, AI scheduling shifts workforce management from a reactive approach to proactive planning. For this POC, the engine will demonstrate intelligence by identifying available slots and simulating the mitigation of no-shows (e.g., highlighting slots that could be double-booked to prevent revenue loss).

### C. Real-Time Occupancy Tracker & Admin Dashboard (Staff Facing)
- **Data Visualization:** A web-based dashboard displaying a live-updating timeline (line chart) of gym occupancy throughout the day.
- **Appointment Management:** A data table view of all upcoming bookings, categorized by service type (Gym Trial, Ozone Therapy, etc.).
- **Occupancy Simulation:** A backend service that simulates live IoT sensor data by periodically generating and logging headcount metrics to the database.

## 4. Technical Architecture & Tech Stack
The POC will be built using a modern, lightweight microservices architecture suitable for rapid prototyping and low-cost cloud deployment.
- **Frontend (Admin Dashboard):** Streamlit (Python). Used for rapid UI development of the occupancy timeline and appointment tables.
- **Frontend (Chatbot UI):** Botpress or Dialogflow web widget (communicating via webhooks).
- **Backend API Framework:** FastAPI (Python). Chosen for its speed, asynchronous capabilities, and ease of creating RESTful endpoints and webhooks.
- **Database:** Supabase (PostgreSQL). A cloud-native database that provides a generous free tier and easy Python integration via the supabase-py client.
- **AI/NLP Layer:** OpenAI API (GPT-4o-mini). Used within the FastAPI backend to parse user intents and resolve scheduling logic.
- **Predictive Modeling (Mock):** Scikit-learn (Python). Used to create a lightweight mock model demonstrating demand forecasting.

## 5. Database Schema (Supabase / PostgreSQL)
The system requires three primary tables:

### Users Table:
- id (UUID, Primary Key)
- name (String)
- contact_number (String)
- membership_status (String - e.g., 'none', '2-day-trial', 'active')

### Appointments Table:
- id (UUID, Primary Key)
- user_id (UUID, Foreign Key)
- service_type (String - e.g., 'Ozone Therapy', 'Gym Trial')
- appointment_time (Timestamp)
- status (String - e.g., 'scheduled', 'completed', 'cancelled')

### Occupancy_Logs Table:
- id (UUID, Primary Key)
- timestamp (Timestamp, default to now)
- current_headcount (Integer)
