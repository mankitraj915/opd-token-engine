# OPD Token Allocation Engine

## Overview
This project is a backend system designed to manage hospital Outpatient Department (OPD) token allocation with **elastic capacity**. [cite_start]It handles real-world variability such as emergency insertions, cancellations, and doctor availability

## Features
* [cite_start]**Elastic Capacity**: Supports dynamic slot resizing for emergencies[cite: 3].
* [cite_start]**Priority Queueing**: Automatically reorders patients based on triage urgency (Emergency > Paid > Standard)[cite: 17].
* [cite_start]**Real-time Reallocation**: When a patient cancels, the queue is instantly rebalanced to fill gaps[cite: 15].

## Technical Implementation

### 1. Prioritization Logic
The system uses a weighted priority mechanism implemented via Python's `IntEnum`. Lower values indicate higher priority:
* **Emergency (0)**: Bypasses all standard limits.
* **Paid Priority (1)**: Jump ahead of standard bookings.
* **Standard (3)**: First-Come-First-Served (FCFS).

When a token is requested, the algorithm inserts it into the slot's list and immediately runs a generic sort `O(N log N)` based on these priority weights.

### 2. Edge Case Handling
* [cite_start]**Hard Limit Enforcement**: Standard requests are rejected if `current_tokens >= max_capacity`[cite: 14].
* [cite_start]**Emergency Override**: Emergency requests explicitly bypass the hard limit check, allowing the system to expand capacity dynamically[cite: 18].
* [cite_start]**No-Shows/Cancellations**: The `handle_cancellation` method removes the token and shifts the entire queue up, ensuring no slot time is wasted[cite: 18].

### 3. Failure Handling
* **Invalid Doctor/Slot**: The API returns HTTP 404/400 errors for non-existent IDs.
* [cite_start]**Capacity Overflow**: The API returns a clear "Slot is full" error for non-emergency patients attempting to overbook[cite: 29].

## How to Run

### Prerequisites
* Python 3.8+
* FastAPI, Uvicorn, Pydantic

### Installation
```bash
python -m pip install fastapi uvicorn pydantic

## 🏗 System Architecture (Request Flow)

```mermaid
sequenceDiagram
    participant P as Patient
    participant API as FastAPI Endpoint
    participant E as Allocation Engine
    participant S as Slot (Priority Queue)

    P->>API: POST /book-token (Name, Priority)
    API->>E: allocate_token()
    
    alt Slot is Full
        E->>E: Check Hard Limit
        E-->>API: Error (400 Bad Request)
    else Slot Has Space OR Emergency
        E->>S: Append Token
        S->>S: Sort by Priority (O(log n))
        
        opt Starvation Check
            E->>E: prevent_starvation()
            E->>S: Re-sort if upgraded
        end
        
        E-->>API: Return Token ID
        API-->>P: Booking Confirmed
    end






🛠️ Installation & Setup
Option 1: Run Locally (Recommended for Development)
Clone the repository:

Bash

git clone [https://github.com/YOUR_USERNAME/opd-token-engine.git](https://github.com/YOUR_USERNAME/opd-token-engine.git)
cd opd-token-engine
Install Dependencies:

Bash

python -m pip install -r requirements.txt
Run the Simulation: This script demonstrates the priority logic and starvation prevention with a live CLI dashboard.

Bash

python -m app.simulator
Start the API Server:

Bash

python -m uvicorn app.main:app --reload
Access Swagger UI at: http://127.0.0.1:8000/docs

Option 2: Run with Docker
Build the Image:

Bash

docker build -t opd-engine .
Run the Container:

Bash

docker run -p 8000:8000 opd-engine


📂 Project Structure
Bash

opd-token-engine/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI Entry Points (API Design)
│   ├── engine.py        # Core Allocation & Priority Logic
│   ├── models.py        # Pydantic Schemas & Enums
│   └── simulator.py     # CLI Simulation Script (Rich UI)
├── tests/               # Unit Tests for Edge Cases
├── Dockerfile           # Production Container Config
├── requirements.txt     # Python Dependencies
└── README.md            # 



