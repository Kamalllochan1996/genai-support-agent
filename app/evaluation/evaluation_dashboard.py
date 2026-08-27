import json
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="RAG Evaluation Dashboard",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# Constants
# ============================================================

DEFAULT_THRESHOLD = 0.70

HISTORY_FILES = [
    Path("data/evaluation_history.json"),
    Path("data/evaluation_results.json"),
    Path("app/evaluation/evaluation_history.json"),
    Path("app/evaluation/evaluation_results.json"),
    Path("evaluation_history.json"),
    Path("evaluation_results.json"),
]


# ============================================================
# Helper Functions
# ============================================================

def safe_score(value):
    """Convert a score safely to a float between 0 and 1."""

    if value is None:
        return 0.0

    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0

    # Handle percentages such as 75 instead of 0.75
    if score > 1:
        score = score / 100

    return max(
        0.0,
        min(1.0, score),
    )


def percentage(value):
    """Convert a 0-1 score to percentage text."""

    return f"{safe_score(value) * 100:.2f}%"


def load_json_file(path):
    """Load JSON safely."""

    try:

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    except Exception as error:

        st.warning(
            f"Could not load {path}: {error}"
        )

        return None


def normalize_history(data):
    """
    Normalize different possible evaluation-history
    structures into a list of runs.
    """

    if data is None:
        return []

    # Already a list
    if isinstance(data, list):

        return data

    # Common wrapper formats
    if isinstance(data, dict):

        for key in [
            "history",
            "runs",
            "results",
            "evaluation_history",
            "evaluation_results",
        ]:

            value = data.get(key)

            if isinstance(value, list):

                # If this is actually a single evaluation
                # result list, wrap it as a run when needed.
                if value and isinstance(value[0], dict):

                    if any(
                        key_name in value[0]
                        for key_name in [
                            "question",
                            "score",
                            "actual_answer",
                        ]
                    ):

                        return [
                            {
                                "run_id": 1,
                                "results": value,
                            }
                        ]

                    return value

                return value

        # A single run
        if any(
            key in data
            for key in [
                "results",
                "average_score",
                "score",
            ]
        ):

            return [data]

    return []


def find_history_file():
    """Find the first available evaluation history file."""

    for path in HISTORY_FILES:

        if path.exists():

            return path

    return None


def load_history():
    """Load evaluation history."""

    history_file = find_history_file()

    if history_file is None:

        return []

    data = load_json_file(
        history_file
    )

    return normalize_history(data)


def get_run_results(run):
    """Extract individual results from a run."""

    if not isinstance(run, dict):

        return []

    results = run.get(
        "results",
        []
    )

    if isinstance(results, list):

        return results

    return []


def calculate_average_score(results):
    """Calculate average score from test results."""

    if not results:

        return 0.0

    scores = []

    for result in results:

        scores.append(
            safe_score(
                result.get(
                    "score",
                    0,
                )
            )
        )

    return sum(scores) / len(scores)


def get_run_score(run):
    """Get average score for a run."""

    if not isinstance(run, dict):

        return 0.0

    if "average_score" in run:

        return safe_score(
            run["average_score"]
        )

    if "score" in run:

        return safe_score(
            run["score"]
        )

    return calculate_average_score(
        get_run_results(run)
    )


def get_run_id(run, index):
    """Get a readable run ID."""

    if not isinstance(run, dict):

        return index + 1

    return run.get(
        "run_id",
        index + 1,
    )


def get_timestamp(run):
    """Get run timestamp."""

    if not isinstance(run, dict):

        return "Unknown"

    return run.get(
        "timestamp",
        run.get(
            "created_at",
            "Unknown",
        ),
    )


def get_current_results(history_data):
    """Return results from the latest run."""

    if not history_data:

        return []

    latest_run = history_data[-1]

    results = get_run_results(
        latest_run
    )

    return results


def metric_passed(result, metric):
    """Safely determine whether a metric passed."""

    value = result.get(
        metric,
        False,
    )

    if isinstance(value, bool):

        return value

    if isinstance(value, (int, float)):

        return value >= 0.5

    if isinstance(value, str):

        return value.lower() in {
            "true",
            "pass",
            "passed",
            "yes",
            "1",
        }

    return False


# ============================================================
# Load Data
# ============================================================

history_data = load_history()

threshold = DEFAULT_THRESHOLD

current_results = get_current_results(
    history_data
)


