<p align="center">
  <img src="https://raw.githubusercontent.com/getbindu/create-bindu-agent/refs/heads/main/assets/light.svg" alt="bindu Logo" width="200">
</p>

<h1 align="center">Movie Recommender Agent</h1>
<h3 align="center">AI-Powered Personalized Movie Recommendation System</h3>

<p align="center">
  <strong>Provides intelligent movie suggestions based on preferences, genres, ratings, and viewing history. Uses Exa search for real-time movie data and ratings to deliver personalized recommendations.</strong><br/>
  Discover your next favorite film with AI-powered recommendations tailored to your tastes.
</p>

<p align="center">
  <a href="https://github.com/Paraschamoli/movie-recommender-agent/actions/workflows/build-and-push.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/Paraschamoli/movie-recommender-agent/build-and-push.yml?branch=main" alt="Build status">
  </a>
  <a href="https://img.shields.io/github/license/Paraschamoli/movie-recommender-agent">
    <img src="https://img.shields.io/github/license/Paraschamoli/movie-recommender-agent" alt="License">
  </a>
  <a href="https://img.shields.io/badge/python-3.12-blue">
    <img src="https://img.shields.io/badge/python-3.12-blue" alt="Python 3.12">
  </a>
</p>

---

## 🎯 What is Movie Recommender Agent?

An AI-powered assistant that provides personalized movie recommendations based on your preferences, viewing history, favorite genres, and mood. Think of it as your personal film curator that understands your taste and suggests movies you'll love.

### Key Features
*   **🎬 Personalized Recommendations** - Tailored to your unique preferences and taste.
*   **🌍 Global Cinema** - Recommendations from Hollywood to international films.
*   **⭐ Real-time Ratings** - Current IMDB, Rotten Tomatoes scores via Exa search.
*   **🎭 Genre Expertise** - All genres from thriller to romance, horror to comedy.
*   **🧠 Mood Matching** - Suggestions based on emotional tone and viewing context.
*   **📱 Streaming Info** - Guidance on platform availability.
*   **🎫 Upcoming Releases** - Information about anticipated new films.
*   **🧠 Memory Support** - Optional Mem0 integration for conversation context.

### Built-in Tools
*   **ExaTools** - Real-time movie information and ratings.
*   **Mem0Tools** - Optional conversation memory.
*   **Intelligent Analysis** - Preference understanding and matching.

### Recommendation Process
1.  **Preference Analysis** - Understand your tastes and requirements.
2.  **Movie Research** - Search current movie data via Exa.
3.  **Personalized Matching** - Match films to your preferences.
4.  **Comprehensive Info** - Provide ratings, cast, plot, and streaming details.
5.  **Contextual Suggestions** - Consider mood, viewing context, and group dynamics.

---

