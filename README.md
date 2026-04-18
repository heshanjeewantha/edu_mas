# EduMAS — Educational Multi-Agent System
**SE4010 CTSE · Assignment 2 · Group Project**

A locally-hosted Multi-Agent System (MAS) that automates an end-to-end educational quiz pipeline using **CrewAI** + **Ollama (llama3:8b)**. Zero cloud costs, zero paid APIs.

---

## System Architecture

```
Student Input (Topic + Difficulty)
          ↓
  [Coordinator Agent]       → Tool: wikipedia_topic_fetcher (free Wikipedia API)
          ↓  [topic_summary passed via context]
  [Quiz Generator Agent]    → Tool: save_quiz_to_file (writes output/quiz.json)
          ↓  [quiz_file_path passed via context]
  [Grader Agent]            → Tool: score_student_answers (reads quiz, scores answers)
          ↓  [scores passed via context]
  [Report Writer Agent]     → Tool: write_final_report (writes output/report_*.json)
```

---

## Team Contributions

| Student | Agent | Tool | Test File |
|---------|-------|------|-----------|
| Student A | `coordinator.py` | `api_tool.py` (Wikipedia) | `test_coordinator.py` |
| Student B | `quiz_generator.py` | `file_tools.py` (Save Quiz) | `test_quiz_generator.py` |
| Student C | `grader.py` | `scoring_tool.py` (Scorer) | `test_grader.py` |
| Student D | `report_writer.py` | `report_tool.py` (Report) | `test_report_writer.py` |

---

## Setup & Run

### 1. Install Ollama
Download from https://ollama.com and install for your OS.

### 2. Pull the model
```bash
ollama pull llama3:8b
```

### 3. Install Python dependencies
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run Ollama server (in a separate terminal)
```bash
ollama serve
```

### 5. Run the pipeline
```bash
python main.py
```

### 6. Run tests
```bash
pytest tests/ -v
```

---

## Project Structure

```
edu_mas/
├── main.py                    # Entry point — runs the full pipeline
├── state.py                   # Global shared state dataclass
├── logger.py                  # LLMOps / AgentOps observability module
├── requirements.txt
├── agents/
│   ├── coordinator.py         # Agent 1 (Student A)
│   ├── quiz_generator.py      # Agent 2 (Student B)
│   ├── grader.py              # Agent 3 (Student C)
│   └── report_writer.py       # Agent 4 (Student D)
├── tools/
│   ├── api_tool.py            # Wikipedia fetcher (Student A)
│   ├── file_tools.py          # Quiz file writer (Student B)
│   ├── scoring_tool.py        # Answer scorer (Student C)
│   └── report_tool.py         # Report compiler (Student D)
├── tests/
│   ├── test_coordinator.py    # 12 tests — WikipediaTool
│   ├── test_quiz_generator.py # 12 tests — SaveQuizTool
│   ├── test_grader.py         # 15 tests — AnswerScoringTool
│   └── test_report_writer.py  # 15 tests — WriteReportTool
├── frontend/
│   └── src/App.jsx            # React dashboard
├── logs/
│   └── agent_trace.log        # Auto-generated observability log
└── output/
    ├── quiz.json              # Generated quiz questions
    └── report_*.json          # Timestamped graded reports
```

---

## Architectural Components

### 1. Multi-Agent Orchestration
Four distinct agents in a sequential pipeline managed by CrewAI. Each agent has a unique `role`, `goal`, `backstory`, and `allow_delegation=False` to prevent scope creep.

### 2. Tool Usage
Every agent uses exactly one custom Python tool that interacts with the real world:
- **WikipediaTool** — calls the free Wikipedia public API
- **SaveQuizTool** — writes JSON to local filesystem
- **AnswerScoringTool** — reads a JSON file and performs scoring logic
- **WriteReportTool** — compiles and writes a structured JSON report

### 3. State Management
State is passed via CrewAI's `context=[task]` chaining, ensuring each agent receives the output of its predecessor. The `EduMASState` dataclass in `state.py` tracks the full pipeline state including a `pipeline_log` list for audit purposes.

### 4. LLMOps / AgentOps Observability
`logger.py` provides structured logging with 6 dedicated functions:
- `log_pipeline_start/end` — pipeline lifecycle
- `log_agent_start/end` — agent I/O
- `log_tool_call/result` — every tool invocation and its result
- `log_state_transition` — data flowing between agents
- `crewai_step_callback` — hooked into CrewAI's `step_callback` for automatic step tracing

All logs are written to both stdout and `logs/agent_trace.log`.