# ============================================================
# Header
# ============================================================

st.title(
    "📊 RAG Evaluation Dashboard"
)

st.caption(
    "Monitor retrieval quality, answer quality, "
    "evaluation trends, failures and recommendations."
)


# ============================================================
# Top Status Bar
# ============================================================

if history_data:

    latest_run = history_data[-1]

    latest_score = get_run_score(
        latest_run
    )

    latest_run_id = get_run_id(
        latest_run,
        len(history_data) - 1,
    )

    latest_timestamp = get_timestamp(
        latest_run
    )

    status_col1, status_col2, status_col3, status_col4 = (
        st.columns(4)
    )

    with status_col1:

        st.metric(
            "Latest Score",
            percentage(
                latest_score
            ),
        )

    with status_col2:

        st.metric(
            "Latest Run",
            latest_run_id,
        )

    with status_col3:

        st.metric(
            "Test Cases",
            len(current_results),
        )

    with status_col4:

        st.metric(
            "Total Runs",
            len(history_data),
        )

    st.caption(
        f"Last evaluation: {latest_timestamp}"
    )

else:

    st.info(
        "No evaluation history found yet."
    )


# ============================================================
# Threshold
# ============================================================

with st.sidebar:

    st.header("⚙️ Dashboard Settings")

    threshold = st.slider(
        "Pass Threshold",
        min_value=0.0,
        max_value=1.0,
        value=DEFAULT_THRESHOLD,
        step=0.05,
        format="%.0f%%",
    )

    st.divider()

    st.write(
        "### Dashboard Sections"
    )

    st.write(
        """
        📈 Evaluation History

        🔄 Run Comparison

        📊 Trend Analysis

        🚨 Failure Analysis

        💡 Recommendations

        🏁 Final Summary
        """
    )


# ============================================================
# No Data
# ============================================================

if not history_data:

    st.warning(
        "No evaluation runs are available."
    )

    st.info(
        "Run the evaluation first and refresh this dashboard."
    )

    st.stop()


# ============================================================
# Evaluation History
# ============================================================

st.header(
    "📈 Evaluation History"
)


history_rows = []

for index, run in enumerate(
    history_data
):

    score = get_run_score(
        run
    )

    history_rows.append(
        {
            "Run": get_run_id(
                run,
                index,
            ),
            "Timestamp": get_timestamp(
                run
            ),
            "Score": round(
                score * 100,
                2,
            ),
            "Test Cases": len(
                get_run_results(
                    run
                )
            ),
        }
    )


history_df = pd.DataFrame(
    history_rows
)


st.dataframe(
    history_df,
    use_container_width=True,
    hide_index=True,
)


history_chart = history_df[
    [
        "Run",
        "Score",
    ]
].copy()


history_chart = history_chart.set_index(
    "Run"
)


st.line_chart(
    history_chart
)


# ============================================================
# History CSV Download
# ============================================================

history_csv = (
    history_df
    .to_csv(index=False)
    .encode("utf-8")
)


st.download_button(
    label="⬇️ Download Evaluation History CSV",
    data=history_csv,
    file_name="evaluation_history.csv",
    mime="text/csv",
    key="download_evaluation_history_csv",
)


# ============================================================
# Run Comparison
# ============================================================

st.header(
    "🔄 Run Comparison"
)