> **🌐 Join the Internet of Agents**
> Register your agent at [bindus.directory](https://bindus.directory) to make it discoverable worldwide and enable agent-to-agent collaboration. **It takes 2 minutes and unlocks the full potential of your agent.**

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Paraschamoli/movie-recommender-agent.git
cd movie-recommender-agent

# Set up virtual environment with uv
uv venv --python 3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys:
# OPENAI_API_KEY=sk-...      # For OpenAI GPT-4o (or)
# OPENROUTER_API_KEY=sk-...  # For OpenRouter (alternative)
# EXA_API_KEY=sk-...         # REQUIRED: Get from https://exa.ai
# MEM0_API_KEY=sk-...        # Optional: For conversation memory
```

### 3. Run Locally

```bash
# Start the movie recommender agent
python movie_recommender_agent/main.py

# Or using uv
uv run python movie_recommender_agent/main.py
```

### 4. Test with Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at: http://localhost:3773
```

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file:

```env
# Required APIs
EXA_API_KEY=sk-...           # Required for movie information

# Choose ONE LLM provider
OPENAI_API_KEY=sk-...        # OpenAI API key
OPENROUTER_API_KEY=sk-...    # OpenRouter API key (alternative)

# Optional features
MODEL_NAME=openai/gpt-4o     # Model ID for OpenRouter
MEM0_API_KEY=sk-...          # Optional: For memory operations
```

### Port Configuration
Default port: `3773` (can be changed in `agent_config.json`)

---

## 💡 Usage Examples

### Via HTTP API

```bash
curl -X POST http://localhost:3773/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Suggest thriller movies similar to Inception with IMDB ratings above 8.0"
      }
    ]
  }'
```

### Sample Movie Recommendation Queries
*   "What are the top-rated comedy movies from the last 2 years?"
*   "Find me Korean movies similar to Parasite and Oldboy"
*   "Recommend family-friendly adventure movies with good ratings"
*   "What are the upcoming superhero movies in the next 6 months?"
*   "Suggest psychological thrillers similar to Black Swan and Gone Girl"
*   "What are the best animated movies from Studio Ghibli?"
*   "Recommend mind-bending sci-fi movies like Inception and Interstellar"
*   "What are good family movies for kids aged 8-12?"
*   "Suggest comedy movies perfect for a group movie night"
*   "Find romantic movies with happy endings from the 2000s"

### Expected Response Format

```markdown
# 🎬 Thriller Movie Recommendations (IMDB 8.0+)

## 🎯 Based on your request for: Thrillers similar to Inception

### 🏆 Top Recommendations

| Movie | Year | Rating | Genre | Runtime | Why You Might Like It |
|-------|------|--------|-------|---------|----------------------|
| **Inception** | 2010 | ⭐ 8.8/10 IMDB | 🎬 Thriller, 🚀 Sci-Fi | 2h 28m | Mind-bending narrative you requested |
| **The Dark Knight** | 2008 | ⭐ 9.0/10 IMDB | 🎬 Thriller, 🦇 Action | 2h 32m | Complex storytelling like Inception |
| **Se7en** | 1995 | ⭐ 8.6/10 IMDB | 🎬 Thriller, 🔍 Crime | 2h 7m | Atmospheric, intellectually engaging |

## 🎞️ Detailed Recommendations

### 1. **Inception** (2010)
**⭐ Rating**: IMDB 8.8/10, 🍅 87% Rotten Tomatoes
**🎭 Genre**: Sci-Fi Thriller, Heist, Mystery
**⏱️ Runtime**: 2 hours 28 minutes
**🎞️ Director**: Christopher Nolan
**🌟 Starring**: Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page
**🎟️ Rating**: PG-13
**🌐 Language**: English, Japanese, French

**📖 Synopsis**:
Dom Cobb is a thief with the rare ability to enter people's dreams and steal their secrets from their subconscious. His skill has made him a hot commodity in the world of corporate espionage but has also cost him everything he loves. Cobb gets a chance at redemption when he is offered a seemingly impossible task: plant an idea in someone's mind. If he succeeds, it will be the perfect crime, but a dangerous enemy anticipates Cobb's every move.

**💡 Why this matches your request**:
Perfect match for "mind-bending thriller" - combines complex narrative structure with thrilling action sequences, similar intellectual engagement to what you enjoy.

### 2. **The Dark Knight** (2008)
**⭐ Rating**: IMDB 9.0/10, 🍅 94% Rotten Tomatoes
**🎭 Genre**: Action Thriller, Crime, Drama
**⏱️ Runtime**: 2 hours 32 minutes
**🎞️ Director**: Christopher Nolan
**🌟 Starring**: Christian Bale, Heath Ledger, Aaron Eckhart
**🎟️ Rating**: PG-13
**🌐 Language**: English

**📖 Synopsis**:
When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.

**💡 Why this matches your request**:
From the same director as Inception, features similarly complex moral dilemmas and psychological depth in a thriller framework.

## 🎪 Bonus Recommendations
- **Memento** (2000) - Christopher Nolan's earlier mind-bending thriller
- **Shutter Island** (2010) - Psychological thriller with similar mystery elements
- **The Prestige** (2006) - Another Nolan film with thriller and mystery elements

## 🔮 Upcoming Releases to Watch For
- **Tenet** (2020) - Christopher Nolan's latest mind-bending thriller
- **Dune: Part Two** (2024) - Epic sci-fi with thriller elements

## 💡 Tips for Your Movie Night
- **Inception** is best watched with full attention - avoid distractions
- Consider watching with subtitles to catch all dialogue
- Perfect for late-night viewing when you can focus on the complex plot

---

*Recommendations curated by PopcornPal 🎥*
*Last updated: 2024-01-15*
*Note: Streaming availability may vary by region*
```

---

## 🐳 Docker Deployment

### Quick Docker Setup

```bash
# Build the image
docker build -t movie-recommender-agent .

# Run container
docker run -d \
  -p 3773:3773 \
  -e EXA_API_KEY=your_exa_key \
  -e OPENAI_API_KEY=your_openai_key \
  -e MEM0_API_KEY=your_mem0_key \
  --name movie-recommender-agent \
  movie-recommender-agent

# Check logs
docker logs -f movie-recommender-agent
```

### Docker Compose (Recommended)

`docker-compose.yml`:

```yaml
version: '3.8'
services:
  movie-recommender-agent:
    build: .
    ports:
      - "3773:3773"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - EXA_API_KEY=${EXA_API_KEY}
      - MEM0_API_KEY=${MEM0_API_KEY}
    restart: unless-stopped
```

Run with Compose:

```bash
# Start with compose
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## 📁 Project Structure

```text
movie-recommender-agent/
├── movie_recommender_agent/
│   ├── skills/
│   │   └── movie-recommender/
│   │       ├── skill.yaml          # Skill configuration
│   │       └── __init__.py
│   ├── __init__.py
│   └── main.py                     # Agent entry point
├── agent_config.json               # Bindu agent configuration
├── pyproject.toml                  # Python dependencies
├── Dockerfile                      # Multi-stage Docker build
├── docker-compose.yml              # Docker Compose setup
├── README.md                       # This documentation
├── .env.example                    # Environment template
└── tests/                          # Test suite
```

---

## 🔌 API Reference

### Health Check

```bash
GET http://localhost:3773/health
```

**Response:**
```json
{"status": "healthy", "agent": "Movie Recommender Agent"}
```

### Chat Endpoint

```bash
POST http://localhost:3773/chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Your movie recommendation query here"}
  ]
}
```

---

## 🧪 Testing

### Local Testing

```bash
# Install test dependencies
uv sync --group dev

