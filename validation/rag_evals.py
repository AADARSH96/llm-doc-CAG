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
    question_indices = []

    # Determine number of unique questions from ground truth keys (assumed continuous from 0)
    try:
        num_questions = len(ground_truths)
    except:
        num_questions = 4  # default fallback, adjust if needed

    for global_i, item in enumerate(data):
        question_idx = global_i % num_questions
        ref = ground_truths.get(str(question_idx)) if ground_truths else None

        samples.append(
            SingleTurnSample(
                user_input=item["question"],
                retrieved_contexts=[item["prompt"]],
                response=item[model_key],
                reference=ref
            )
        )
        modes.append(item.get("mode", "unknown"))
        question_indices.append(question_idx)

    return samples, modes, question_indices

def save_scores_to_csv(scores, model_name, modes, question_indices, filename="validation/evaluation_metrics.csv"):
    if hasattr(scores, "to_pandas"):  # New Ragas EvaluationResult object
        df = scores.to_pandas()
    else:
        df = pd.DataFrame(scores)

    df.insert(0, "model", model_name)
    df.insert(1, "sample_index", question_indices)  # Assign correct question indices repeated per prompt mode
    df.insert(2, "prompt_mode", modes)

    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        existing_df = pd.read_csv(filename)
        df = pd.concat([existing_df, df], ignore_index=True)

    df.to_csv(filename, index=False)
    print(f"✅ Saved evaluation metrics for {model_name} to {filename}")

def main():
    data = load_data()
    ground_truths = load_ground_truth()

    # Only run all metrics if ground truth references exist and are non-empty for *all* question indices
    if ground_truths and all(ground_truths.get(str(i)) for i in range(len(ground_truths))):
        metrics = [faithfulness, context_recall, answer_correctness]
        print("📏 Full metric set: faithfulness, context_recall, answer_correctness")
    else:
        metrics = [faithfulness]
        print("📏 Limited metric set: faithfulness only (missing or incomplete ground truths)")

    csv_file = "validation/evaluation_metrics.csv"
    # Clear previous CSV to avoid duplication
    with open(csv_file, "w") as f:
        f.write("")

    for model_key in ["chatgpt_answer", "claude_answer"]:
        print(f"\n🔍 Evaluating model: {model_key}")
        samples, modes, question_indices = build_samples_and_modes(data, model_key, ground_truths)
        dataset = EvaluationDataset(samples)
        scores = evaluate(dataset=dataset, metrics=metrics)
        save_scores_to_csv(scores, model_key, modes, question_indices, csv_file)

if __name__ == "__main__":
    main()