if len(history_data) >= 2:

    comparison_options = []

    for index, run in enumerate(
        history_data
    ):

        comparison_options.append(
            f"Run {get_run_id(run, index)} | "
            f"{get_timestamp(run)} | "
            f"{percentage(get_run_score(run))}"
        )


    col1, col2 = st.columns(2)


    with col1:

        run_a_label = st.selectbox(
            "Select Run A",
            comparison_options,
            index=0,
            key="comparison_run_a",
        )


    with col2:

        run_b_label = st.selectbox(
            "Select Run B",
            comparison_options,
            index=len(comparison_options) - 1,
            key="comparison_run_b",
        )


    run_a_index = comparison_options.index(
        run_a_label
    )

    run_b_index = comparison_options.index(
        run_b_label
    )


    run_a = history_data[
        run_a_index
    ]

    run_b = history_data[
        run_b_index
    ]


    run_a_score = get_run_score(
        run_a
    )

    run_b_score = get_run_score(
        run_b
    )

    score_difference = (
        run_b_score - run_a_score
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Run A Score",
            percentage(
                run_a_score
            ),
        )


    with col2:

        st.metric(
            "Run B Score",
            percentage(
                run_b_score
            ),
        )


    with col3:

        st.metric(
            "Change",
            f"{score_difference * 100:+.2f}%",
        )


    if score_difference > 0:

        st.success(
            f"📈 Run B improved by "
            f"{score_difference * 100:.2f}%."
        )

    elif score_difference < 0:

        st.error(
            f"📉 Run B decreased by "
            f"{abs(score_difference) * 100:.2f}%."
        )

    else:

        st.info(
            "➡️ Both runs have the same score."
        )


    run_a_results = get_run_results(
        run_a
    )

    run_b_results = get_run_results(
        run_b
    )


    if run_a_results and run_b_results:

        run_a_map = {}

        for index, result in enumerate(
            run_a_results
        ):

            test_case = result.get(
                "test_case",
                index + 1,
            )

            run_a_map[str(test_case)] = result


        run_b_map = {}

        for index, result in enumerate(
            run_b_results
        ):

            test_case = result.get(
                "test_case",
                index + 1,
            )

            run_b_map[str(test_case)] = result


        comparison_rows = []


        all_test_cases = sorted(
            set(run_a_map)
            | set(run_b_map)
        )


        for test_case in all_test_cases:

            result_a = run_a_map.get(
                test_case,
                {}
            )

            result_b = run_b_map.get(
                test_case,
                {}
            )


            score_a = safe_score(
                result_a.get(
                    "score",
                    0,
                )
            )

            score_b = safe_score(
                result_b.get(
                    "score",
                    0,
                )
            )


            change = (
                score_b - score_a
            )


            if change > 0:

                status = "📈 Improved"

            elif change < 0:

                status = "📉 Declined"

            else:

                status = "➡️ No Change"


            comparison_rows.append(
                {
                    "Test Case": test_case,
                    "Run A Score": round(
                        score_a * 100,
                        2,
                    ),
                    "Run B Score": round(
                        score_b * 100,
                        2,
                    ),
                    "Change": round(
                        change * 100,
                        2,
                    ),
                    "Status": status,
                }
            )


        comparison_df = pd.DataFrame(
            comparison_rows
        )


        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True,
        )


        comparison_chart = comparison_df[
            [
                "Test Case",
                "Run A Score",
                "Run B Score",
            ]
        ].set_index(
            "Test Case"
        )


        st.bar_chart(
            comparison_chart
        )


        comparison_csv = (
            comparison_df
            .to_csv(index=False)
            .encode("utf-8")
        )


        st.download_button(
            label="⬇️ Download Run Comparison CSV",
            data=comparison_csv,
            file_name="run_comparison.csv",
            mime="text/csv",
            key="download_run_comparison_csv",
        )


else:

    st.info(
        "At least two evaluation runs are required "
        "for run comparison."
    )


# ============================================================
# Trend Analysis
# ============================================================

st.header(
    "📊 Evaluation Trend Analysis"
)


if len(history_data) >= 2:

    scores = [
        get_run_score(run)
        for run in history_data
    ]


    first_score = scores[0]

    latest_score = scores[-1]

    best_score = max(scores)

    worst_score = min(scores)


    overall_change = (
        latest_score - first_score
    )


    best_index = scores.index(
        best_score
    )

    worst_index = scores.index(
        worst_score
    )


    if overall_change > 0.001:

        trend_status = "📈 Improving"

    elif overall_change < -0.001:

        trend_status = "📉 Declining"

    else:

        trend_status = "➡️ Stable"


    if overall_change > 0.001:

        st.success(
            f"Evaluation is improving by "
            f"{overall_change * 100:+.2f}%."
        )

    elif overall_change < -0.001:

        st.error(
            f"Evaluation is declining by "
            f"{abs(overall_change) * 100:.2f}%."
        )

    else:

        st.info(
            "Evaluation performance is stable."
        )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Trend",
            trend_status,
        )


    with col2:

        st.metric(
            "First Run",
            percentage(
                first_score
            ),
        )


    with col3:

        st.metric(
            "Latest Run",
            percentage(
                latest_score
            ),
        )


    with col4:

        st.metric(
            "Best Score",
            percentage(
                best_score
            ),
        )


    trend_df = pd.DataFrame(
        [
            {
                "Run": get_run_id(
                    run,
                    index,
                ),
                "Score": get_run_score(
                    run
                ) * 100,
            }
            for index, run in enumerate(
                history_data
            )
        ]
    )


    trend_chart = trend_df.set_index(
        "Run"
    )


    st.line_chart(
        trend_chart
    )


