# Module: 4

### 4.1: Introduction

- Why observability?
    - Pain points
        - Complex chains of prompts, agents, APIs
        - Difficult to pinpoint where the application broke
        - No visibility into how prompt changes affect downstream
- Semantic failures
    - Hallucinations
    - Toxic responses
    - Incorrect answers
    - Broken function calls
- LLM tracing
    - The practice of recording what actually happened inside an LLM interaction
    - Tracing isn’t just about bugs, it’s about iteration, quality, and trust
    - Tracing reveals
        - Failures
        - Session divergence
        - Handoff issues
- The limits of online evaluation
    - Feedback delayed or missing
    - Hard to measure safety, helpfulness, correctness in real-time
    - Need offline evals to fill the gaps

### 4.2: Instrumenting LLM Pipelines with OpenTelementry

- OpenTelementry (OTel)
    - Open source standard for collecting distributed traces, metrics, and logs across systems
    - Core idea
        - To give every request a trace ID and let each component of the system contributes a span to that trace
        - Each span contains duration, status, context specific metadata
- OpenInference
    - The extension of OTel that is designed for ML and AI systems
- What to instrument in LLM RAG pipeline
    - User input
        - Capture the initial request
    - Retriever
        - What query was used? How many docs came back?
    - Prompt construction
        - Include prompt template, parameters used…
    - Model call
        - Which model, what temperature, latency…
    - Parsing/ Tooling
        - Functions, agents, or tools
- Takeaways
    - Tracing is first step to LLM observability
    - OpenTelementry = tooling
    - OpenInference = schema
    - Phoenix = visibility

### 4.3: Evaluation of LLM Pipelines

- Example of what goes wrong
    - Figure out which tool to call (tool selection eval)
        - Calls the wrong tool
    - Search API (function calling eval)
        - Constructs search incorrectly
    - Use context (RAG eval)
    - Construct a response (tone eval)
        - Could be jail-broken, or in appropriate
    - Overall correctness (correctness eval)
        - Unhappy user
- Mental model
    - Instrumentation
    - Traces
    - Evaluations
    - Metrics & dashboards
- What can be measured from Live Traces
    - Latency
    - Fallback/ Retry Rate
    - Answer Quality
- Best practices for evaluation
    - Start simple
        - Latency, fallbacks, empty responses
    - Tag spans
        - Good metadata makes evaluation easier
    - Use thresholds + alerts
        - To get signal
    - Layer in LLM evals
        - Fluency, factuality
    - Backfill
        - From historical traces as needed
- Takeaways
    - Catch issues before users do
    - Build trust in pipeline
    - Foundation for continuous improvement