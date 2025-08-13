def explicit_instruction_prompt(cache, question):
    system = (
        "You are an assistant. Answer ONLY using information in the 'Knowledge Cache' below. "
        "Do NOT use outside knowledge. If you can't find the answer, reply: 'Not found in cache.'"
    )
    prompt = f"{system}\n\n[Knowledge Cache Start]\n{cache}\n[Knowledge Cache End]\n\nUSER: {question}\n"
    return {"system": system, "prompt": prompt, "question": question}

def separator_format_prompt(cache, question):
    prompt = (
        "[CACHE]\n" + cache + "\n[/CACHE]\n" + "Question: " + question + "\nAnswer:"
    )
    return {"prompt": prompt}

def bullet_point_prompt(cache, question):
    system = (
        "Respond ONLY using facts from the Knowledge Cache. Present your answer as bullet points."
    )
    prompt = f"{system}\n\n[Knowledge Cache]\n{cache}\n\nQuestion: {question}\nAnswer (bullets):"
    return {"system": system, "prompt": prompt}

def fewshot_prompt(cache, question):
    example = (
        "Q: What is CAG?\nA: CAG is a technique where all required reference data is preloaded into a language model’s context window, removing the need for retrieval at inference time.\n"
        "Q: [Your Question]\nA:"
    )
    prompt = f"{cache}\n\n{example.replace('[Your Question]', question)}"
    return {"prompt": prompt}

def zero_shot_prompt(cache, question):
    system = (
        "Only answer the question using the knowledge provided in the cache below."
    )
    prompt = f"{system}\n\n[Knowledge Cache]\n{cache}\n\nQuestion: {question}\nAnswer:"
    return {"system": system, "prompt": prompt}

def chain_of_thought_prompt(cache, question):
    system = (
        "Only answer using the cache below. Show your answer as logical steps, using only cache facts."
    )
    prompt = (
        f"{system}\n\n[Knowledge Cache]\n{cache}\n\n"
        f"Question: {question}\nAnswer (step by step):"
    )
    return {"system": system, "prompt": prompt}

PROMPT_TEMPLATES = {
    "explicit_instruction": explicit_instruction_prompt,
    "separator_format": separator_format_prompt,
    "bullet_point": bullet_point_prompt,
    "fewshot": fewshot_prompt,
    "zero_shot": zero_shot_prompt,
    "chain_of_thought": chain_of_thought_prompt,
}
