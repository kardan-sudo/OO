from typing import List
from database.database import get_db
from schemas.quiz import QuestionResponse, QuizCreate, QuizListResponse, QuizResponse, QuizResult, QuizSubmission
from routers.crud.quiz import quiz_crud
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

quiz_router = APIRouter(prefix="/quizzes", tags=["quizzes"])


# Ручки для заполнения данных
@quiz_router.post("/", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
async def create_quiz(
    quiz_data: QuizCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать новую викторину с вопросами и ответами"""
    try:
        quiz = await quiz_crud.create_quiz(db, quiz_data)
        # Добавляем количество вопросов для ответа
        quiz_dict = {**quiz.__dict__, "questions_count": len(quiz.questions)}
        return quiz_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating quiz: {str(e)}"
        )

# Получить список всех викторин
@quiz_router.get("/", response_model=QuizListResponse)
async def get_quizzes(
    db: AsyncSession = Depends(get_db),
    only_active: bool = Query(True, description="Только активные викторины"),
):
    """Получить список всех викторин"""
    quizzes = await quiz_crud.get_quizzes(
        db=db,
        only_active=only_active
    )
    
    total = await quiz_crud.get_quizzes_count(db=db, only_active=only_active)
    
    # Добавляем количество вопросов для каждой викторины
    quizzes_with_count = []
    for quiz in quizzes:
        quiz_dict = {**quiz.__dict__, "questions_count": len(quiz.questions)}
        quizzes_with_count.append(quiz_dict)
    
    return QuizListResponse(
        items=quizzes_with_count,
        total=total,
    )

# Получить вопросы конкретной викторины
@quiz_router.get("/{quiz_id}/questions", response_model=List[QuestionResponse])
async def get_quiz_questions(
    quiz_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить список вопросов для конкретной викторины"""
    questions = await quiz_crud.get_quiz_questions(db, quiz_id)
    
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found or has no questions"
        )
    
    return questions

# Пройти викторину и получить результат
@quiz_router.post("/{quiz_id}/submit", response_model=QuizResult)
async def submit_quiz(
    quiz_id: int,
    submission: QuizSubmission,
    db: AsyncSession = Depends(get_db)
):
    """Отправить ответы на викторину и получить результат"""
    if quiz_id != submission.quiz_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quiz ID in path and body don't match"
        )
    
    try:
        result = await quiz_crud.check_quiz_answers(db, quiz_id, submission.answers)
        return QuizResult(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing quiz: {str(e)}"
        )
