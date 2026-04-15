# UCCIS Review Packet

## System Overview

Urban Command and Control Interface System (UCCIS) monitors city zones and enables real-time decision making.

## Features Implemented

- Zone Monitoring (Mumbai, Thane, Navi Mumbai)
- Status Indicators (Green, Yellow, Red)
- Real vs Synthetic Mode
- Alerts System (Severity + Timestamp)
- Action Control System
- Data Pipeline Representation

## Pipeline

Input → JSON Data  
Intelligence → Mode-based processing  
Alert → Generated alerts  
Action → Trigger buttons  
Output → Dashboard updates

## APIs

- /zones → Fetch zones
- /alerts → Fetch alerts
- /action → Trigger system action
- /mode → Switch real/synthetic

## Tech Stack

- Python (Flask)
- HTML, JS
- JSON Data

## Future Improvements

- Map integration
- Live APIs
- AI prediction system
