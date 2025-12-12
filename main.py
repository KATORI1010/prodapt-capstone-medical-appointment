import os
from typing import Annotated
import string
import random
from datetime import date

from pydantic import BaseModel, Field, field_validator
from fastapi import (
    FastAPI,
    Request,
    Response,
    HTTPException,
    UploadFile,
    Form,
    status,
    BackgroundTasks,
    Depends,
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from supabase import create_client, Client

from db import get_db_session, get_db, Session
from models import JobBoard, JobPost, JobApplication, JobApplicationAIEvaluation
from auth import (
    authenticate_admin,
    is_admin,
    delete_admin_session,
    AdminAuthzMiddleware,
    AdminSessionMiddleware,
)
from evaluate_resume import evaluate_resume_with_ai
from extract_text_from_pdf import extract_text_from_pdf_bytes
from ai import (
    review_application,
    ReviewedApplication,
    ingest_resume,
    get_vector_store,
    QdrantVectorStore,
    get_recommendatation,
)
from emailer import send_email
from config import settings

app = FastAPI()
app.add_middleware(AdminAuthzMiddleware)
app.add_middleware(AdminSessionMiddleware)

supabase: Client = create_client(str(settings.SUPABASE_URL), settings.SUPABASE_KEY)


def ingest_resume_for_recommendation(
    pdf_content: bytes, filename: str, resume_id: int, vector_store
):
    text_content = extract_text_from_pdf_bytes(pdf_bytes=pdf_content)
    ingest_resume(text_content, filename, resume_id, vector_store)


@app.get("/api/health")
async def health():
    try:
        with get_db_session() as session:
            session.execute(text("SELECT 1"))
        return {"database": "ok"}
    except:
        return {"database": "down"}


class CalRequest(BaseModel):
    x: int
    y: int


@app.post("/api/add")
async def add(payload: CalRequest):
    result = payload.x + payload.y
    return {"result": result}


@app.post("/api/multiply")
async def multiply(payload: CalRequest):
    result = payload.x * payload.y
    return {"result": result}


# Jobify Part
jobBoards = {
    "acme": [
        {
            "title": "Customer Support Executive",
            "jobDescription": "The job posting of ACME for Customer Support Executive...",
        },
        {
            "title": "Project Manager",
            "jobDescription": "The job posting of ACME for Project Manager...",
        },
    ],
    "bcg": [
        {
            "title": "Technical Architect",
            "jobDescription": "The job posting of BCG for Technical Architect...",
        },
        {
            "title": "Junior Software Developer",
            "jobDescription": "The job posting of BCG for Junior Software Developer...",
        },
    ],
    "atlas": [
        {
            "title": "Azure Infrastracture Engineer",
            "jobDescription": "The job posting of ATLAS for Azure Infrastrucre Engineer...",
        },
        {
            "title": "Solution Architect",
            "jobDescription": "The job posting of ATLAS Solution Architect...",
        },
    ],
}

templates = Jinja2Templates(directory="templates")


@app.get("/job-boards/{slug}")
async def company_job_board(request: Request, slug: str):
    if slug in jobBoards:
        jobBoard = jobBoards[slug]
        return templates.TemplateResponse(
            request=request,
            name="job-boards.html",
            context={"jobs": jobBoard, "company": slug},
        )
    else:
        raise HTTPException(status_code=404, detail="Job board not found")


class AdminLoginForm(BaseModel):
    username: str
    password: str


@app.post("/api/admin-login")
async def admin_login(
    response: Response, admin_login_form: Annotated[AdminLoginForm, Form()]
):
    auth_response = authenticate_admin(
        admin_login_form.username, admin_login_form.password
    )
    if auth_response is not None:
        secure = settings.PRODUCTION
        response.set_cookie(
            key="admin_session",
            value=auth_response,
            httponly=True,
            secure=secure,
            samesite="Lax",
        )
        return {}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/api/admin-logout")
async def admin_logout(request: Request, response: Response):
    delete_admin_session(request.cookies.get("admin_session"))
    secure = settings.PRODUCTION
    response.delete_cookie(
        key="admin_session", httponly=True, secure=secure, samesite="Lax"
    )
    return {}


@app.get("/api/me")
async def me(request: Request):
    return {"is_admin": request.state.is_admin}


@app.get("/api/job-boards")
async def api_job_boards(db: Session = Depends(get_db)):
    jobBoards = db.query(JobBoard).order_by(JobBoard.id).all()
    return jobBoards


@app.get("/api/job-boards/{id}")
async def api_job_board_by_id(id: int, db: Session = Depends(get_db)):
    jobBoard = db.get(JobBoard, id)
    return jobBoard


# @app.post("/api/job-boards")
# async def api_create_new_job_board(request: Request):
#   body = await request.body()
#   raw_text = body.decode()
#   print(request.headers.get("content-type"))
#   print(raw_text)
#   return {}


class JobBoardForm(BaseModel):
    slug: str = Field(..., min_length=3, max_length=20)
    logo: UploadFile = Field(...)

    # @field_validator("slug")
    # @classmethod
    # def to_lowercase(cls, v):
    #   return v.lower()


class JobBoardUpdateForm(BaseModel):
    slug: str | None = Field(None, min_length=3, max_length=20)
    logo: UploadFile | None = Field(None)


def generate_random_string(length):
    """Generates a random string of specified length using letters and digits."""
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for i in range(length))
    return random_string


