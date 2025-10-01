from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime

# Базовые схемы
class AnswerBase(BaseModel):
    answer_text: str = Field(..., description="Текст ответа")
    is_correct: bool = Field(False, description="Правильный ли ответ")
    order_index: int = Field(0, description="Порядок ответа")

class AnswerCreate(AnswerBase):
    pass

class AnswerResponse(AnswerBase):
    id: int
    
    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    question_text: str = Field(..., description="Текст вопроса")
    order_index: int = Field(0, description="Порядок вопроса")

class QuestionCreate(QuestionBase):
    answers: List[AnswerCreate] = Field(..., min_items=2, description="Список ответов")

class QuestionResponse(QuestionBase):
    id: int
    quiz_id: int
    answers: List[AnswerResponse]
    
    class Config:
        from_attributes = True

class QuizBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Название викторины")
    description: Optional[str] = Field(None, description="Описание викторины")
    prize: str = Field(..., description="Описание приза")

class QuizCreate(QuizBase):
    questions: List[QuestionCreate] = Field(..., min_items=1, description="Список вопросов")

class QuizResponse(QuizBase):
    id: int
    questions_count: int  # Количество вопросов
    
    class Config:
        from_attributes = True

class QuizListResponse(BaseModel):
    items: List[QuizResponse]
    total: int
    page: int
    size: int
    pages: int

# Схемы для прохождения викторины
class UserAnswer(BaseModel):
    question_id: int = Field(..., description="ID вопроса")
    answer_ids: List[int] = Field(..., min_items=1, description="Выбранные ID ответов")

class QuizSubmission(BaseModel):
    quiz_id: int = Field(..., description="ID викторины")
    answers: List[UserAnswer] = Field(..., min_items=1, description="Ответы пользователя")

class QuizResult(BaseModel):
    quiz_id: int
    total_questions: int
    correct_answers: int
    score_percentage: float
    has_won_prize: bool
    prize_description: Optional[str] = None
    correct_answers_details: List[Dict[str, Any]]  # Детали по каждому вопросу