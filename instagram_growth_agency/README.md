# Instagram Growth Agency Microservices

## Overview
A distributed, event-driven microservices architecture for Instagram growth marketing.

## Services
- Content Creator: Generates platform-specific content
- Social Media Manager: Develops social media strategies
- Market Researcher: Conducts market and competitive analysis
- Growth Manager: Orchestrates overall campaign workflow

## Prerequisites
- Docker
- Docker Compose
- Google Gemini API Key

## Setup
1. Set environment variables
```bash
export GOOGLE_GEMINI_API_KEY=your_api_key
```

2. Build and run services
```bash
docker-compose up --build
```

## Architecture
- Kafka for event-driven communication
- Redis for state management
- Containerized Python microservices
- Event-based task processing

## Communication Flow
1. Growth Manager receives client request
2. Tasks distributed via Kafka topics
3. Individual services process tasks
4. Results stored in Redis
5. Final strategy compiled by Growth Manager
