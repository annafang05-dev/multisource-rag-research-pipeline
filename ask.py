import os
import json
import csv
import re
import time
import argparse
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

MAP_FILE = Path("vector_stores.json")
OUTPUT_DIR = Path("results")
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def load_store_map():
    with open(MAP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_questions(questions_path: Path):
    with open(questions_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_number(text: str) -> str:
    match = re.search(r"-?\d+(\.\d+)?", text.strip())
    return match.group(0) if match else ""


def build_prompt(collection: str, question: str, coding: str) -> str:
    return (
        f"You are answering based only on the uploaded documents for {collection}. "
        "Use only retrieved source material. "
        "Return only a single numerical value and nothing else.\n\n"
        f"Question:\n{question}\n\n"
        f"Response coding:\n{coding}"
    )


def ask_model(vector_store_id: str, prompt: str) -> str:
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [vector_store_id],
            }
        ],
    )
    return response.output_text.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection", required=True, help='Example: "sample_author"')
    parser.add_argument("--questions", default="sample_questions.json")
    parser.add_argument("--survey-name", default="demo_survey")

    args = parser.parse_args()

    OUTPUT_DIR.mkdir(exist_ok=True)

    questions_path = Path(args.questions)
    if not questions_path.exists():
        raise FileNotFoundError(f"Questions file not found: {questions_path}")

    store_map = load_store_map()
    questions = load_questions(questions_path)

    if args.collection not in store_map:
        raise KeyError(f"Collection '{args.collection}' not found in vector_stores.json")

    vector_store_id = store_map[args.collection]

    safe_collection = args.collection.replace(" ", "_")
    safe_model = MODEL_NAME.replace(".", "_")
    safe_survey = args.survey_name.replace(" ", "_")

    output_file = OUTPUT_DIR / f"{safe_survey}_{safe_collection}_{safe_model}.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "survey",
            "collection",
            "model",
            "question_id",
            "variable",
            "scale_type",
            "question",
            "coding",
            "raw_response",
            "numeric_response",
        ])

        for q in questions:
            prompt = build_prompt(
                args.collection,
                q["question"],
                q["coding"],
            )

            raw_answer = ask_model(vector_store_id, prompt)
            numeric_answer = extract_number(raw_answer)

            writer.writerow([
                args.survey_name,
                args.collection,
                MODEL_NAME,
                q["id"],
                q.get("variable", ""),
                q.get("scale_type", ""),
                q["question"],
                q["coding"],
                raw_answer,
                numeric_answer,
            ])

            print(
                f"qid={q['id']} raw={raw_answer!r} numeric={numeric_answer!r}"
            )

            time.sleep(0.4)

    print(f"\nSaved → {output_file}")


if __name__ == "__main__":
    main()