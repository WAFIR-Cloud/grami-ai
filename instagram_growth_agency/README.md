# Instagram Growth Agency AI Framework

## 🚀 Overview
A cutting-edge, distributed AI system for automated Instagram marketing and growth.

## 🌟 Key Features
- Event-driven microservices architecture
- AI-powered content generation
- Real-time workflow tracking
- Modular and extensible design

## 🛠 Services
- **Chat Interface Agent**: Customer interaction and workflow coordination
- **Growth Manager Agent**: Project initialization and strategy development
- **Content Creation Agent**: AI-driven media content generation
- **Scheduling Agent**: Optimal content posting schedule
- **Execution Agent**: Instagram content posting and performance tracking

## 📋 Prerequisites
- Docker (20.10+)
- Docker Compose (1.29+)
- Python 3.12
- Minimum 16GB RAM recommended

## 🔧 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/instagram-growth-agency.git
cd instagram-growth-agency
```

### 2. Environment Configuration
Copy `.env.example` to `.env` and update with your credentials:
```bash
cp .env.example .env
```

Edit `.env` and replace placeholders:
- `OPENAI_API_KEY`
- `INSTAGRAM_API_KEY`
- `GOOGLE_GEMINI_API_KEY`

### 3. Build and Run Services
```bash
# Build all services
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Development Mode
```bash
# Run in development mode with hot-reloading
docker-compose -f docker-compose.dev.yml up --build
```

## 🧪 Testing
```bash
# Run unit tests
docker-compose run --rm test

# Run integration tests
docker-compose run --rm integration-test
```

## 🔍 Monitoring
- Kafka: `http://localhost:9092`
- Redis Commander: `http://localhost:8081`
- Prometheus Metrics: `http://localhost:9090`

## 📦 Deployment
- Supports Kubernetes via Helm charts
- CI/CD ready with GitHub Actions

## 🚨 Troubleshooting
- Check Docker logs: `docker-compose logs <service_name>`
- Verify network connectivity
- Ensure all API keys are correctly configured

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and create a Pull Request

## 📄 License
MIT License

## 💬 Support
Join our [Discord Community](https://discord.gg/your-community) for support and discussions.

---

**Note**: This is an AI-powered system. Always review and validate generated content before publishing.
