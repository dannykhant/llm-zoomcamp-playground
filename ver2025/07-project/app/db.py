import os
import psycopg2
import psycopg2.extras

psycopg2.extras.register_uuid()


def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME", "fitness_db"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password"),
        host=os.getenv("DB_HOST", "localhost"),
        port="5432",
    )
    return conn


def initialize_db():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS conversations;")
            cursor.execute("DROP TABLE IF EXISTS feedback;")

            cursor.execute(
                """
                CREATE TABLE conversations (
                    id SERIAL PRIMARY KEY,
                    conversation_id UUID NOT NULL,
                    query TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    relevance_evaluation TEXT NOT NULL,
                    evaluation_explanation TEXT NOT NULL,
                    model TEXT NOT NULL,
                    response_time FLOAT NOT NULL,
                    answer_tokens INTEGER NOT NULL,
                    eval_tokens INTEGER NOT NULL,
                    answer_cost FLOAT NOT NULL,
                    eval_cost FLOAT NOT NULL,
                    total_cost FLOAT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE feedback (
                    id SERIAL PRIMARY KEY,
                    conversation_id UUID NOT NULL,
                    feedback INTEGER NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
        conn.commit()
    finally:
        conn.close()


def insert_conversation(
    conversation_id,
    query,
    answer,
    prompt,
    relevance_evaluation,
    evaluation_explanation,
    model,
    response_time,
    answer_tokens,
    eval_tokens,
    answer_cost,
    eval_cost,
    total_cost,
):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO conversations (
                    conversation_id, query, answer, prompt,
                    relevance_evaluation, evaluation_explanation,
                    model, response_time, answer_tokens, eval_tokens,
                    answer_cost, eval_cost, total_cost
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    conversation_id,
                    query,
                    answer,
                    prompt,
                    relevance_evaluation,
                    evaluation_explanation,
                    model,
                    response_time,
                    answer_tokens,
                    eval_tokens,
                    answer_cost,
                    eval_cost,
                    total_cost,
                ),
            )
        conn.commit()
    finally:
        conn.close()


def insert_feedback(
    conversation_id,
    feedback,
):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO conversations (
                    conversation_id, query, answer, prompt,
                    relevance_evaluation, evaluation_explanation,
                    model, response_time, answer_tokens, eval_tokens,
                    answer_cost, eval_cost, total_cost
                ) VALUES (%s, %s)
                """,
                (conversation_id, feedback),
            )
        conn.commit()
    finally:
        conn.close()


def fetch_recent_conversations(limit=3):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    conv.conversation_id,
                    conv.query,
                    conv.answer,
                    conv.prompt,
                    conv.relevance_evaluation,
                    conv.evaluation_explanation,
                    conv.model,
                    conv.response_time,
                    conv.answer_tokens,
                    conv.eval_tokens,
                    conv.answer_cost,
                    conv.eval_cost,
                    conv.total_cost,
                    fb.feedback,
                    conv.timestamp
                FROM conversations AS conv
                LEFT JOIN feedback AS fb 
                USING (conversation_id)
                ORDER BY conv.timestamp DESC
                LIMIT %s
                """,
                (limit,),
            )
            result = cursor.fetchall()
            return result
    finally:
        conn.close()
