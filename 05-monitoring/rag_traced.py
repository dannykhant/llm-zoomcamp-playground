from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor, SpanExporter, SpanExportResult

import sqlite3

from rag_helper import RAGBase


class SQLiteSpanExporter(SpanExporter):

    def __init__(self, db_path="traces.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS spans (
                name TEXT,
                start_time INTEGER,
                end_time INTEGER,
                input_tokens INTEGER,
                output_tokens INTEGER,
                cost REAL
            )
        """)
        self.conn.commit()

    def export(self, spans):
        for span in spans:
            attrs = dict(span.attributes or {})
            self.conn.execute(
                "INSERT INTO spans VALUES (?, ?, ?, ?, ?, ?)",
                (
                    span.name,
                    span.start_time,
                    span.end_time,
                    attrs.get("input_tokens"),
                    attrs.get("output_tokens"),
                    attrs.get("cost"),
                ),
            )
        self.conn.commit()
        return SpanExportResult.SUCCESS

    def shutdown(self):
        self.conn.close()

    def force_flush(self):
        return True

provider = TracerProvider()
provider.add_span_processor(
    SimpleSpanProcessor(SQLiteSpanExporter())
)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("llm-zoomcamp")


class RAGTraced(RAGBase):
    def __init__(self, index, llm_client):
        model = 'GLM-4.7-Flash'
        super().__init__(index, llm_client, model=model)

    def search(self, query, num_results=5):
        with tracer.start_as_current_span("search") as span:
            search_results = super().search(query, num_results)
            span.set_attribute("num_results", len(search_results))
            return search_results

    def llm_completion(self, prompt):
        with tracer.start_as_current_span("llm") as span:
            response = super().llm_completion(prompt)
            span.set_attribute("input_tokens", response.usage.prompt_tokens)
            span.set_attribute("output_tokens", response.usage.completion_tokens)
            return response

    def rag(self, query):
        with tracer.start_as_current_span("rag") as span:
            span.set_attribute("query", query)
            return super().rag(query)
