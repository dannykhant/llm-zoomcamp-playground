import time
import json
from openai import OpenAI

from app.ingest import ingest_data


client = OpenAI()
index = ingest_data("data.csv")


def search(query):
    boost = {
        "body_part": 1.3617719252298475,
        "exercise_name": 2.747748020851861,
        "instructions": 1.6961000266977542,
        "muscle_groups_activated": 0.5307260562229762,
        "type": 2.290634544364637,
        "type_of_activity": 2.8558751878100637,
        "type_of_equipment": 2.651131478469881,
    }

    results = index.search(query=query, filter_dict={}, boost_dict=boost, num_results=5)
    return results


def build_prompt(query, search_results):
    prompt_template = """
You're an expert fitness instructor. Answer the QUESTION based on the CONTEXT from our exercises database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()

    context_template = """
exercise_name: {exercise_name}
type_of_activity: {type_of_activity}
type_of_equipment: {type_of_equipment}
body_part: {body_part}
type: {type}
muscle_groups_activated: {muscle_groups_activated}
instructions: {instructions}
"""

    context = ""
    for doc in search_results:
        context += context_template.format(**doc) + "\n\n"

    prompt = prompt_template.format(question=query, context=context)
    return prompt


def llm(prompt, model="gpt-5-nano"):
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content

    token_stats = {}
    if response.usage is not None:
        token_stats = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }

    return answer, token_stats


def evaluate_relevance(answer, query, model="gpt-5-nano"):
    eval_prompt_template = """
You are an expert evaluator for a RAG system.
Your task is to analyze the relevance of the generated answer to the given question.
Based on the relevance of the generated answer, you will classify it
as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Question: {question}
Generated Answer: {answer_llm}

Please analyze the content and context of the generated answer in relation to the question
and provide your evaluation in parsable JSON. Don't use code blocks.

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()

    prompt = eval_prompt_template.format(question=query, answer_llm=answer)
    evaluation, token_stats = llm(prompt=prompt, model=model)

    try:
        evaluation_json = (
            json.loads(evaluation)
            if evaluation
            else {
                "Relevance": "ERROR",
                "Explanation": "No response from LLM evaluation.",
            }
        )
    except json.JSONDecodeError:
        evaluation_json = {
            "Relevance": "ERROR",
            "Explanation": "Failed to parse LLM evaluation response as JSON.",
        }

    return evaluation_json, token_stats


def calculate_openai_cost(token_stats, model="gpt-5-nano"):
    model_pricing = {
        "gpt-5-nano": {"prompt": 0.0001, "completion": 0.0002},  # per 1K tokens
    }

    if model not in model_pricing:
        return 0.0

    pricing = model_pricing[model]
    prompt_cost = (token_stats.get("prompt_tokens", 0) / 1000) * pricing["prompt"]
    completion_cost = (token_stats.get("completion_tokens", 0) / 1000) * pricing[
        "completion"
    ]

    total_cost = prompt_cost + completion_cost
    return total_cost


def rag(query, model="gpt-5-nano"):
    start = time.time()

    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer, answer_tokens = llm(prompt, model=model)
    evaluation, eval_tokens = evaluate_relevance(answer, query, model=model)

    end = time.time()
    time_taken = end - start

    answer_cost = calculate_openai_cost(answer_tokens, model=model)
    eval_cost = calculate_openai_cost(eval_tokens, model=model)
    total_cost = answer_cost + eval_cost

    response = {
        "answer": answer,
        "prompt": prompt,
        "relevance_evaluation": evaluation.get("Relevance", "ERROR"),
        "evaluation_explanation": evaluation.get("Explanation", "ERROR"),
        "model": model,
        "response_time": time_taken,
        "token_usage": {
            "answer_tokens": answer_tokens,
            "eval_tokens": eval_tokens,
        },
        "cost": {
            "answer_cost": answer_cost,
            "eval_cost": eval_cost,
            "total_cost": total_cost,
        },
    }

    return response
