from models.quiz import Answer, Question, Quiz
from schemas.quiz import QuizCreate, UserAnswer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Optional, Dict, Any

class QuizCRUD:
    # Викторины
    async def create_quiz(self, db: AsyncSession, quiz_data: QuizCreate) -> Quiz:
        """Создать викторину с вопросами и ответами"""
        quiz_dict = quiz_data.dict(exclude={'questions'})
        db_quiz = Quiz(**quiz_dict)
        db.add(db_quiz)
        await db.flush()  # Получаем ID викторины
        
        # Создаем вопросы и ответы
        for question_data in quiz_data.questions:
            question_dict = question_data.dict(exclude={'answers'})
            db_question = Question(quiz_id=db_quiz.id, **question_dict)
            db.add(db_question)
            await db.flush()  # Получаем ID вопроса
            
            # Создаем ответы
            for answer_data in question_data.answers:
                db_answer = Answer(question_id=db_question.id, **answer_data.dict())
                db.add(db_answer)
        
        await db.commit()
        await db.refresh(db_quiz)
        return db_quiz

    async def get_quiz(self, db: AsyncSession, quiz_id: int) -> Optional[Quiz]:
        stmt = select(Quiz).where(Quiz.id == quiz_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_quizzes(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100,
        only_active: bool = True
    ) -> List[Quiz]:
        stmt = select(Quiz)
        
        if only_active:
            stmt = stmt.where(Quiz.is_active == True)
            
        stmt = stmt.order_by(Quiz.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_quizzes_count(self, db: AsyncSession, only_active: bool = True) -> int:
        stmt = select(func.count(Quiz.id))
        
        if only_active:
            stmt = stmt.where(Quiz.is_active == True)
            
        result = await db.execute(stmt)
        return result.scalar_one()

    # Вопросы
    async def get_quiz_questions(self, db: AsyncSession, quiz_id: int) -> List[Question]:
        stmt = (
            select(Question)
            .where(Question.quiz_id == quiz_id)
            .order_by(Question.order_index, Question.id)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_question_with_answers(self, db: AsyncSession, question_id: int) -> Optional[Question]:
        stmt = (
            select(Question)
            .where(Question.id == question_id)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    # Проверка ответов
    async def check_quiz_answers(
        self, 
        db: AsyncSession, 
        quiz_id: int, 
        user_answers: List[UserAnswer]
    ) -> Dict[str, Any]:
        """Проверить ответы пользователя и вернуть результат"""
        # Получаем викторину
        quiz = await self.get_quiz(db, quiz_id)
        if not quiz:
            raise ValueError("Quiz not found")
        
        # Получаем все вопросы викторины
        questions = await self.get_quiz_questions(db, quiz_id)
        total_questions = len(questions)
        
        if not total_questions:
            raise ValueError("Quiz has no questions")
        
        correct_count = 0
        details = []
        
        # Проверяем каждый вопрос
        for question in questions:
            user_answer = next((ua for ua in user_answers if ua.question_id == question.id), None)
            
            if not user_answer:
                # Пользователь не ответил на вопрос
                details.append({
                    "question_id": question.id,
                    "question_text": question.question_text,
                    "is_correct": False,
                    "user_answers": [],
                    "correct_answers": [answer.id for answer in question.answers if answer.is_correct]
                })
                continue
            
            # Получаем правильные ответы для этого вопроса
            correct_answer_ids = [answer.id for answer in question.answers if answer.is_correct]
            user_answer_ids = user_answer.answer_ids
            
            # Проверяем правильность ответа
            is_correct = False
            if question.question_type == "single_choice":
                # Для одиночного выбора - должен быть выбран ровно один правильный ответ
                is_correct = (len(user_answer_ids) == 1 and 
                            user_answer_ids[0] in correct_answer_ids)
            else:  # multiple_choice
                # Для множественного выбора - все выбранные должны быть правильными и все правильные выбраны
                is_correct = (set(user_answer_ids) == set(correct_answer_ids))
            
            if is_correct:
                correct_count += 1
            
            details.append({
                "question_id": question.id,
                "question_text": question.question_text,
                "is_correct": is_correct,
                "user_answers": user_answer_ids,
                "correct_answers": correct_answer_ids
            })
        
        # Рассчитываем результат
        score_percentage = (correct_count / total_questions) * 100
        has_won_prize = score_percentage >= 90
        
        return {
            "quiz_id": quiz_id,
            "total_questions": total_questions,
            "correct_answers": correct_count,
            "score_percentage": round(score_percentage, 2),
            "has_won_prize": has_won_prize,
            "prize_description": quiz.prize if has_won_prize else None,
            "correct_answers_details": details
        }
    
quiz_crud = QuizCRUD()