else:

    st.info(
        "At least two runs are required "
        "for trend analysis."
    )


# ============================================================
# Failure Analysis
# ============================================================

st.header(
    "🚨 Evaluation Failure Analysis"
)


if current_results:

    failed_results = []

    for index, result in enumerate(
        current_results
    ):

        score = safe_score(
            result.get(
                "score",
                0,
            )
        )

        if score < threshold:

            failed_results.append(
                {
                    "index": index,
                    "result": result,
                    "score": score,
                }
            )


    total_test_cases = len(
        current_results
    )

    total_failed = len(
        failed_results
    )

    total_passed = (
        total_test_cases
        - total_failed
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Total",
            total_test_cases,
        )


    with col2:

        st.metric(
            "Passed",
            total_passed,
        )


    with col3:

        st.metric(
            "Failed",
            total_failed,
        )


    if total_failed == 0:

        st.success(
            "🎉 No test cases failed."
        )

    else:

        st.error(
            f"{total_failed} test case(s) "
            f"failed the threshold."
        )


    metric_names = {
        "context_relevance": "Context Relevance",
        "faithfulness": "Faithfulness",
        "answer_relevance": "Answer Relevance",
        "answer_correctness": "Answer Correctness",
        "source_pass": "Source Check",
    }


    metric_failures = {
        metric: 0
        for metric in metric_names
    }


    for result in current_results:

        for metric in metric_names:

            if not metric_passed(
                result,
                metric,
            ):

                metric_failures[
                    metric
                ] += 1


    failure_rows = []


    for metric, name in metric_names.items():

        count = metric_failures[
            metric
        ]

        failure_rows.append(
            {
                "Metric": name,
                "Failures": count,
                "Failure %": round(
                    (
                        count
                        / total_test_cases
                        * 100
                    ),
                    2,
                ),
            }
        )


    failure_df = pd.DataFrame(
        failure_rows
    )


    st.write(
        "### Failure Count by Metric"
    )


    st.dataframe(
        failure_df,
        use_container_width=True,
        hide_index=True,
    )


    failure_chart = failure_df[
        [
            "Metric",
            "Failures",
        ]
    ].set_index(
        "Metric"
    )


    st.bar_chart(
        failure_chart
    )


    if metric_failures:

        worst_metric = max(
            metric_failures,
            key=metric_failures.get,
        )

        st.warning(
            f"⚠️ Most problematic metric: "
            f"**{metric_names[worst_metric]}** "
            f"with "
            f"**{metric_failures[worst_metric]} "
            f"failure(s)**."
        )


    if failed_results:

        failed_rows = []


        for item in failed_results:

            result = item["result"]

            failed_metrics = []


            for metric, name in metric_names.items():

                if not metric_passed(
                    result,
                    metric,
                ):

                    failed_metrics.append(
                        name
                    )


            failed_rows.append(
                {
                    "Test Case": result.get(
                        "test_case",
                        item["index"] + 1,
                    ),
                    "Question": result.get(
                        "question",
                        "",
                    ),
                    "Score": round(
                        item["score"] * 100,
                        2,
                    ),
                    "Failed Metrics": ", ".join(
                        failed_metrics
                    ),
                }
            )


        failed_df = pd.DataFrame(
            failed_rows
        )


        st.write(
            "### ❌ Failed Test Cases"
        )


        st.dataframe(
            failed_df,
            use_container_width=True,
            hide_index=True,
        )


        failure_csv = (
            failed_df
            .to_csv(index=False)
            .encode("utf-8")
        )


        st.download_button(
            label="⬇️ Download Failure Analysis CSV",
            data=failure_csv,
            file_name="evaluation_failures.csv",
            mime="text/csv",
            key="download_failure_analysis_csv",
        )


# ============================================================
# Recommendations
# ============================================================

st.header(
    "💡 Evaluation Recommendations"
)


