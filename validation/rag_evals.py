import json
import os
import pandas as pd
from ragas import SingleTurnSample, EvaluationDataset
from ragas.metrics import faithfulness, context_recall, answer_correctness
from ragas.evaluation import evaluate

def load_data(path="validation/model_outputs.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def load_ground_truth(path="data/ground_truth.json"):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) and data else {}
    except FileNotFoundError:
        print("⚠️ No ground_truth.json found — skipping reference-based metrics.")
        return {}

def build_samples_and_modes(data, model_key, ground_truths):
    samples = []
    modes = []
    for i, item in enumerate(data):
        ref = ground_truths.get(str(i)) if ground_truths else None
        samples.append(
            SingleTurnSample(
                user_input=item["question"],
                retrieved_contexts=[item["prompt"]],
                response=item[model_key],
                reference=ref
            )
        )
        modes.append(item.get("mode", "unknown"))
    return samples, modes

def save_scores_to_csv(scores, model_name, modes, filename="validation/evaluation_metrics.csv"):
    if hasattr(scores, "to_pandas"):  # New Ragas result object
        df = scores.to_pandas()
    else:
        df = pd.DataFrame(scores)

    df.insert(0, "model", model_name)
    df.insert(1, "sample_index", range(len(df)))
    df.insert(2, "prompt_mode", modes)

    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        existing_df = pd.read_csv(filename)
        df = pd.concat([existing_df, df], ignore_index=True)

    df.to_csv(filename, index=False)
    print(f"✅ Saved evaluation metrics for {model_name} to {filename}")

def main():
    data = load_data()
    ground_truths = load_ground_truth()

    # Require complete references for context_recall / answer_correctness
    if ground_truths and all(ground_truths.get(str(i)) for i in range(len(data))):
        metrics = [faithfulness, context_recall, answer_correctness]
        print("📏 Full metric set: faithfulness, context_recall, answer_correctness")
    else:
        metrics = [faithfulness]
        print("📏 Limited metric set: faithfulness only")

    csv_file = "validation/evaluation_metrics.csv"
    with open(csv_file, "w") as f:
        f.write("")

    for model_key in ["chatgpt_answer", "claude_answer"]:
        print(f"\n🔍 Evaluating model: {model_key}")
        samples, modes = build_samples_and_modes(data, model_key, ground_truths)
        dataset = EvaluationDataset(samples)
        scores = evaluate(dataset=dataset, metrics=metrics)
        save_scores_to_csv(scores, model_key, modes, csv_file)

if __name__ == "__main__":
    main()
