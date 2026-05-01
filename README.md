# AI Agent Chain 🔗

Fully automated AI agent pipeline for business automation powered by **Anthropic Claude**.

## Pipeline

The system runs **10 specialized AI agents** in sequence, each building on the previous outputs:

| # | Agent | Description |
|---|-------|-------------|
| 1 | **Goal** | Clarifies and structures the business goal |
| 2 | **Business DNA** | Defines core identity, values, and differentiators |
| 3 | **Research** | Market research, competitive analysis, trends |
| 4 | **Plan** | Strategic business plan with milestones |
| 5 | **Offer** | Product/service offers and pricing strategy |
| 6 | **Website** | Website structure, copy, design specs, SEO |
| 7 | **Email** | Email marketing sequences and campaigns |
| 8 | **Actions** | Concrete, prioritized action items |
| 9 | **Quality/Risk** | Quality review, risk analysis, go/no-go |
| 10 | **Execute + Work Finder** | Execution roadmap + growth opportunities |

## Quick Start

### 1. Install dependencies

```bash
pip install -e .
```

### 2. Set up environment

```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

### 3. Run the server

```bash
python -m src.main
```

The API will be available at `http://localhost:8000`.

### 4. Use the API

**Start a full pipeline run (synchronous):**

```bash
curl -X POST http://localhost:8000/api/run/sync \
  -H "Content-Type: application/json" \
  -d '{"goal": "Create a SaaS platform for small business accounting"}'
```

**Start a background pipeline run:**

```bash
curl -X POST http://localhost:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{"goal": "Launch an online fitness coaching business"}'
```

**Check run status:**

```bash
curl http://localhost:8000/api/run/{run_id}
```

**List all agents:**

```bash
curl http://localhost:8000/api/agents
```

## API Docs

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Architecture

```
src/
├── main.py              # FastAPI application entry point
├── api/
│   └── routes.py        # API endpoints
├── core/
│   ├── base_agent.py    # Abstract base agent class
│   ├── config.py        # Configuration (env vars)
│   ├── llm.py           # Anthropic Claude client
│   ├── models.py        # Pydantic data models
│   └── pipeline.py      # Pipeline orchestrator
└── agents/
    ├── goal.py           # Goal Agent
    ├── business_dna.py   # Business DNA Agent
    ├── research.py       # Research Agent
    ├── plan.py           # Plan Agent
    ├── offer.py          # Offer Agent
    ├── website.py        # Website Agent
    ├── email_campaign.py # Email Campaign Agent
    ├── actions.py        # Actions Agent
    ├── quality_risk.py   # Quality/Risk Agent
    └── execute.py        # Execute + Work Finder Agent
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key (required) | - |
| `ANTHROPIC_MODEL` | Claude model to use | `claude-sonnet-4-20250514` |
| `MAX_TOKENS` | Max tokens per LLM call | `4096` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