UPLOAD_DIR = "uploads"


def upload_file(bucket_name, path: str, contents, content_type):
    file_name = ".".join([generate_random_string(20), path.split(".")[-1]])
    if settings.PRODUCTION:
        response = supabase.storage.from_(bucket_name).upload(
            file_name, contents, {"content-type": content_type, "upsert": "true"}
        )
        return f"{str(settings.SUPABASE_URL)}/storage/v1/object/public/{response.full_path}"
    else:
        os.makedirs(os.path.join(UPLOAD_DIR, bucket_name), exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, bucket_name, file_name)
        with open(file_path, "wb") as f:
            f.write(contents)
        return f"/{UPLOAD_DIR}/{bucket_name}/{file_name}"


# curl -X POST -H "Content-Type: multipart/form-data" -F 'slug=google' http://localhost:8000/api/job-board
# curl -X POST -H "multipart/form-data" -F 'slug=acme' -F 'logo=@./acme-capital.png' http://localhost:8000/api/job-boards
@app.post("/api/job-boards")
async def api_create_new_job_board(
    request: Request,
    job_board_form: Annotated[JobBoardForm, Form()],
    db: Session = Depends(get_db),
):
    token = request.cookies.get("admin_session")
    if not is_admin(token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission deny"
        )

    logo_contents = await job_board_form.logo.read()
    file_url = upload_file(
        "company-logos",
        job_board_form.logo.filename,
        logo_contents,
        job_board_form.logo.content_type,
    )

    db_jobBoard = JobBoard(
        slug=job_board_form.slug,
        logo_url=file_url,
    )
    db.add(db_jobBoard)
    db.commit()
    db.refresh(db_jobBoard)
    return {"slug": job_board_form.slug, "file_url": file_url}


@app.get("/api/job-boards/{id}/job-posts")
async def api_job_boards_posts(id: int, db: Session = Depends(get_db)):
    jobPosts = db.query(JobPost).filter(JobPost.job_board_id == id).all()
    return jobPosts


@app.get("/api/job-boards/{slug}")
async def api_job_boards_posts_by_slug(slug: str, db: Session = Depends(get_db)):
    jobPosts = (
        db.query(JobPost).join(JobPost.job_board).filter(JobBoard.slug == slug).all()
    )
    return jobPosts