if current_results:

    total_test_cases = len(
        current_results
    )


    recommendation_data = {
        "context_relevance": (
            "Improve document retrieval, chunking, "
            "embeddings and top_k."
        ),
        "faithfulness": (
            "Strengthen grounding and instruct the LLM "
            "to answer only from retrieved context."
        ),
        "answer_relevance": (
            "Improve query handling and the generation "
            "prompt so answers directly address the question."
        ),
        "answer_correctness": (
            "Check retrieval quality and verify that the "
            "LLM correctly interprets retrieved information."
        ),
        "source_pass": (
            "Check source metadata, source tracking, "
            "and page information."
        ),
    }


    recommendation_rows = []


    for metric, recommendation in recommendation_data.items():

        failures = metric_failures.get(
            metric,
            0,
        )


        failure_percentage = (
            failures
            / total_test_cases
            * 100
        )


        if failure_percentage >= 75:

            priority = "🔴 High"

        elif failure_percentage >= 50:

            priority = "🟠 Medium"

        elif failure_percentage > 0:

            priority = "🟡 Low"

        else:

            priority = "🟢 Good"


        recommendation_rows.append(
            {
                "Metric": metric_names.get(
                    metric,
                    metric,
                ),
                "Failures": failures,
                "Failure %": round(
                    failure_percentage,
                    2,
                ),
                "Priority": priority,
                "Recommendation": (
                    recommendation
                    if failures
                    else "Metric is performing well."
                ),
            }
        )


    recommendation_df = pd.DataFrame(
        recommendation_rows
    )


    st.dataframe(
        recommendation_df,
        use_container_width=True,
        hide_index=True,
    )


    for row in recommendation_rows:

        if row["Failures"] == 0:

            continue


        with st.expander(
            f"{row['Priority']} "
            f"{row['Metric']} — "
            f"{row['Failure %']:.2f}% failure rate"
        ):

            st.write(
                row["Recommendation"]
            )


    recommendation_csv = (
        recommendation_df
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        label="⬇️ Download Recommendations CSV",
        data=recommendation_csv,
        file_name="evaluation_recommendations.csv",
        mime="text/csv",
        key="download_recommendations_csv",
    )


# ============================================================
# Final Evaluation Summary
# ============================================================

st.header(
    "🏁 Final Evaluation Summary"
)


