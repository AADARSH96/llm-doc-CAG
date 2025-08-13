
```markdown
# Cache‑Augmented Generation (CAG) — Model Comparison and Evaluation

This project runs controlled, side‑by‑side comparisons of **OpenAI ChatGPT** and **Anthropic Claude** using **Cache‑Augmented Generation (CAG)** with multiple prompt engineering techniques.  
It evaluates their answers using **Ragas metrics** and produces visualizations to identify the most effective prompt approach.

***

## 📂 Project Structure

```

.
├── data/
│   ├── cache_knowledge.txt      \# Static knowledge cache
│   ├── ground_truth.json        \# Reference answers for evaluation metrics
│
├── scripts/
│   ├── prompts.py               \# Prompt engineering template functions
│   ├── compare_llms.py          \# Queries both models and saves outputs
│
├── validation/
│   ├── rag_evals.py             \# Evaluates results with Ragas
│   ├── plot_results.py          \# Generates charts from evaluation CSV
│
├── requirements.txt
└── README.md

```

***

## 📖 How It Works

1. **Cache Knowledge**  
   `data/cache_knowledge.txt` contains your **static reference** (the cache) that is injected into every model prompt.

2. **Prompt Engineering**  
   `scripts/prompts.py` defines multiple template styles (explicit instruction, zero‑shot, chain-of-thought, few-shot, etc.).

3. **Questioning Both Models**  
   `scripts/compare_llms.py` asks the same set of questions to **ChatGPT** and **Claude** using the same chosen prompt style.

4. **Evaluation**  
   `validation/rag_evals.py` scores answers using [Ragas](https://github.com/explodinggradients/ragas):
   - **Faithfulness** (no ground truth needed)
   - **Context Recall** (needs ground truth)
   - **Answer Correctness** (needs ground truth)

5. **Visualization**  
   `validation/plot_results.py` produces charts showing which prompt mode gave the best results for each metric.

***

## 🚀 Setup

### 1. Clone Repository

```

git clone https://github.com/yourusername/llm-doc-CAG.git
cd llm-doc-CAG

```

### 2. Create & Activate Virtual Environment

```

python -m venv venv
source venv/bin/activate   \# Mac/Linux
venv\Scripts\activate      \# Windows

```

### 3. Install Dependencies

```

pip install -r requirements.txt

```

### 4. Set API Keys

**Recommended:** use environment variables (don’t hardcode keys in code).

For Mac/Linux:

```

export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

```

For Windows PowerShell:

```

\$env:OPENAI_API_KEY="sk-..."
\$env:ANTHROPIC_API_KEY="sk-ant-..."

```

***

## 📌 Workflow

### Step 1 — Ask Questions & Save Outputs

```

python scripts/compare_llms.py

```

- Will prompt you to choose a **prompt engineering technique**.
- Saves results to `validation/model_outputs.json`.

***

### Step 2 — Evaluate Answers

Make sure `data/ground_truth.json` exists and has **complete** references (one per question) to enable all metrics.

```

python validation/rag_evals.py

```

- Produces `validation/evaluation_metrics.csv` with columns:

```

model,sample_index,prompt_mode,faithfulness,context_recall,answer_correctness

```

***

### Step 3 — Visualize Performance

```

python validation/plot_results.py

```

- Generates faceted bar charts comparing **metrics by prompt engineering technique and model**.
- Charts visually show the comparative strengths of different prompt modes.

***

## 📊 Example Chart

Each subplot shows a metric (`faithfulness`, `context_recall`, `answer_correctness`), grouped by prompt mode and model:

| Faithfulness Chart | Context Recall Chart | Answer Correctness Chart |
|--------------------|---------------------|-------------------------|

***

## 🧩 Tips & Notes

- **context_recall** & **answer_correctness** require a `reference` answer in `ground_truth.json` for *every* question.
- To add more questions, edit the questions list in `scripts/compare_llms.py` **AND** update `ground_truth.json`.
- Modify prompt styles in `scripts/prompts.py` to test additional prompt engineering techniques.
- If you hit API rate limits, adjust or increase `time.sleep()` delays in `compare_llms.py`.
- Keep your API keys secure using environment variables—not hardcoded.

***

## 📜 License

[MIT](LICENSE) — feel free to use and adapt.

***

## 🙋 Support

If you experience any issues:  
- Verify API keys are set and valid.  
- Ensure `ground_truth.json` matches your question set and is complete.  
- Check that dependencies in `requirements.txt` are installed and compatible.

***

If you want, I can also provide a tested, fixed `plot_results.py` script to generate clean visualizations matching this README workflow. Just let me know!

```

You can copy all of the above and save it as `README.md` in your project directory. This way it is plain text and fully editable.

If you want, I can also generate and send you a `.md` file content for download via another interface or help create any other project files! Just ask.