@app.put("/api/job-boards/{id}")
async def api_update_job_board(
    id: int,
    job_board_form: Annotated[JobBoardUpdateForm, Form()],
    db: Session = Depends(get_db),
):
    # print(job_board_form.logo.filename)
    # if job_board_form.logo.filename:
    if job_board_form.logo is not None and job_board_form.logo.filename:
        logo_contents = await job_board_form.logo.read()
        file_url = upload_file(
            "company-logos",
            job_board_form.logo.filename,
            logo_contents,
            job_board_form.logo.content_type,
        )

    db_jobBoard = db.get(JobBoard, id)
    if not db_jobBoard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job board not found"
        )

    if job_board_form.slug:
        db_jobBoard.slug = job_board_form.slug
    # if job_board_form.logo.filename:
    if job_board_form.logo is not None and job_board_form.logo.filename:
        db_jobBoard.logo_url = file_url
    db.commit()
    db.refresh(db_jobBoard)
    return db_jobBoard


@app.delete("/api/job-boards/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def api_delete_job_board(id: int, db: Session = Depends(get_db)):
    db_jobBoard = db.get(JobBoard, id)
    if not db_jobBoard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job board not found"
        )
    db.delete(db_jobBoard)
    db.commit()
    return None


class JobPostForm(BaseModel):
    job_board_id: int = Field(...)
    title: str = Field(..., min_length=1, max_length=50)
    description: str = Field(...)


@app.get("/api/job-posts/{id}")
async def api_job_post_by_id(id: int, db: Session = Depends(get_db)):
    jobPost = db.get(JobPost, id)
    return jobPost


@app.get("/api/job-posts/{id}/job-applications")
async def api_job_posts_applications(id: int, db: Session = Depends(get_db)):
    jobApplications = (
        db.query(JobApplication).filter(JobApplication.job_post_id == id).all()
    )
    return jobApplications


@app.post("/api/job-posts")
async def api_create_new_job_post(
    job_post_form: Annotated[JobPostForm, Form()], db: Session = Depends(get_db)
):
    db_jobBoard = (
        db.query(JobBoard).filter(JobBoard.id == job_post_form.job_board_id).first()
    )
    if not db_jobBoard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job board not found"
        )

    db_jobPost = JobPost(
        title=job_post_form.title,
        description=job_post_form.description,
        job_board_id=job_post_form.job_board_id,
        status="open",
    )
    db.add(db_jobPost)
    db.commit()
    db.refresh(db_jobPost)
    return db_jobPost


class JobReviewForm(BaseModel):
    description: str = Field(...)


@app.post("/api/review-job-description")
async def api_review_job_description(
    job_review_form: Annotated[JobReviewForm, Form()],
) -> ReviewedApplication:
    result = review_application(job_description=job_review_form.description)
    return result


@app.get("/api/job-posts/{job_post_id}/recommend")
async def api_recommend_resume(
    job_post_id: int,
    db: Session = Depends(get_db),
    vector_store: QdrantVectorStore = Depends(get_vector_store),
):
    db_job_post = db.get(JobPost, job_post_id)
    if not db_job_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job post not found"
        )
    result = get_recommendatation(
        job_description=db_job_post.description, vector_store=vector_store
    )
    db_job_application = db.get(JobApplication, result.metadata["_id"])
    return db_job_application


@app.post("/api/job-posts/{job_post_id}/close")
async def api_close_job_application(job_post_id: int, db: Session = Depends(get_db)):
    db_jobApplication = db.get(JobPost, job_post_id)
    db_jobApplication.status = "close"
    db.commit()
    db.refresh(db_jobApplication)
    return db_jobApplication


class JobApplicationForm(BaseModel):
    job_post_id: int = Field(...)
    first_name: str = Field(..., min_length=1, max_length=30)
    last_name: str = Field(..., min_length=1, max_length=30)
    email: str = Field(..., min_length=1, max_length=30)
    resume: UploadFile = Field(...)


@app.get("/api/job-applications")
async def api_job_applications(db: Session = Depends(get_db)):
    jobApplications = db.query(JobApplication).order_by(JobApplication.id).all()
    return jobApplications


