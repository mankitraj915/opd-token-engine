# OPD Token Allocation Engine

## Overview
This project is a backend system designed to manage hospital Outpatient Department (OPD) token allocation with **elastic capacity**. It handles real-world variability such as emergency insertions, cancellations, and doctor availability.

## Features
* **Elastic Capacity**: Supports dynamic slot resizing for emergencies.
* **Priority Queueing**: Automatically reorders patients based on triage urgency (Emergency > Paid > Standard).
* **Real-time Reallocation**: When a patient cancels, the queue is instantly rebalanced to fill gaps.

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
