import json
import subprocess
import argparse
from pathlib import Path

MAP_FILE = Path("vector_stores.json")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", default="sample_questions.json")
    parser.add_argument("--survey-name", default="demo_survey")

    args = parser.parse_args()

    if not MAP_FILE.exists():
        raise FileNotFoundError("vector_stores.json not found. Run upload_docs.py first.")

    with open(MAP_FILE, "r", encoding="utf-8") as f:
        store_map = json.load(f)

    for collection in store_map:
        print("\n====================")
        print("Running:", collection)
        print("====================\n")

        cmd = [
            "python3",
            "ask.py",
            "--collection",
            collection,
            "--questions",
            args.questions,
            "--survey-name",
            args.survey_name,
        ]

        result = subprocess.run(cmd)

        if result.returncode != 0:
            print(f"\nStopped because ask.py failed for: {collection}")
            break


if __name__ == "__main__":
    main()