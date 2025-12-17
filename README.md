# Medical Interview AI System

## Problem statement

Clinics often collect pre-visit medical intake information manually, leading to incomplete or inconsistent data.
Patients may provide vague or partial descriptions of their symptoms, medications, or allergies, requiring clinicians to repeat basic questioning during the visit.
This system addresses the problem by using a conversational AI agent that gathers, clarifies, and validates intake information through multi-turn dialogue, producing a structured summary ready for clinical use.


## Overview

This project provides an **AI-powered medical intake system** that collects patient information **before a clinic visit** through a natural, human-like conversation.

It is designed to:
- Ask follow-up questions when information is missing
- Confirm that nothing important was missed
- Produce a structured intake form for clinicians
- Validate intake quality before completion

> ⚠️ This system does **not** provide diagnosis or medical advice.


## High-Level Architecture
```mermaid
graph TD
  P[Patient] -->|Chat| IA[Medical Interview Agent<br>- Conversational<br>- Human-like asking<br>- Fills intake form]
  IA -->|update_intake_form| DB[(Intake Form / DB)]
  IA -->|call agent as tool| RV
  DB -->|read_intake_form| RV[Reviewer Agent<br>- Quality check<br>- Pass / Fail]
  RV -->|Pass| DONE[Interview Completed]
  RV -->|Fail: actionable feedback| IA
```

## Medical Interview Agent

### Role

The Medical Interview Agent conducts a **multi-turn interview** with the patient and fills out the intake form step by step.

It behaves similarly to a trained human interviewer:
- Uses empathetic language
- Asks only **1–2 questions at a time**
- Confirms unclear answers
- Explicitly checks “anything else?”

---

### Required Intake Information

The agent must collect **all six categories**:

```
1. Reason for visit
2. Symptoms
3. Duration / onset
4. Severity (0–10 or daily impact)
5. Current medications
6. Allergies
```

The interview **cannot finish** until all six are sufficiently covered.

---

### Interview Flow (Phase-Based)

```
Phase A ──► Chief Complaint
Phase B ──► Symptom Details (OPQRST)
Phase C ──► Related Symptoms
Phase D ──► “Anything else?” Coverage Check
Phase E ──► Summary & Patient Confirmation
Phase F ──► Review & Completion
```

---

### Symptom Deep Dive ([OPQRST](https://www.osmosis.org/answers/opqrst-pain-assessment-mnemonic))

For key symptoms, the agent gradually collects:

```
O – Onset        (When did it start?)
P – Provocation  (What makes it better/worse?)
Q – Quality      (How does it feel?)
R – Region       (Where is it?)
S – Severity     (0–10 or life impact)
T – Timing       (Constant? Improving? Worsening?)
```

Not all details are required at once — missing parts are asked later.

---

### Coverage Confirmation (Critical)

The following are **not considered complete** until explicitly confirmed:

```
Symptoms     → “No other symptoms”
Medications  → “No other medications (including OTC/supplements)”
Allergies    → “No other allergies”
```

This mirrors how human clinicians avoid missing secondary issues.

---

## Reviewer Agent (Quality Gate)

### Role

The Reviewer Agent checks whether the intake is **good enough for a clinical visit**.

It verifies the following points:
- Are all categories present?
- Any clear contradictions?
- Coverage confirmed (“no more”)?

If **any check fails**, the reviewer returns **specific feedback** (e.g., “duration unclear”, “medications not fully confirmed”).

---

## Example Feedback Loop

```
Patient → Intake Agent
        → Intake Form
        → Reviewer Agent
        → "Medication coverage not confirmed"
        → Intake Agent asks follow-up
        → Updated Intake Form
        → Reviewer Passes
```

---

## Tech Stack

