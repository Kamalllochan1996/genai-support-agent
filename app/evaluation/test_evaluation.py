import json
from datetime import datetime
from pathlib import Path

from app.evaluation.test_dataset import evaluation_dataset
from app.evaluation.rag_metrics import evaluate_rag

from app.langchain.rag_chain import (
    retrieve_documents,
    run_rag_with_documents,
    format_documents
)


# ============================================================
# Evaluation Configuration
# ============================================================

EVALUATION_THRESHOLD = 0.90

RESULT_FILE = Path("evaluation_results.json")

HISTORY_FILE = Path("evaluation_history.json")

BASELINE_FILE = Path("evaluation_baseline.json")


# ============================================================
# Source Evaluation
# ============================================================

def evaluate_source(actual_sources, expected_source):
    """
    Check whether the expected source was retrieved.
    """

    if expected_source is None:
        return len(actual_sources) == 0

    actual_source_names = [
        source["source"]
        for source in actual_sources
    ]

    return expected_source in actual_source_names


# ============================================================
# Run Evaluation
# ============================================================

def run_evaluation():

    results = []

    for index, item in enumerate(
        evaluation_dataset,
        start=1
    ):

        question = item["question"]

        expected_answer = item["expected_answer"]

        expected_source = item["expected_source"]

        print("\n" + "=" * 80)

        print(f"Test Case: {index}")

        print("\nQuestion:")
        print(question)

        # ==================================================
        # 1. Retrieve documents
        # ==================================================

        documents = retrieve_documents(question)

        # ==================================================
        # 2. Create context
        # ==================================================

        context = format_documents(documents)

        # ==================================================
        # 3. Generate answer
        # ==================================================

        rag_result = run_rag_with_documents(
            question,
            documents
        )

        actual_answer = rag_result["answer"]

        actual_sources = rag_result["sources"]

        # ==================================================
        # 4. Evaluate RAG metrics
        # ==================================================

        metrics = evaluate_rag(
            question=question,
            context=context,
            expected_answer=expected_answer,
            actual_answer=actual_answer
        )

        # ==================================================
        # 5. Evaluate source
        # ==================================================

        source_pass = evaluate_source(
            actual_sources,
            expected_source
        )

        # ==================================================
        # 6. Print answers
        # ==================================================

        print("\nExpected Answer:")
        print(expected_answer)

        print("\nActual Answer:")
        print(actual_answer)

        print("\nExpected Source:")
        print(expected_source)

        print("\nActual Sources:")
        print(actual_sources)

        # ==================================================
        # 7. Print metrics
        # ==================================================

        print("\nRAG Metrics:")

        print(
            "Context Relevance :",
            "PASS"
            if metrics["context_relevance"]
            else "FAIL"
        )

        print(
            "Faithfulness      :",
            "PASS"
            if metrics["faithfulness"]
            else "FAIL"
        )

        print(
            "Answer Relevance  :",
            "PASS"
            if metrics["answer_relevance"]
            else "FAIL"
        )

        print(
            "Answer Correctness:",
            "PASS"
            if metrics["answer_correctness"]
            else "FAIL"
        )

        print(
            "Source Check      :",
            "PASS"
            if source_pass
            else "FAIL"
        )

        print(
            "\nRAG Score:",
            f"{metrics['score'] * 100:.2f}%"
        )

        # ==================================================
        # 8. Store result
        # ==================================================

        results.append({
            "test_case": index,
            "question": question,
            "expected_answer": expected_answer,
            "actual_answer": actual_answer,
            "expected_source": expected_source,
            "actual_sources": actual_sources,
            "context_relevance": metrics["context_relevance"],
            "faithfulness": metrics["faithfulness"],
            "answer_relevance": metrics["answer_relevance"],
            "answer_correctness": metrics["answer_correctness"],
            "source_pass": source_pass,
            "score": metrics["score"]
        })

    return results


# ============================================================
# Save Latest Results
# ============================================================

