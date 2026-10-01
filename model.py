from pydantic import BaseModel


class Quiz(BaseModel):
    question: str | None
    answer: str | None


class Lesson(BaseModel):
    answer: str
    topic: str | None
    summary: str | None
    key_points: list[str] | None
    quiz: list[Quiz] | None