### Frontend
- **React + TypeScript**
- **Routing + Framework:** React Router
- **Chat UI:** [`@openai/chatkit-react`](https://platform.openai.com/docs/guides/chatkit)
- **Styling:** Tailwind CSS
- **UI Components:** shadcn/ui

### Backend
- **Python**
- **API framework:** FastAPI
- **Chat server:** [OpenAI ChatKit Python SDK](https://openai.github.io/chatkit-python/)
- **Agent framework:** [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- **Validation:** Pydantic
- **ORM:** SQLAlchemy

### Database
- **PostgreSQL**
- **Primary storage:** JSONB column for intake form payload (prototype-friendly)

### LLMOps
- **Tracing:** [Braintrust](https://www.braintrust.dev/)


## Runtime Architecture
![alt text](SystemDiagram.drawio.png)

## Multi-turn Conversation (Chat) Sequence Diagram
```mermaid
sequenceDiagram
  autonumber
  participant U as User (Browser)
  participant FE as Frontend (React Router)
  participant CK as ChatKit UI (@openai/chatkit-react)
  participant API as FastAPI (POST /chatkit)
  participant S as MyChatKitServer.respond()
  participant ST as MyChatKitStore (memory)
  participant DB as PostgreSQL (MedicalInterview.intake)
  participant AG as Agents SDK (Runner.run_streamed)
  participant OAI as OpenAI API

  U->>FE: Navigate UI (medical_interview route)
  FE->>API: GET /api/medical_interviews/{id}
  API->>DB: SELECT medical_interviews
  DB-->>API: Return intake, etc.
  API-->>FE: JSON response

  U->>CK: Send message
  CK->>API: POST /chatkit (with x-interview-id header)
  API->>S: server.process(body, context)
  S->>DB: Load intake form by interview_id
  S->>ST: load_thread_items(recent history)
  S->>AG: Runner.run_streamed(agent, input_items)
  AG->>OAI: LLM inference (streaming)
  AG->>DB: (tool) Update intake via update_intake_form, etc.
  AG-->>S: Stream events (progress/widget/effect)
  S-->>CK: Stream via SSE (text/event-stream)
  CK-->>FE: Update UI (e.g., re-fetch intake in side panel)
```

## Why use Chatkit?
This prototype focuses on quickly validating an AI agent–based chat experience, and ChatKit was selected for the following reasons:

- **Reduced effort for chat UI implementation**<br>
Core chat features such as message input, conversation history, and streaming responses are provided out of the box, allowing us to focus on validating agent logic rather than building the UI from scratch.

- **Strong compatibility with the OpenAI Agents SDK**<br>
ChatKit aligns well with the design principles of the OpenAI Agents SDK, making it easier to build, iterate on, and extend agent-based architectures in the future.

---
## Development Setup

This section describes how to set up and run the application locally for
development.

------------------------------------------------------------------------

### Prerequisites

-   Python 3.10+
-   Node.js 18+
-   npm
-   PostgreSQL

------------------------------------------------------------------------

### Backend Setup (FastAPI)

#### 1. Create a Python virtual environment

``` bash
python -m venv .venv
```

#### 2. Activate the virtual environment

-   **Windows Command Prompt**

``` cmd
.venv\Scripts\activate.bat
```

-   **macOS / Linux**

``` bash
source .venv/bin/activate
```

#### 3. Install Python dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

### Database Setup (PostgreSQL)

#### 4. Prepare PostgreSQL

Make sure PostgreSQL is installed and running locally.

#### 5. Create a development database

``` sql
CREATE DATABASE medical_appointment_dev;
```

------------------------------------------------------------------------

### Environment Configuration

#### 6. Add environment variables

Create a `.env` file in the project root and define the required
environment variables.

``` env
PRODUCTION=false
DATABASE_URL=postgresql://user:password@localhost:5432/medical_appointment_dev
OPENAI_API_KEY=<your_api_key>
BRAINTRUST_API_KEY=<your_api_key>
```

------------------------------------------------------------------------

### Start Backend Server

#### 7. Run FastAPI in development mode

``` bash
fastapi dev main.py
```

------------------------------------------------------------------------

### Frontend Setup

#### 8. Move to the frontend directory

``` bash
cd frontend
```

#### 9. Install frontend dependencies

``` bash
npm install
```

#### 10. Start the frontend development server

``` bash
npm run dev
```

------------------------------------------------------------------------

### Seed Dummy Data

#### 11. Insert dummy data into the database
Insert dummy data into patients and appointments table.

------------------------------------------------------------------------

### Access the Application

-   Backend API: http://localhost:8000/docs
-   Frontend: http://localhost:5173

