from datetime import datetime
from uuid import uuid4
from fastapi import FastAPI
from pydantic import UUID4, BaseModel, ConfigDict, Field

from app.rag import rag
from app.db import fetch_recent_conversations, insert_conversation, insert_feedback

app = FastAPI(title="Fitness Assistant API")


class UserQuery(BaseModel):
    query: str = "What are some effective exercises for building core strength?"


class GenerationResponse(BaseModel):
    conversation_id: UUID4
    query: str
    answer: str


class UserFeedback(BaseModel):
    conversation_id: UUID4
    feedback: str


class ConversationRow(BaseModel):
    conversation_id: UUID4
    query: str
    answer: str
    prompt: str
    relevance: str = Field(alias="relevance_evaluation")
    explanation: str = Field(alias="evaluation_explanation")
    model: str
    response_time: float
    answer_tokens: int
    eval_tokens: int
    answer_cost: float
    eval_cost: float
    total_cost: float
    feedback: str | None = None
    timestamp: datetime

    # Required for Pydantic to accept positional arguments from psycopg2 tuples
    model_config = ConfigDict(populate_by_name=True)


@app.get("/")
async def health():
    return {"status": "ok"}


@app.post("/generate")
async def generate_answer(user_query: UserQuery) -> GenerationResponse:
    uuid = uuid4()
    query = user_query.query
    answer = rag(query)

    insert_conversation(
        conversation_id=uuid,
        query=query,
        answer=answer["answer"],
        prompt=answer["prompt"],
        relevance_evaluation=answer["relevance_evaluation"],
        evaluation_explanation=answer["evaluation_explanation"],
        model=answer["model"],
        response_time=answer["response_time"],
        answer_tokens=answer["token_usage"]["answer_tokens"]["total_tokens"],
        eval_tokens=answer["token_usage"]["eval_tokens"]["total_tokens"],
        answer_cost=answer["cost"]["answer_cost"],
        eval_cost=answer["cost"]["eval_cost"],
        total_cost=answer["cost"]["total_cost"],
    )

    return GenerationResponse(
        conversation_id=uuid, query=query, answer=answer["answer"]
    )


@app.post("/feedback/{conversation_id}")
async def submit_feedback(user_feedback: UserFeedback):
    insert_feedback(
        conversation_id=user_feedback.conversation_id,
        feedback=user_feedback.feedback,
    )
    return {
        "status": "feedback recorded for conversation_id {}".format(
            user_feedback.conversation_id
        )
    }


@app.get("/recent_conversations")
async def recent_conversations(limit: int = 3):
    conversations = fetch_recent_conversations(limit=limit)
    conversations_mapped = [
        ConversationRow(**dict(zip(ConversationRow.model_fields.keys(), row)))
        for row in conversations
    ]
    return {"recent_conversations": conversations_mapped}
