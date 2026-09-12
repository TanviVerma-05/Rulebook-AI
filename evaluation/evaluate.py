import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_FILE = ROOT / "evaluation" / "unanswerable_questions.json"
RAG_SCRIPT = ROOT / "ai_engine" / "rag.py"

if sys.platform == "win32":
    PYTHON = ROOT / "ai_engine" / "venv" / "Scripts" / "python.exe"
else:
    PYTHON = ROOT / "ai_engine" / "venv" / "bin" / "python"


def run_question(question):
    process = subprocess.run(
        [
            str(PYTHON),
            str(RAG_SCRIPT),
            "--question",
            question
        ],
        cwd=ROOT,
        capture_output=True,
        text=True
    )

    if process.returncode != 0:
        return {
            "state": "ERROR",
            "error": process.stderr
        }

    try:
        return json.loads(process.stdout)
    except json.JSONDecodeError:
        return {
            "state": "ERROR",
            "error": "Invalid JSON returned by RAG engine"
        }


def main():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    results = []
    correct = 0

    print("\nRulebook AI - Unanswerable Question Evaluation")
    print("=" * 55)

    for item in questions:
        question = item["question"]

        print(f"\n[{item['id']:02d}] {question}")

        result = run_question(question)
        state = result.get("state", "ERROR")

        is_correct = state == "NO_EVIDENCE"

        if is_correct:
            correct += 1

        print(f"     Expected: NO_EVIDENCE")
        print(f"     Got:      {state}")
        print(f"     Result:   {'PASS' if is_correct else 'FAIL'}")

        results.append({
            "id": item["id"],
            "question": question,
            "expected_state": "NO_EVIDENCE",
            "actual_state": state,
            "correct": is_correct
        })

    total = len(questions)
    accuracy = (correct / total) * 100 if total else 0

    print("\n" + "=" * 55)
    print("EVALUATION SUMMARY")
    print("=" * 55)
    print(f"Total questions:       {total}")
    print(f"Correctly refused:     {correct}")
    print(f"Incorrect responses:   {total - correct}")
    print(f"Refusal accuracy:      {accuracy:.2f}%")

    output_file = ROOT / "evaluation" / "evaluation_results.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            {
                "total_questions": total,
                "correctly_refused": correct,
                "incorrect_responses": total - correct,
                "refusal_accuracy_percent": round(accuracy, 2),
                "results": results
            },
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"\nDetailed results saved to:")
    print(output_file)


if __name__ == "__main__":
    main()
