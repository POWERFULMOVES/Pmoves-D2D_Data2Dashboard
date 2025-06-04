# Data2Dashboard

This project contains experimental agents for turning tabular CSV data into short, high value insights and charts with the help of large language models (LLMs).  
It grew out of a collection of notebooks and now provides reusable agent code, datasets and example results.

## Repository structure

- `agents/` – implementations of different agents and utilities
  - `llm_factory.py` – create a `langchain` LLM instance for different backends (OpenAI, Ollama, LM Studio, Hugging Face, Google)
  - `d2insight_gpt4o.py` – simple GPT‑4o chain for analysing a CSV
  - `d2insight_gpt4o_domain.py` – same, but first infers the data domain
  - `d2insight_agent_sys.py` – more advanced state‑graph agent that iteratively profiles data, determines domain, extracts concepts and writes analyses
  - `insight2dashboard_tot.py` – experimental Tree‑of‑Thought approach that generates Python plotting code based on an insight library
  - `chart_utils.py`, `ollama_thinking.py`, `utils.py` – helper utilities
- `config.py` and `config.yaml` – load configuration and choose the LLM backend via environment variables
- `dataset/` – example CSV files
- `notebooks/` – Jupyter notebooks with recorded experiment runs
- `exp_result/` – saved JSON and chart artefacts from experiments
- `requirements.txt` – Python dependencies

## Installation

Create a virtual environment (Python 3.10 or later is recommended) and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Some optional packages (e.g. `google-generativeai`) may not have wheels for all Python versions.

Set your LLM credentials via environment variables or edit `config.yaml`:

```
OPENAI_API_KEY=...        # for OpenAI backend
GOOGLE_API_KEY=...        # for Google Edge / Gemini
HF_TOKEN=...              # for HuggingFace models
OLLAMA_HOST=http://...
```

You can override the backend and model with `LLM_BACKEND` and `LLM_MODEL`.

## Usage examples

Analyse a CSV with the simple GPT‑4o chain:

```python
from agents.d2insight_gpt4o import analyze_csv_with_insights
print(analyze_csv_with_insights('dataset/Finance_survey_data.csv', 'Give me a summary'))
```

Run the full domain‑aware agent:

```python
from agents.d2insight_agent_sys import run_domain_detector
result = run_domain_detector('dataset/Finance_survey_data.csv')
print(result['analysis'])
```

Generate chart code from an insight library:

```python
from agents.insight2dashboard_tot import generate_analysis
thoughts = generate_analysis('dataset/Finance_survey_data.csv', 'exp_result/exp03/analysis.json')
print(thoughts)
```

## Next steps

- Explore the notebooks in `notebooks/` to see previous experiment outputs.
- Review `TASK.md` for the adaptation plan and outstanding work.
- Consider adding automated tests and streamlining dependency management.