# Run tests
pytest tests/

# Test with coverage
pytest --cov=movie_recommender_agent tests/
```

### Integration Test

```bash
# Start agent
python movie_recommender_agent/main.py &

# Test API endpoint
curl -X POST http://localhost:3773/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Suggest comedy movies"}]}'
```

---

## 🚨 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **"EXA_API_KEY required"** | Get your key from [exa.ai](https://exa.ai) - This is required for movie information |
| **"No LLM API key provided"** | Set either `OPENAI_API_KEY` or `OPENROUTER_API_KEY` in your `.env` file |
| **"Port 3773 already in use"** | Change port in `agent_config.json` or kill the process: `lsof -ti:3773 \| xargs kill -9` |
| **Docker build fails** | Run `docker system prune -a` then `docker-compose build --no-cache` |
| **Memory errors with Mem0** | Verify your `MEM0_API_KEY` is valid and has sufficient credits |

---

## 📊 Dependencies

### Core Packages
*   **bindu** - Agent deployment framework
*   **agno** - AI agent framework
*   **exa-py** - Exa research API
*   **openai** - OpenAI client
*   **python-dotenv** - Environment management
*   **mem0ai** - Memory operations

### Development Packages
*   **pytest** - Testing framework
*   **ruff** - Code formatting/linting
*   **pre-commit** - Git hooks

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1.  Fork the repository.
2.  Create a feature branch: `git checkout -b feature/improvement`.
3.  Make your changes following the code style.
4.  Add tests for new functionality.
5.  Commit with descriptive messages.
6.  Push to your fork.
7.  Open a Pull Request.

**Code Style:**
*   Follow PEP 8 conventions.
*   Use type hints where possible.
*   Add docstrings for public functions.
*   Keep functions focused and small.

---

## 📄 License
MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Credits & Acknowledgments
*   **Developer:** Paras Chamoli
*   **Framework:** Bindu - Agent deployment platform
*   **Agent Framework:** Agno - AI agent toolkit
*   **Research Engine:** Exa - Movie information API
*   **Memory System:** Mem0 - Conversation memory API

### 🔗 Useful Links
*   🌐 **Bindu Directory:** [bindus.directory](https://bindus.directory)
*   📚 **Bindu Docs:** [docs.getbindu.com](https://docs.getbindu.com)
*   🐙 **GitHub:** [github.com/ParasChamoli/movie-recommender-agent](https://github.com/ParasChamoli/movie-recommender-agent)
*   💬 **Discord:** Bindu Community

<br/>

<p align="center">
  <strong>Built with ❤️ by Paras Chamoli</strong><br/>
  <em>Helping you discover amazing films tailored to your taste</em>
</p>

<p align="center">
  <a href="https://github.com/ParasChamoli/movie-recommender-agent/stargazers">⭐ Star on GitHub</a> •
  <a href="https://bindus.directory">🌐 Register on Bindu</a> •
  <a href="https://github.com/ParasChamoli/movie-recommender-agent/issues">🐛 Report Issues</a>
</p>

<p align="center">
  <em>Note: This agent provides movie recommendations and information for entertainment purposes. It does not handle movie streaming, downloads, or ticket purchases. Always respect copyright laws and use authorized streaming services. Powered by AI with comprehensive movie research capabilities.</em>
</p>
