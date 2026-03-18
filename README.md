# Rural Connect: Smart Telemedical Doctor Recommendation System

Rural Connect is an AI-powered telemedical support platform designed to help patients quickly find the most suitable doctors based on their disease or emergency condition, preferred city or region, language preference, and urgency level.

The system is especially focused on improving healthcare accessibility for rural and semi-urban communities, where patients often face difficulties in identifying the right specialist, language barriers, and delayed access to emergency care.

## Problem Statement

In many rural and remote areas, patients struggle to:

- Identify the correct specialist for their health condition
- Find doctors in nearby or desired regions
- Communicate with doctors in their preferred language
- Access telemedicine options during urgent or emergency situations
- Receive quick doctor recommendations without confusion

This delay in finding the right medical support can become critical in severe health conditions such as cardiac arrest, stroke, trauma, or sudden complications.

## Solution Overview

Rural Connect solves this problem by providing an intelligent doctor recommendation system that:

- Accepts user input such as symptoms, disease, emergency type, city, preferred language, and urgency level
- Maps symptoms or conditions to the appropriate medical specialist
- Filters doctors based on region and language compatibility
- Prioritizes doctors who support emergency cases
- Displays direct contact details, appointment booking links, and video consultation links
- Helps patients and families make faster and safer healthcare decisions

## Key Features

- AI-based symptom-to-specialist mapping
- Doctor recommendation based on disease or emergency condition
- Region-wise doctor search (e.g., Chennai, Bengaluru, Thoothukudi)
- Preferred language-based doctor filtering (Tamil, English, etc.)
- Urgency-aware recommendations (normal / urgent / emergency)
- Emergency support prioritization
- Direct doctor phone number access
- Appointment booking links
- Video consultation links for telemedicine
- Clean and interactive Streamlit frontend
- FastAPI backend for scalable API integration
- CSV-based dataset support for quick prototyping and hackathon deployment

## Example Use Case

A patient in a village such as Udangudi in Thoothukudi district is experiencing symptoms of a cardiac emergency.

Instead of manually searching for hospitals or specialists, the user can enter:

- Disease / emergency type: `cardiac arrest`
- Preferred city: `Chennai`
- Preferred language: `Tamil` or `English`
- Current village / district: `Udangudi, Thoothukudi`
- Urgency: `Emergency`

The system automatically recommends cardiologists in Chennai who speak the requested language, support emergency cases, and provide contact details along with teleconsultation links.

## Project Architecture

```text
User Input (Frontend - Streamlit)
        ↓
FastAPI Backend API
        ↓
Symptom-to-Specialist Mapping
        ↓
Doctor Dataset Filtering + Scoring
        ↓
Ranked Doctor Recommendations
        ↓
Frontend Display (Doctor cards, phone, booking, video consult)
Tech Stack
Frontend

Streamlit

Backend

FastAPI

Uvicorn

Data Processing

Pandas

Data Storage (Prototype Phase)

CSV files

Dataset Files

doctors.csv

symptom_specialist_map.csv

Folder Structure
Rural_Connect/
│
├── backend/
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── doctors.csv
│   └── symptom_specialist_map.csv
│
└── README.md
How It Works
1. User Input

The user provides:

Disease / symptoms / emergency type

Preferred city or region

Preferred language

Optional current village / district

Urgency level

Number of doctor recommendations required

2. Symptom Mapping

The system checks the symptom mapping dataset to identify:

The best matching specialist

Emergency level

Relevant keywords

3. Doctor Filtering

The doctor dataset is filtered using:

Matching specialist

Preferred city or region

Preferred language

Emergency support availability

4. Scoring and Ranking

Doctors are ranked based on:

Specialty match

Language match

City match

Emergency support

Consultation mode

Doctor rating

5. Recommendation Output

The system displays:

Doctor name

Specialty and subspecialty

Hospital name

City and area

Languages spoken

Phone number

Rating

Emergency support status

Consultation mode

Booking link

Video consultation link

Installation and Setup
1. Clone the Repository
git clone https://github.com/your-username/Rural_Connect.git
cd Rural_Connect
2. Create Virtual Environment
python -m venv codevault
3. Activate Virtual Environment
Windows
codevault\Scripts\activate
4. Install Dependencies
pip install fastapi uvicorn pandas streamlit requests
Running the Backend

From the project root:

cd backend
uvicorn main:app --reload

Backend will run at:

http://127.0.0.1:8000
Running the Frontend

Open another terminal from the project root:

streamlit run frontend/app.py

Frontend will open in the browser automatically.

API Endpoint
Health Check
GET /
Doctor Recommendation
POST /recommend
Sample Request Body
{
  "symptoms": "cardiac arrest",
  "city": "Chennai",
  "language": "English",
  "village": "Udangudi, Thoothukudi",
  "urgency": "emergency",
  "top_k": 5
}
Future Enhancements

To make Rural Connect more impactful and production-ready, the following features can be added:

Live hospital bed availability integration

Ambulance recommendation and nearest emergency center routing

Multi-language voice input for rural users

Speech-to-text support for non-technical users

GPS-based nearby doctor suggestions

Government hospital prioritization

AI chatbot for symptom pre-screening

WhatsApp integration for emergency consultation links

SMS alerts for low-network areas

Cloud deployment (AWS / Azure / GCP)

Database integration (PostgreSQL / MySQL / MongoDB)

Role-based login for patients, doctors, and hospitals

Real-World Impact

Rural Connect has strong potential in:

Rural healthcare access improvement

Faster emergency response assistance

Language-inclusive telemedicine

Reducing confusion during medical emergencies

Supporting underserved communities with digital health access

This project aligns with the broader goal of making healthcare more accessible, equitable, and technology-driven.

Why This Project Stands Out

Solves a real and meaningful healthcare accessibility problem

Designed specifically for rural and semi-urban needs

Combines telemedicine with intelligent doctor recommendation

Supports language-based inclusivity

Emergency-focused healthcare support

Simple prototype with high real-world scalability

Strong hackathon relevance and social impact

Limitations (Prototype Version)

Uses CSV files instead of a production database

Doctor data is static and sample-based

Links and phone numbers may be placeholder/demo values

Does not yet integrate live hospital or ambulance APIs

Recommendation logic is rule-based and can be further improved with ML/NLP

Conclusion

Rural Connect is a practical and socially impactful telemedical recommendation system that helps patients quickly discover the right specialist based on condition, location, language, and urgency.

It is designed as a strong prototype for hackathons, academic projects, and future real-world healthcare innovation, especially for improving digital medical access in rural India.
