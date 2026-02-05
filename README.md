# 🤖 AutoWare: Autonomous Fleet & Supply Chain Simulator

### 📖 Project Overview
**AutoWare** is a full-stack robotics simulation engine designed to replicate the control logic of modern fulfillment center fleets (e.g., Amazon Kiva/Hercules systems).

Unlike simple animations, this project implements a **deterministic physics engine** driven by **A* (A-Star) Pathfinding** and **Finite State Machines (FSM)**. It features a distributed architecture where the Python backend handles complex collision logic and multi-threading, while the React frontend visualizes real-time telemetry. The system is cloud-connected, streaming asynchronous agent logs to **AWS S3** to mimic real-world IoT reporting pipelines.

---

### 🚀 Key Features

#### 🧠 Dynamic A* Pathfinding & "Ghost Tracks"
* **Real-Time Rerouting:** Agents autonomously calculate optimal paths around static and dynamic obstacles using the A* algorithm (Manhattan Heuristic).
* **Projected Visualization:** The frontend renders "Ghost Tracks" (projected path dots) to visualize the robot's intended route before it moves, making the algorithm's decision-making process visible to the user.

#### ⚡ Smart Charging & Self-Preservation
* **Finite State Machine (FSM):** Robots operate on a strict logic cycle: `IDLE` → `FETCHING` → `DELIVERING`.
* **Battery Management:** The system implements a priority interrupt; if battery levels drop below **20%**, agents abandon their current mission and autonomously navigate to the nearest **Charging Zone**.

#### ☁️ Cloud-Native Telemetry (AWS)
* **Non-Blocking I/O:** The system utilizes Python `threading` to decouple network requests from the main physics loop.
* **S3 Integration:** Agent status (Position, Battery, State) is serialized and uploaded to an **AWS S3 Bucket** in real-time, simulating an industrial IoT logging pipeline.

#### 🖱️ Interactive "God Mode"
* **Chaos Engineering:** Users can click any cell on the grid during runtime to spawn or remove obstacles.
* **Dynamic Adaptation:** Robots instantly detect the new wall and re-calculate their path without pausing the simulation.

---

### 🛠️ Tech Stack

* **Frontend:** React.js, CSS Grid, Axios, CSS Transitions (Smooth Gliding)
* **Backend:** Python 3.12, Flask, Multi-threading
* **Algorithms:** A* Search, Collision Avoidance, Finite State Machines
* **Cloud:** AWS S3, Boto3 SDK
* **DevOps:** Virtual Environments (venv), Git, Requirements Management

---

### 📂 Repository Structure

```text
AutoWare-Fleet-Sim/
├── client/                 # React.js Frontend
│   ├── src/
│   │   ├── App.jsx         # Dashboard & Grid Rendering Logic
│   │   ├── App.css         # Animations & Zone Styling
│   │   └── main.jsx        # Entry Point
│   └── package.json        # Node Dependencies
├── server/                 # Python Flask Backend
│   ├── app.py              # API Endpoints (REST)
│   ├── simulation.py       # Physics Engine & State Machine
│   ├── pathfinding.py      # A* Algorithm Implementation
│   ├── aws_logger.py       # Threaded AWS S3 Uploader
│   └── requirements.txt    # Backend Dependencies
└── README.md               # Documentation
```
### ⚙️ Installation & Setup

#### 1. Backend (Simulation Engine)
The backend handles the physics loop and pathfinding logic.

```
cd server

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (Flask, Boto3)
pip install -r requirements.txt

# Start the server
python3 app.py
```

*Server runs on `http://127.0.0.1:5001`*

#### 2. Frontend (Dashboard)
The frontend visualizes the fleet and handles user interaction.

```
cd client

# Install Node modules
npm install

# Start the development server
npm run dev
```
*Client runs on `http://localhost:5173`*

---

### 📊 System Architecture

* **The Tick Loop:** The frontend polls the backend every **1000ms** (1 tick).
* **State Update:** The `WarehouseSimulation` class updates robot coordinates based on the A* path plan.
* **Conflict Resolution:** If a path is blocked by a user (God Mode) or another robot, the agent halts and recalculates a new route in the next tick.
* **Async Logging:** A separate thread captures the fleet state and pushes a JSON log to **AWS S3**, ensuring the simulation never stutters due to network latency.

---

### 🛡️ Security Note

* **No Hardcoded Keys:** This project strictly follows security best practices. AWS credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) are loaded from the environment or local AWS configuration, ensuring no secrets are exposed in the source code.
* **Git History:** The repository history has been sanitized to ensure no sensitive configuration files (`.env`, `venv`) were accidentally committed.