def evaluate_resume(resume_content, job_post_description, job_application_id):
    resume_raw_text = extract_text_from_pdf_bytes(resume_content)
    ai_evaluation = evaluate_resume_with_ai(resume_raw_text, job_post_description)
    with get_db_session() as session:
        evaluation = JobApplicationAIEvaluation(
            job_application_id=job_application_id,
            overall_score=ai_evaluation["overall_score"],
            evaluation=ai_evaluation,
        )
        session.add(evaluation)
        session.commit()


@app.post("/api/job-applications")
async def api_create_new_job_application(
    job_application_form: Annotated[JobApplicationForm, Form()],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    vector_store: QdrantVectorStore = Depends(get_vector_store),
):
    resume_contents = await job_application_form.resume.read()
    file_url = upload_file(
        "application-resumes",
        job_application_form.resume.filename,
        resume_contents,
        job_application_form.resume.content_type,
    )

    db_jobPost = db.get(JobPost, job_application_form.job_post_id)
    if not db_jobPost:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job post not found"
        )
    elif db_jobPost.status == "close":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job post is already closed",
        )

    db_jobApplication = JobApplication(
        first_name=job_application_form.first_name,
        last_name=job_application_form.last_name,
        email=job_application_form.email,
        resume_url=file_url,
        job_post_id=job_application_form.job_post_id,
    )
    db.add(db_jobApplication)
    db.commit()
    db.refresh(db_jobPost)
    db.refresh(db_jobApplication)

    background_tasks.add_task(
        send_email,
        db_jobApplication.email,
        "Acknowledgement",
        "Wh have received your job application",
    )

    background_tasks.add_task(
        evaluate_resume, resume_contents, db_jobPost.description, db_jobApplication.id
    )

    background_tasks.add_task(
        ingest_resume_for_recommendation,
        resume_contents,
        db_jobApplication.resume_url,
        db_jobApplication.id,
        vector_store,
    )

    return db_jobApplication


# Self Training
from suggest_weekend import suggest_chennai_weekend


class WeekendForm(BaseModel):
    target_date: date = Field(...)
    user_profile: str = Field(...)


@app.post("/api/suggestion/chennai-weekend")
async def api_suggest_chennai_weekend(
    weekend_form: Annotated[WeekendForm, Form()], background_tasks: BackgroundTasks
):
    result = suggest_chennai_weekend(
        target_date=str(weekend_form.target_date),
        user_profile=weekend_form.user_profile,
    )
    return result


# Mount Static File for Jobify
if not settings.PRODUCTION:
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Static Frontend Server
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/static-job-board.html")
async def static_job_board():
    return HTMLResponse(content="<h3>Hello</h3>")


# Routing for npm run build
# app.mount("/app", StaticFiles(directory="frontend/dist"), name="vite")


# Server Side Routing
app.mount("/assets", StaticFiles(directory="frontend/build/client/assets"))


@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    indexFilePath = os.path.join("frontend", "build", "client", "index.html")
    return FileResponse(path=indexFilePath, media_type="text/html")


# =====================================================
# ATS Part
requiredPersonnel = {
    "departments": [
        {"id": "D001", "name": "Human Resources"},
        {"id": "D002", "name": "Engineering"},
        {"id": "D003", "name": "Marketing"},
    ],
    "jobs": [
        {"jobId": "J001", "title": "HR Specialist", "departmentId": "D001"},
        {"jobId": "J002", "title": "Software Engineer", "departmentId": "D002"},
        {"jobId": "J003", "title": "Frontend Developer", "departmentId": "D002"},
        {"jobId": "J004", "title": "Marketing Coordinator", "departmentId": "D003"},
    ],
}


@app.get("/ats/required-personnel/{slug}")
async def department_required_personnel(slug: str):
    try:
        jobs = [job for job in requiredPersonnel["jobs"] if job["departmentId"] == slug]
        return jobs
    except KeyError:
        raise HTTPException(status_code=404, detail="Department job not found")


# =====================================================
