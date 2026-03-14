# AI Agent System for IoT Monitoring and Automated Decision-Making

A modular IoT monitoring and decision-making backend built with FastAPI, SQLite, Docker, and Open-Meteo integration.

This project simulates an intelligent IoT monitoring platform for cold-chain / warehouse scenarios. It ingests sensor data, detects anomalies, evaluates risk, integrates external weather context, generates structured recommendations, and stores decision logs for auditing and review.

---

## Features

- FastAPI-based REST API backend
- Structured sensor input validation with Pydantic
- Rule-based anomaly detection
- Risk scoring and severity classification
- Policy-driven recommendation generation
- External weather context integration using Open-Meteo
- SQLite-based persistence for sensor and decision logs
- Modular API routing and service-layer design
- Automated test coverage with pytest
- Dockerized deployment

---

## Use Case

This system is designed for IoT monitoring scenarios such as:

- cold-chain storage
- warehouse environmental monitoring
- smart facility health checks
- equipment condition tracking

The platform combines:

- sensor data
- weather context
- anomaly detection
- policy decision logic

to produce interpretable operational decisions.

---

## Tech Stack

- **Backend:** FastAPI, Uvicorn
- **Validation:** Pydantic
- **Database:** SQLite, SQLAlchemy
- **External API:** Open-Meteo
- **Testing:** pytest
- **Deployment:** Docker, Docker Compose
- **Language:** Python 3.12

---

## System Architecture

```mermaid
flowchart TD
    A[IoT Sensor Input] --> B[FastAPI API Layer]
    B --> C[Schema Validation]
    C --> D[Weather Service]
    C --> E[Anomaly Detection Service]
    E --> F[Policy Service]
    D --> E
    F --> G[Decision Output]
    G --> H[SQLite Logging]
    H --> I[Logs API]