def save_results(
    results,
    average_score,
    evaluation_passed
):
    """
    Save the latest evaluation results.
    """

    output = {
        "evaluation_threshold": EVALUATION_THRESHOLD,
        "average_score": average_score,
        "overall_evaluation": (
            "PASS"
            if evaluation_passed
            else "FAIL"
        ),
        "results": results
    }

    with open(
        RESULT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# Load Evaluation History
# ============================================================

def load_history():
    """
    Load previous evaluation runs.
    """

    if not HISTORY_FILE.exists():
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            history = json.load(file)

            if isinstance(history, list):
                return history

            return []

    except json.JSONDecodeError:

        return []


# ============================================================
# Load Baseline
# ============================================================

def load_baseline(history):
    """
    Load the fixed baseline.

    If a baseline does not exist yet, use the first
    evaluation run from history as the baseline.

    If there is no history, the current run will become
    the baseline.
    """

    # --------------------------------------------------------
    # Existing baseline
    # --------------------------------------------------------

    if BASELINE_FILE.exists():

        try:

            with open(
                BASELINE_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                baseline = json.load(file)

                return baseline

        except json.JSONDecodeError:

            pass

    # --------------------------------------------------------
    # Existing history
    # --------------------------------------------------------

    if history:

        first_run = history[0]

        baseline = {
            "baseline_run_id":
                first_run.get("run_id", 1),

            "baseline_timestamp":
                first_run.get("timestamp"),

            "baseline_score":
                first_run.get("average_score", 0)
        }

        save_baseline(baseline)

        return baseline

    # --------------------------------------------------------
    # No baseline yet
    # --------------------------------------------------------

    return None


# ============================================================
# Save Baseline
# ============================================================

def save_baseline(baseline):
    """
    Save the fixed baseline.
    """

    with open(
        BASELINE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            baseline,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# Create Baseline From Current Run
# ============================================================

def create_baseline_from_current_run(
    run_id,
    timestamp,
    average_score
):
    """
    Create the initial baseline.
    """

    baseline = {
        "baseline_run_id": run_id,

        "baseline_timestamp": timestamp,

        "baseline_score": average_score
    }

    save_baseline(baseline)

    return baseline


# ============================================================
# Save Evaluation History
# ============================================================

def save_history(
    history,
    results,
    average_score,
    evaluation_passed
):
    """
    Append the current evaluation run to history.
    """

    current_run = {
        "run_id": len(history) + 1,

        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),

        "evaluation_threshold":
            EVALUATION_THRESHOLD,

        "average_score":
            average_score,

        "overall_evaluation":
            (
                "PASS"
                if evaluation_passed
                else "FAIL"
            ),

        "results":
            results
    }

    history.append(current_run)

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )

    return current_run


# ============================================================
# Compare With Previous Run
# ============================================================

def compare_with_previous_run(
    history,
    current_score
):
    """
    Compare current score with the previous run.
    """

    if len(history) < 1:

        return {
            "has_previous_run": False,
            "previous_score": None,
            "current_score": current_score,
            "change": None,
            "status": "FIRST_RUN"
        }

    previous_run = history[-1]

    previous_score = previous_run.get(
        "average_score",
        0
    )

    change = current_score - previous_score

    if change > 0:

        status = "IMPROVED"

    elif change < 0:

        status = "DEGRADED"

    else:

        status = "UNCHANGED"

    return {
        "has_previous_run": True,
        "previous_score": previous_score,
        "current_score": current_score,
        "change": change,
        "status": status
    }


# ============================================================
# Compare With Baseline
# ============================================================

def compare_with_baseline(
    baseline,
    current_score
):
    """
    Compare current score with the fixed baseline.
    """

    if baseline is None:

        return {
            "has_baseline": False,
            "baseline_score": None,
            "current_score": current_score,
            "change": None,
            "status": "NO_BASELINE"
        }

    baseline_score = baseline.get(
        "baseline_score",
        0
    )

    change = current_score - baseline_score

    if change > 0:

        status = "ABOVE_BASELINE"

    elif change < 0:

        status = "BELOW_BASELINE"

    else:

        status = "AT_BASELINE"

    return {
        "has_baseline": True,
        "baseline_score": baseline_score,
        "current_score": current_score,
        "change": change,
        "status": status
    }


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    # ======================================================
    # Load history BEFORE adding current run
    # ======================================================

    history = load_history()

    # ======================================================
    # Load existing baseline
    # ======================================================

    baseline = load_baseline(history)

    # ======================================================
    # Run evaluation
    # ======================================================

    results = run_evaluation()

    # ======================================================
    # Calculate Summary
    # ======================================================

    total = len(results)

    context_passed = sum(
        result["context_relevance"]
        for result in results
    )

    faithfulness_passed = sum(
        result["faithfulness"]
        for result in results
    )

    answer_relevance_passed = sum(
        result["answer_relevance"]
        for result in results
    )

    answer_correctness_passed = sum(
        result["answer_correctness"]
        for result in results
    )

    source_passed = sum(
        result["source_pass"]
        for result in results
    )

    # ======================================================
    # Calculate Average Score
    # ======================================================

    average_score = (
        sum(
            result["score"]
            for result in results
        ) / total
        if total > 0
        else 0
    )

    # ======================================================
    # Create baseline if this is the first run
    # ======================================================

    if baseline is None:

        baseline = create_baseline_from_current_run(
            run_id=len(history) + 1,
            timestamp=datetime.now().isoformat(
                timespec="seconds"
            ),
            average_score=average_score
        )

    # ======================================================
    # Threshold Check
    # ======================================================

    evaluation_passed = (
        average_score >= EVALUATION_THRESHOLD
    )

    # ======================================================
    # Compare With Previous Run
    # ======================================================

    previous_comparison = compare_with_previous_run(
        history=history,
        current_score=average_score
    )

    # ======================================================
    # Compare With Baseline
    # ======================================================

    baseline_comparison = compare_with_baseline(
        baseline=baseline,
        current_score=average_score
    )

    # ======================================================
    # Save Latest Results
    # ======================================================

    save_results(
        results=results,
        average_score=average_score,
        evaluation_passed=evaluation_passed
    )

    # ======================================================
    # Save History
    # ======================================================

    save_history(
        history=history,
        results=results,
        average_score=average_score,
        evaluation_passed=evaluation_passed
    )

    # ======================================================
    # Final Report
    # ======================================================

    print("\n\n" + "=" * 80)

    print("FINAL RAG EVALUATION REPORT")

    print("=" * 80)

    print(
        f"\nTotal Questions       : {total}"
    )

    print(
        f"Context Relevance     : "
        f"{context_passed}/{total}"
    )

    print(
        f"Faithfulness          : "
        f"{faithfulness_passed}/{total}"
    )

    print(
        f"Answer Relevance      : "
        f"{answer_relevance_passed}/{total}"
    )

    print(
        f"Answer Correctness    : "
        f"{answer_correctness_passed}/{total}"
    )

    print(
        f"Source Check          : "
        f"{source_passed}/{total}"
    )

    print(
        f"\nAverage RAG Score     : "
        f"{average_score * 100:.2f}%"
    )

    print(
        f"Evaluation Threshold  : "
        f"{EVALUATION_THRESHOLD * 100:.2f}%"
    )

    print(
        "\nOverall Evaluation    : "
        + (
            "PASS"
            if evaluation_passed
            else "FAIL"
        )
    )

    # ======================================================
    # Previous Run Comparison
    # ======================================================

    print("\n" + "-" * 80)

    print("PREVIOUS RUN COMPARISON")

    print("-" * 80)

    if previous_comparison["has_previous_run"]:

        previous_score = (
            previous_comparison["previous_score"]
        )

        change = (
            previous_comparison["change"]
        )

        print(
            f"\nPrevious Score        : "
            f"{previous_score * 100:.2f}%"
        )

        print(
            f"Current Score         : "
            f"{average_score * 100:.2f}%"
        )

        print(
            f"Score Change          : "
            f"{change * 100:+.2f}%"
        )

        print(
            f"Status                : "
            f"{previous_comparison['status']}"
        )

    else:

        print(
            "\nPrevious Score        : N/A"
        )

        print(
            f"Current Score         : "
            f"{average_score * 100:.2f}%"
        )

        print(
            "Status                : FIRST_RUN"
        )

    # ======================================================
    # Baseline Comparison
    # ======================================================

    print("\n" + "-" * 80)

    print("BASELINE COMPARISON")

    print("-" * 80)

    if baseline_comparison["has_baseline"]:

        baseline_score = (
            baseline_comparison["baseline_score"]
        )

        baseline_change = (
            baseline_comparison["change"]
        )

        print(
            f"\nBaseline Score        : "
            f"{baseline_score * 100:.2f}%"
        )

        print(
            f"Current Score         : "
            f"{average_score * 100:.2f}%"
        )

        print(
            f"Change vs Baseline    : "
            f"{baseline_change * 100:+.2f}%"
        )

        print(
            f"Baseline Status       : "
            f"{baseline_comparison['status']}"
        )

        print(
            f"Baseline Run ID       : "
            f"{baseline.get('baseline_run_id')}"
        )

    else:

        print(
            "\nBaseline Score        : N/A"
        )

    # ======================================================
    # File Information
    # ======================================================

    print("\n" + "-" * 80)

    print(
        f"\nLatest results saved  : "
        f"{RESULT_FILE}"
    )

    print(
        f"History saved         : "
        f"{HISTORY_FILE}"
    )

    print(
        f"Baseline saved        : "
        f"{BASELINE_FILE}"
    )

    print("=" * 80)

    # ======================================================
    # Regression Test / Quality Gate
    # ======================================================

    if not evaluation_passed:

        raise SystemExit(
            "\nRAG regression test FAILED. "
            "The average score is below the required threshold."
        )

    print(
        "\nRAG regression test PASSED."
    )