if current_results:

    total_test_cases = len(
        current_results
    )


    scores = [
        safe_score(
            result.get(
                "score",
                0,
            )
        )
        for result in current_results
    ]


    average_score = (
        sum(scores)
        / len(scores)
        if scores
        else 0
    )


    passed = sum(
        score >= threshold
        for score in scores
    )


    failed = (
        total_test_cases
        - passed
    )


    pass_rate = (
        passed
        / total_test_cases
        if total_test_cases
        else 0
    )


    if average_score >= 0.80:

        health_status = "🟢 Excellent"

    elif average_score >= 0.65:

        health_status = "🟡 Good"

    elif average_score >= 0.50:

        health_status = "🟠 Needs Improvement"

    else:

        health_status = "🔴 Poor"


    if average_score >= 0.80:

        st.success(
            f"{health_status} — "
            "The RAG system is performing very well."
        )

    elif average_score >= 0.65:

        st.info(
            f"{health_status} — "
            "The RAG system is performing reasonably well."
        )

    elif average_score >= 0.50:

        st.warning(
            f"{health_status} — "
            "The RAG system needs improvement."
        )

    else:

        st.error(
            f"{health_status} — "
            "The RAG system requires significant improvement."
        )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Overall Score",
            percentage(
                average_score
            ),
        )


    with col2:

        st.metric(
            "Pass Rate",
            percentage(
                pass_rate
            ),
        )


    with col3:

        st.metric(
            "Passed",
            passed,
        )


    with col4:

        st.metric(
            "Failed",
            failed,
        )


    # --------------------------------------------------------
    # Best / Worst Test
    # --------------------------------------------------------

    best_index = scores.index(
        max(scores)
    )

    worst_index = scores.index(
        min(scores)
    )


    best_result = current_results[
        best_index
    ]

    worst_result = current_results[
        worst_index
    ]


    col1, col2 = st.columns(2)


    with col1:

        st.write(
            "### 🏆 Best Test Case"
        )

        st.metric(
            "Score",
            percentage(
                scores[best_index]
            ),
        )

        st.write(
            best_result.get(
                "question",
                "",
            )
        )


    with col2:

        st.write(
            "### ⚠️ Worst Test Case"
        )

        st.metric(
            "Score",
            percentage(
                scores[worst_index]
            ),
        )

        st.write(
            worst_result.get(
                "question",
                "",
            )
        )


    # --------------------------------------------------------
    # Metric Summary
    # --------------------------------------------------------

    metric_summary_rows = []


    for metric, name in metric_names.items():

        passed_count = sum(
            metric_passed(
                result,
                metric,
            )
            for result in current_results
        )


        metric_score = (
            passed_count
            / total_test_cases
            if total_test_cases
            else 0
        )


        metric_summary_rows.append(
            {
                "Metric": name,
                "Score": round(
                    metric_score * 100,
                    2,
                ),
            }
        )


    metric_summary_df = pd.DataFrame(
        metric_summary_rows
    )


    st.write(
        "### 📊 Metric Performance"
    )


    st.dataframe(
        metric_summary_df,
        use_container_width=True,
        hide_index=True,
    )


    # --------------------------------------------------------
    # Final Recommendation
    # --------------------------------------------------------

    if metric_failures:

        worst_metric = max(
            metric_failures,
            key=metric_failures.get,
        )


        recommendations = {
            "context_relevance": (
                "Focus on the retrieval pipeline: "
                "chunking, embeddings, top_k and document quality."
            ),
            "faithfulness": (
                "Focus on grounding the LLM response "
                "strictly in retrieved context."
            ),
            "answer_relevance": (
                "Improve query handling and the generation prompt."
            ),
            "answer_correctness": (
                "Investigate both retrieval and generation "
                "for incorrect answers."
            ),
            "source_pass": (
                "Review source metadata and source tracking."
            ),
        }


        st.info(
            recommendations.get(
                worst_metric,
                "Review the failed test cases."
            )
        )


    # --------------------------------------------------------
    # Final Summary Download
    # --------------------------------------------------------

    final_summary = pd.DataFrame(
        [
            {
                "Category": "Overall Health",
                "Value": health_status,
            },
            {
                "Category": "Overall Score",
                "Value": percentage(
                    average_score
                ),
            },
            {
                "Category": "Pass Rate",
                "Value": percentage(
                    pass_rate
                ),
            },
            {
                "Category": "Passed Tests",
                "Value": passed,
            },
            {
                "Category": "Failed Tests",
                "Value": failed,
            },
            {
                "Category": "Total Tests",
                "Value": total_test_cases,
            },
        ]
    )


    st.write(
        "### 📋 Summary"
    )


    st.dataframe(
        final_summary,
        use_container_width=True,
        hide_index=True,
    )


    final_summary_csv = (
        final_summary
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        label="⬇️ Download Final Evaluation Summary",
        data=final_summary_csv,
        file_name="final_evaluation_summary.csv",
        mime="text/csv",
        key="download_final_evaluation_summary",
    )


# ============================================================
# Evaluation Run Details
# ============================================================

st.header(
    "🔎 Evaluation Run Details"
)


if current_results:

    for index, result in enumerate(
        current_results
    ):

        test_case = result.get(
            "test_case",
            index + 1,
        )

        question = result.get(
            "question",
            "",
        )

        score = safe_score(
            result.get(
                "score",
                0,
            )
        )


        with st.expander(
            f"Test Case {test_case} — "
            f"{percentage(score)}"
        ):

            st.write(
                "### Question"
            )

            st.write(
                question
            )


            if "expected_answer" in result:

                st.write(
                    "### Expected Answer"
                )

                st.write(
                    result.get(
                        "expected_answer",
                        "",
                    )
                )


            if "actual_answer" in result:

                st.write(
                    "### Actual Answer"
                )

                st.write(
                    result.get(
                        "actual_answer",
                        "",
                    )
                )


            st.write(
                "### Metrics"
            )


            metric_detail_rows = []


            for metric, name in metric_names.items():

                value = metric_passed(
                    result,
                    metric,
                )


                metric_detail_rows.append(
                    {
                        "Metric": name,
                        "Result": (
                            "✅ Pass"
                            if value
                            else "❌ Fail"
                        ),
                    }
                )


            st.dataframe(
                pd.DataFrame(
                    metric_detail_rows
                ),
                use_container_width=True,
                hide_index=True,
            )


            if "metadata" in result:

                st.write(
                    "### Metadata"
                )

                st.json(
                    result["metadata"]
                )


else:

    st.info(
        "No test-case details available."
    )


# ============================================================
# Footer
# ============================================================

st.divider()

st.caption(
    "RAG Evaluation Dashboard • "
    "Evaluation pipeline monitoring and analysis"
)