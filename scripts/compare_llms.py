import os
import json
from openai import OpenAI
import time

client = OpenAI(api_key='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')
import anthropic
from prompts import PROMPT_TEMPLATES

 #os.environ.get("OPENAI_API_KEY")
claude_client =  anthropic.Anthropic(api_key='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')


def load_cache(path="data/cache_knowledge.txt"):
    with open(path, encoding="utf-8") as f:
        return f.read().strip()

def run_chatgpt(prompt_dict):
    if "system" in prompt_dict:
        messages = [
            {"role": "system", "content": prompt_dict["system"]},
            {"role": "user", "content": prompt_dict["prompt"]}
        ]
    else:
        messages = [{"role": "user", "content": prompt_dict["prompt"]}]
    response = client.chat.completions.create(model="gpt-5", messages=messages, max_completion_tokens=256)
    time.sleep(30)
    return response.choices[0].message.content.strip()

def run_claude(prompt_dict):
    # The actual cache+question combined by your prompt template
    prompt_body = prompt_dict.get("prompt", "")

    # Messages API call (Claude 4 compatible)
    message = claude_client.messages.create(
        model="claude-sonnet-4-20250514",  # or another Claude 3.5/4 model
        max_tokens=256,
        temperature=0,
        system="You are an assistant. Only answer using the provided cache/context.",
        messages=[
            {"role": "user", "content": prompt_body}
        ]
    )

    # Combine any text segments into one string
    return "".join(block.text for block in message.content if block.type == "text").strip()


def main():
    cache = load_cache()
    questions = [
        "What is Cache-Augmented Generation (CAG)?",
        "How is CAG different from RAG?",
        "When should I use CAG?",
        "What should the model reply if answer isn't in cache?"
    ]

    print("Running all prompt engineering techniques automatically:\n")

    all_results = []

    for mode in PROMPT_TEMPLATES.keys():
        print(f"\n=== Prompt Engineering Technique: {mode} ===")
        prompt_func = PROMPT_TEMPLATES[mode]

        for question in questions:
            prompt_dict = prompt_func(cache, question)
            print(f"\nQuestion: {question}\n---")

            try:
                chatgpt_answer = run_chatgpt(prompt_dict)
                print("ChatGPT answer:\n", chatgpt_answer)
            except Exception as e:
                chatgpt_answer = f"Error: {e}"
                print(chatgpt_answer)

            try:
                claude_answer = run_claude(prompt_dict)
                print("Claude answer:\n", claude_answer)
            except Exception as e:
                claude_answer = f"Error: {e}"
                print(claude_answer)

            all_results.append({
                "question": question,
                "chatgpt_answer": chatgpt_answer,
                "claude_answer": claude_answer,
                "prompt": prompt_dict.get("prompt") or "",
                "mode": mode,
            })

    os.makedirs("validation", exist_ok=True)
    with open("validation/model_outputs.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print("\nSaved all outputs to validation/model_outputs.json")

if __name__ == "__main__":
    main()
