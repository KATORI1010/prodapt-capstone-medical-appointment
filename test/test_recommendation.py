from pathlib import Path

from ai import ingest_resume, get_recommendatation
from main import ingest_resume_for_recommendation
from models import JobBoard, JobPost


def test_should_embed_text_and_add_to_vector_db(vector_store):
    ingest_resume(
        "Siddharta\nSiddharta is an AI trainer", "siddharta.pdf", 1, vector_store
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})
    result = retriever.invoke("I am looking for an AI trainer")
    assert len(result) == 1
    assert "Siddharta" in result[0].page_content
    assert result[0].metadata["_id"] == 1


def test_background_task(vector_store):
    filename = "test/resumes/ProfileAndrewNg.pdf"
    with open(filename, "rb") as f:
        content = f.read()
    ingest_resume_for_recommendation(
        content, filename, resume_id=1, vector_store=vector_store
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})
    result = retriever.invoke("I am looking for an AI trainer")
    assert "Andrew" in result[0].page_content


def test_retrieval_quality(vector_store):
    for index, file in enumerate(list(Path("test/resumes").glob("*.pdf"))):
        with open(file, "rb") as f:
            content = f.read()
        ingest_resume_for_recommendation(
            content, file, resume_id=index, vector_store=vector_store
        )

    retriever = vector_store.as_retriever(search_kwargs={"k": 1})
    result = retriever.invoke("I am looking for an expert in AI")
    assert "Andrew" in result[0].page_content
    result = retriever.invoke("I am looking for an expert in Linux")
    assert "Linus" in result[0].page_content
    result = retriever.invoke("I am looking for an expert in Javascript")
    assert "Yuxi" in result[0].page_content
    result = retriever.invoke(
        "I am looking for a generalist who can work in python and typescript"
    )
    assert "Koudai" in result[0].page_content
    result = retriever.invoke("I am looking for a data journalist")
    assert "Simon" in result[0].page_content


def test_job_application_api(db_session, vector_store, client):
    job_board = JobBoard(slug="test", logo_url="http://example.com")
    db_session.add(job_board)
    db_session.commit()
    db_session.refresh(job_board)
    job_post = JobPost(
        title="AI Engineer",
        description="Need an AI Engineer",
        job_board_id=job_board.id,
    )
    db_session.add(job_post)
    db_session.commit()
    db_session.refresh(job_post)
    filename = "test/resumes/ProfileAndrewNg.pdf"
    post_data = {
        "first_name": "Siddharta",
        "last_name": "Govindaraj",
        "email": "siddharta@gmail.com",
        "job_post_id": job_post.id,
    }
    with open(filename, "rb") as f:
        response = client.post(
            "/api/job-applications",
            data=post_data,
            files={"resume": ("ProfileAndrewNg.pdf", f, "application/pdf")},
        )
    assert response.status_code == 200
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})
    result = retriever.invoke("I am looking for an expert in AI")
    assert "Andrew" in result[0].page_content
    assert result[0].metadata["_id"] == job_post.id


def test_get_recommendatation(vector_store):
    for index, file in enumerate(list(Path("test/resumes").glob("*.pdf"))):
        with open(file, "rb") as f:
            content = f.read()
        ingest_resume_for_recommendation(
            content, file, resume_id=index, vector_store=vector_store
        )

    result = get_recommendatation(
        job_description="I am looking for an expert in AI", vector_store=vector_store
    )
    assert "ProfileAndrewNg.pdf" in result.metadata["url"]
    result = get_recommendatation(
        job_description="I am looking for an expert in Linux", vector_store=vector_store
    )
    assert "ProfileLinusTorvalds.pdf" in result.metadata["url"]
    result = get_recommendatation(
        job_description="I am looking for an expert in Javascript",
        vector_store=vector_store,
    )
    assert "ProfileEvanYou.pdf" in result.metadata["url"]
    result = get_recommendatation(
        job_description="I am looking for a generalist who can work in python and typescript",
        vector_store=vector_store,
    )
    assert "ProfileKoudaiAono.pdf" in result.metadata["url"]
    result = get_recommendatation(
        job_description="I am looking for a data journalist", vector_store=vector_store
    )
    assert "ProfileSimonWillison.pdf" in result.metadata["url"]


def test_get_recommendatation_api(db_session, client):
    job_board = JobBoard(slug="test", logo_url="http://example.com")
    db_session.add(job_board)
    db_session.commit()
    db_session.refresh(job_board)
    job_post = JobPost(
        title="AI Engineer",
        description="I am looking for an expert in AI",
        job_board_id=job_board.id,
    )
    db_session.add(job_post)
    db_session.commit()
    db_session.refresh(job_post)

    test_resumes = [
        ("Andrew", "Ng", "andrewng@gmail.com", "ProfileAndrewNg.pdf"),
        ("Koudai", "Aono", "koxudaxi@gmail.com", "ProfileKoudaiAono.pdf"),
    ]
    for first_name, last_name, email, filename in test_resumes:
        post_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "job_post_id": job_post.id,
        }
        with open(f"test/resumes/{filename}", "rb") as f:
            response = client.post(
                "/api/job-applications",
                data=post_data,
                files={"resume": (filename, f, "application/pdf")},
            )

    # Recommendation API Test
    response = client.get(f"/api/job-posts/{job_post.id}/recommend")
    assert response.status_code == 200
    data = response.json()
    assert data['first_name'] == 'Andrew'
    assert data['last_name'] == 'Ng'
