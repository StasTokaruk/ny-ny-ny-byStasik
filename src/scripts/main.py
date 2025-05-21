from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, DateTime, BLOB, ForeignKey, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from typing import List, Optional
from datetime import datetime
import os
import uvicorn

# Database connection
DATABASE_URL = "mysql+pymysql://root:admin@localhost:3307/mydb"
# Replace with your actual database credentials

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Models (SQLAlchemy ORM models)
class Role(Base):
    __tablename__ = "Role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100))

    # Relationships
    users = relationship("UserRole", backref="role")


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    picture = Column(BLOB, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    nickname = Column(String(50), nullable=False)

    # Relationships
    expertise = relationship("UserExpertise", back_populates="user")
    roles = relationship("UserRole", backref="user")


class UserRole(Base):
    __tablename__ = "UserRole"

    User_id = Column(Integer, ForeignKey("User.id"), primary_key=True)
    Role_id = Column(Integer, ForeignKey("Role.id"), primary_key=True)


class ExpertiseCategory(Base):
    __tablename__ = "ExpertiseCategory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String(100))

    # Relationships
    users = relationship("UserExpertise", back_populates="expertise_category")


class UserExpertise(Base):
    __tablename__ = "UserExpertise"

    ExpertiseCategory_id = Column(Integer, ForeignKey("ExpertiseCategory.id"), primary_key=True)
    User_id = Column(Integer, ForeignKey("User.id"), primary_key=True)

    # Relationships
    expertise_category = relationship("ExpertiseCategory", back_populates="users")
    user = relationship("User", back_populates="expertise")


class Quiz(Base):
    __tablename__ = "Quiz"

    id = Column(Integer, primary_key=True, index=True)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    name = Column(String(100))
    description = Column(String(255))
    User_id = Column(Integer, ForeignKey("User.id"))

    # Relationships
    user = relationship("User", backref="quizzes")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "Question"

    id = Column(Integer, primary_key=True, index=True)
    Quiz_id = Column(Integer, ForeignKey("Quiz.id"))
    number = Column(Integer)
    description = Column(String(255))
    type = Column(String(45))

    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")
    answers = relationship("Answer", back_populates="question")


class Option(Base):
    __tablename__ = "Option"

    id = Column(Integer, primary_key=True, index=True)
    Question_id = Column(Integer, ForeignKey("Question.id"))
    number = Column(Integer)
    description = Column(Integer)  # Note: This should probably be String instead of Integer based on common patterns

    # Relationships
    question = relationship("Question", back_populates="options")
    selected_options = relationship("SelectedOption", back_populates="option")


class SurveySession(Base):
    __tablename__ = "SurveySession"

    id = Column(Integer, primary_key=True, index=True)
    User_id = Column(Integer, ForeignKey("User.id"))
    Quiz_id = Column(Integer, ForeignKey("Quiz.id"))
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    status = Column(String(45))

    # Relationships
    user = relationship("User", backref="survey_sessions")
    quiz = relationship("Quiz", backref="survey_sessions")
    answers = relationship("Answer", back_populates="survey_session", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "Answer"

    id = Column(Integer, primary_key=True, index=True)
    SurveySession_id = Column(Integer, ForeignKey("SurveySession.id"))
    Question_id = Column(Integer, ForeignKey("Question.id"))
    file = Column(BLOB)
    text = Column(String(255))

    # Relationships
    survey_session = relationship("SurveySession", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    selected_options = relationship("SelectedOption", back_populates="answer", cascade="all, delete-orphan")


class SelectedOption(Base):
    __tablename__ = "SelectedOption"

    Answer_id = Column(Integer, ForeignKey("Answer.id"), primary_key=True)
    Option_id = Column(Integer, ForeignKey("Option.id"), primary_key=True)

    # Relationships
    answer = relationship("Answer", back_populates="selected_options")
    option = relationship("Option", back_populates="selected_options")


# Pydantic models (for request/response)
class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    surname: str
    nickname: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    surname: str
    nickname: str
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


class ExpertiseCategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ExpertiseCategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class UserExpertiseCreate(BaseModel):
    User_id: int
    ExpertiseCategory_id: int


class UserExpertiseResponse(BaseModel):
    User_id: int
    ExpertiseCategory_id: int

    model_config = {
        "from_attributes": True
    }


class QuizCreate(BaseModel):
    name: str
    description: Optional[str] = None
    User_id: int


class QuizResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    User_id: int

    model_config = {
        "from_attributes": True
    }


class QuestionCreate(BaseModel):
    Quiz_id: int
    number: int
    description: str
    type: str


class QuestionResponse(BaseModel):
    id: int
    Quiz_id: int
    number: int
    description: str
    type: str

    model_config = {
        "from_attributes": True
    }


class OptionCreate(BaseModel):
    Question_id: int
    number: int
    description: str  # Changed from int to str based on common sense for option descriptions


class OptionResponse(BaseModel):
    id: int
    Question_id: int
    number: int
    description: str  # Changed from int to str

    model_config = {
        "from_attributes": True
    }


class SurveySessionCreate(BaseModel):
    User_id: int
    Quiz_id: int
    status: str = "started"


class SurveySessionResponse(BaseModel):
    id: int
    User_id: int
    Quiz_id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str

    model_config = {
        "from_attributes": True
    }


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="Expert Survey API")


# Role endpoints
@app.post("/roles/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@app.get("/roles/", response_model=List[RoleResponse])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles


@app.get("/roles/{role_id}", response_model=RoleResponse)
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role


# User endpoints
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # In a real application, you would hash the password here
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/expertise-categories/", response_model=ExpertiseCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_expertise_category(category: ExpertiseCategoryCreate, db: Session = Depends(get_db)):
    db_category = ExpertiseCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.get("/expertise-categories/", response_model=List[ExpertiseCategoryResponse])
def read_expertise_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(ExpertiseCategory).offset(skip).limit(limit).all()
    return categories


@app.get("/expertise-categories/{category_id}", response_model=ExpertiseCategoryResponse)
def read_expertise_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(ExpertiseCategory).filter(ExpertiseCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Expertise category not found")
    return db_category


@app.put("/expertise-categories/{category_id}", response_model=ExpertiseCategoryResponse)
def update_expertise_category(category_id: int, category: ExpertiseCategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(ExpertiseCategory).filter(ExpertiseCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Expertise category not found")

    for key, value in category.dict().items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


@app.delete("/expertise-categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expertise_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(ExpertiseCategory).filter(ExpertiseCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Expertise category not found")

    db.delete(db_category)
    db.commit()
    return None


# UserExpertise endpoints
@app.post("/user-expertise/", response_model=UserExpertiseResponse, status_code=status.HTTP_201_CREATED)
def create_user_expertise(user_expertise: UserExpertiseCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == user_expertise.User_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if expertise category exists
    category = db.query(ExpertiseCategory).filter(ExpertiseCategory.id == user_expertise.ExpertiseCategory_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Expertise category not found")

    # Check if this association already exists
    existing = db.query(UserExpertise).filter(
        UserExpertise.User_id == user_expertise.User_id,
        UserExpertise.ExpertiseCategory_id == user_expertise.ExpertiseCategory_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="This user already has this expertise category")

    db_user_expertise = UserExpertise(**user_expertise.dict())
    db.add(db_user_expertise)
    db.commit()
    return db_user_expertise


@app.get("/user-expertise/by-user/{user_id}", response_model=List[ExpertiseCategoryResponse])
def read_user_expertise(user_id: int, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all expertise categories for this user
    user_expertise = db.query(UserExpertise).filter(UserExpertise.User_id == user_id).all()

    if not user_expertise:
        return []

    # Get the actual expertise categories
    category_ids = [ue.ExpertiseCategory_id for ue in user_expertise]
    categories = db.query(ExpertiseCategory).filter(ExpertiseCategory.id.in_(category_ids)).all()

    return categories


@app.delete("/user-expertise/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_expertise(user_id: int, category_id: int, db: Session = Depends(get_db)):
    # Try to find the association
    user_expertise = db.query(UserExpertise).filter(
        UserExpertise.User_id == user_id,
        UserExpertise.ExpertiseCategory_id == category_id
    ).first()

    if not user_expertise:
        raise HTTPException(status_code=404, detail="User expertise association not found")

    db.delete(user_expertise)
    db.commit()
    return None


# Quiz endpoints
@app.post("/quizzes/", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == quiz.User_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_quiz = Quiz(**quiz.dict(), created_by=quiz.User_id)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz


@app.get("/quizzes/", response_model=List[QuizResponse])
def read_quizzes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).offset(skip).limit(limit).all()
    return quizzes


@app.get("/quizzes/{quiz_id}", response_model=QuizResponse)
def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz


@app.get("/quizzes/by-user/{user_id}", response_model=List[QuizResponse])
def read_quizzes_by_user(user_id: int, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    quizzes = db.query(Quiz).filter(Quiz.User_id == user_id).all()
    return quizzes


@app.put("/quizzes/{quiz_id}", response_model=QuizResponse)
def update_quiz(quiz_id: int, quiz: QuizCreate, db: Session = Depends(get_db)):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Check if user exists
    user = db.query(User).filter(User.id == quiz.User_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in quiz.dict().items():
        setattr(db_quiz, key, value)

    db_quiz.updated_at = datetime.now()
    db.commit()
    db.refresh(db_quiz)
    return db_quiz


@app.delete("/quizzes/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    db.delete(db_quiz)
    db.commit()
    return None


# Question endpoints
@app.post("/questions/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    # Check if quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == question.Quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@app.get("/questions/by-quiz/{quiz_id}", response_model=List[QuestionResponse])
def read_questions_by_quiz(quiz_id: int, db: Session = Depends(get_db)):
    # Check if quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    questions = db.query(Question).filter(Question.Quiz_id == quiz_id).order_by(Question.number).all()
    return questions


@app.get("/questions/{question_id}", response_model=QuestionResponse)
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@app.put("/questions/{question_id}", response_model=QuestionResponse)
def update_question(question_id: int, question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check if quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == question.Quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    for key, value in question.dict().items():
        setattr(db_question, key, value)

    db.commit()
    db.refresh(db_question)
    return db_question


@app.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(db_question)
    db.commit()
    return None


# Option endpoints
@app.post("/options/", response_model=OptionResponse, status_code=status.HTTP_201_CREATED)
def create_option(option: OptionCreate, db: Session = Depends(get_db)):
    # Check if question exists
    question = db.query(Question).filter(Question.id == option.Question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    db_option = Option(**option.dict())
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option


@app.get("/options/by-question/{question_id}", response_model=List[OptionResponse])
def read_options_by_question(question_id: int, db: Session = Depends(get_db)):
    # Check if question exists
    question = db.query(Question).filter(Question.id == question_id).first()
    db_quiz = db.query(Quiz)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    options = db.query(Option).filter(Option.Question_id == question_id).order_by(Option.number).all()
    return options.refresh(db_quiz)
    return db_quiz


@app.get("/quizzes/", response_model=List[QuizResponse])
def read_quizzes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).offset(skip).limit(limit).all()
    return quizzes


@app.get("/quizzes/{quiz_id}", response_model=QuizResponse)
def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz


# Test connection endpoint
@app.get("/test-connection")
def test_connection(db: Session = Depends(get_db)):
    try:
        # Execute a simple query to test the connection
        result = db.execute(text("SELECT 1")).first()
        if result:
            return {"status": "success", "message": "Connected to database successfully"}
        return {"status": "error", "message": "Connection test returned unexpected result"}
    except Exception as e:
        return {"status": "error", "message": f"Database connection error: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
