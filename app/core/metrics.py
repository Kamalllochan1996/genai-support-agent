from prometheus_client import Counter, Histogram


chat_requests_total = Counter(
    "chat_requests_total",
    "Total number of chat requests",
)


chat_errors_total = Counter(
    "chat_errors_total",
    "Total number of failed chat requests",
)


llm_requests_total = Counter(
    "llm_requests_total",
    "Total number of LLM requests",
)


llm_errors_total = Counter(
    "llm_errors_total",
    "Total number of failed LLM requests",
)


llm_request_duration_seconds = Histogram(
    "llm_request_duration_seconds",
    "Time spent generating LLM responses",
)