import math
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session

from app.models import Job
from app.schemas import JobCreate, JobPublic, JobUpdate, UserPublic, JobList
from app.dependencies import get_session, get_current_active_user, check_demo_user


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=JobList)
def read_jobs(
    *,
    current_user: Annotated[UserPublic, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
    search: str = "",
    sort: Literal["oldest", "newest", "a-z", "z-a"] = "newest",
    job_type: Literal["full-time", "part-time", "internship"] | None = None,
    job_status: Literal["pending", "interview", "declined"] | None = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, le=10),
):
    jobs_statement = select(Job).where(
        Job.user_id == current_user.id,
        or_(Job.position.like(f"%{search}%"), Job.company.like(f"%{search}%")),
    )
    total_statement = select(func.count().label("count")).where(
        Job.user_id == current_user.id,
        or_(Job.position.like(f"%{search}%"), Job.company.like(f"%{search}%")),
    )

    if sort == "oldest":
        jobs_statement = jobs_statement.order_by(Job.create_date)
    elif sort == "newest":
        jobs_statement = jobs_statement.order_by(Job.create_date.desc())
    elif sort == "a-z":
        jobs_statement = jobs_statement.order_by(Job.position)
    elif sort == "z-a":
        jobs_statement = jobs_statement.order_by(Job.position.desc())

    if job_type:
        jobs_statement = jobs_statement.where(Job.type == job_type)
        total_statement = total_statement.where(Job.type == job_type)
    if job_status:
        jobs_statement = jobs_statement.where(Job.status == job_status)
        total_statement = total_statement.where(Job.status == job_status)

    jobs_statement = jobs_statement.offset((page - 1) * per_page).limit(per_page)

    jobs = session.scalars(jobs_statement).all()
    total = session.scalar(total_statement)

    return {
        "jobs": jobs,
        "page": page,
        "pages": math.ceil(total / per_page),
        "total": total,
    }


@router.post("/", response_model=JobPublic)
def create_job(
    *,
    current_user: Annotated[UserPublic, Depends(check_demo_user)],
    session: Session = Depends(get_session),
    job: JobCreate,
):
    db_job = Job(**job.model_dump(), user_id=current_user.id)
    session.add(db_job)
    session.commit()
    session.refresh(db_job)
    return db_job


@router.get("/{job_id}", response_model=JobPublic)
def read_job(
    *,
    current_user: Annotated[UserPublic, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
    job_id: int,
):
    statement = select(Job).where(Job.id == job_id, Job.user_id == current_user.id)
    results = session.scalars(statement)
    job = results.first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    return job


@router.patch("/{job_id}", response_model=JobPublic)
def update_job(
    *,
    current_user: Annotated[UserPublic, Depends(check_demo_user)],
    session: Session = Depends(get_session),
    job_id: int,
    job: JobUpdate,
):
    statement = select(Job).where(Job.id == job_id, Job.user_id == current_user.id)
    results = session.scalars(statement)
    db_job = results.first()
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )

    job_data = job.model_dump()
    for key, value in job_data.items():
        setattr(db_job, key, value)
    session.add(db_job)
    session.commit()
    session.refresh(db_job)
    return db_job


@router.delete("/{job_id}")
def delete_job(
    *,
    current_user: Annotated[UserPublic, Depends(check_demo_user)],
    session: Session = Depends(get_session),
    job_id: int,
):
    statement = select(Job).where(Job.id == job_id, Job.user_id == current_user.id)
    results = session.scalars(statement)
    job = results.first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    session.delete(job)
    session.commit()
    return {"ok": True}
