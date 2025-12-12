import os
from typing import List, Literal
from dotenv import load_dotenv
import json
import truststore  # SSL証明書エラーの対応のため

from pydantic import BaseModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from braintrust import init_logger, traced
from braintrust_langchain import BraintrustCallbackHandler, set_global_handler


from config import settings

load_dotenv()
truststore.inject_into_ssl()

# Tracing to Braintrust
init_logger(project="Prodapt", api_key=os.environ.get("BRAINTRUST_API_KEY"))
set_global_handler(BraintrustCallbackHandler())


class ReviewedApplication(BaseModel):
    overall_summary: str
    revised_description: str


class JDAnalysis(BaseModel):
    unclear_sections: List[str]
    jargon_terms: List[str]
    biased_language: List[str]
    missing_information: List[str]
    overall_summary: str


class RewrittenSection(BaseModel):
    category: Literal["clarity", "jargon", "bias", "missing_information"]
    original_text: str
    issue_explanation: str
    improved_text: str


class JDRewriteOutput(BaseModel):
    rewritten_sections: List[RewrittenSection]


ANALYSIS_BASE_PROMPT = """
You are an expert HR job description analyst specializing in inclusive hiring practices.
Analyze the provided job description for potential issues across these dimensions:

1. CLARITY: Identify sections with vague responsibilities, unclear expectations, or ambiguous requirements. Flag phrases like "various duties," "other tasks as assigned," or undefined acronyms.

2. JARGON: Flag unnecessarily technical language inappropriate for the role level. Consider whether terms would be understood by qualified candidates unfamiliar with internal terminology.

3. BIAS: Identify language that may discourage diverse candidates:
    - Gender-coded words (e.g., "rockstar," "ninja," "aggressive," "nurturing")
    - Age bias (e.g., "digital native," "recent graduate")
    - Exclusionary phrases (e.g., "culture fit," "work hard/play hard")
    - Excessive requirements (unnecessarily requiring degrees or years of experience)

4. MISSING INFORMATION: Note absent critical details:
    - Salary range or compensation structure
    - Work location/arrangement (remote/hybrid/onsite)
    - Reporting structure or team context
    - Clear distinction between required vs. preferred qualifications
    - Application process and timeline
    - Growth/development opportunities

5. SUMMARY: Provide 2-3 sentences describing overall quality and primary concerns.

For each issue, provide:
    - The specific problematic text (quote directly)
    - Why it's problematic
    - A suggested improvement (where applicable)


Analyze the following job description:

--- JOB DESCRIPTION ---
{job_description}
----------------------

Return ONLY valid JSON matching the provided schema.

{format_instructions}
"""


REWRITE_BASE_PROMPT = """
You are an expert HR editor specializing in rewriting job descriptions for clarity, inclusivity, and accessibility.

You will receive:
1. The original job description.
2. A structured analysis of issues found in Step 1.

Your task is to rewrite ONLY the problematic sections, not the entire job description.

For each identified issue:
- Include the original problematic text (quoted exactly)
- Include the category (clarity, jargon, bias, or missing_information)
- Provide an improved, inclusive alternative that preserves meaning
- Maintain neutral, professional tone
- Ensure suggestions follow inclusive hiring practices

Original Job Description:
-------------------------
{job_description}
-------------------------

Analysis Findings:
------------------
{analysis_result}
------------------

Return ONLY valid JSON matching the provided schema.
Do not write any prose outside JSON.

{format_instructions}
"""


FINALISE_BASE_PROMPT = """
You are an expert HR writer specializing in creating clear, concise, and inclusive job descriptions.

Your job is to produce the final polished version of the job description.

You will receive:
1. The original job description.
2. A list of rewritten sections (from Step 2).

Your tasks:
- Incorporate all improved rewritten sections into the original job description.
- Remove or replace the problematic text that was flagged in earlier steps.
- Maintain the original intent, structure, and role scope.
- Ensure clarity, inclusivity, and accessibility.
- Make tone consistent: professional, warm, and concise.
- Improve flow and readability where necessary.
- Do NOT invent new responsibilities, requirements, or benefits.

Original Job Description:
-------------------------
{job_description}
-------------------------

Rewritten Sections:
-------------------------
{rewrite_result}
-------------------------

Return ONLY the final polished job description as plain text. Do not include JSON.
"""


@traced(name="Review Job Description")
def review_application(job_description: str) -> ReviewedApplication:
    llm = ChatOpenAI(model="gpt-5.1-chat-latest")

    # Analysis --------------------
    analysis_output_parser = PydanticOutputParser(pydantic_object=JDAnalysis)

    analysis_prompt = PromptTemplate(
        template=ANALYSIS_BASE_PROMPT,
        input_variables=["job_description"],
        partial_variables={
            "format_instructions": analysis_output_parser.get_format_instructions()
        },
    )

    analysis_chain = analysis_prompt | llm | analysis_output_parser

    analysis_result = analysis_chain.invoke({"job_description": job_description})

    # Rewite --------------------
    rewrite_output_parser = PydanticOutputParser(pydantic_object=JDRewriteOutput)

    rewrite_prompt = PromptTemplate(
        template=REWRITE_BASE_PROMPT,
        input_variables=["job_description", "analysis_result"],
        partial_variables={
            "format_instructions": rewrite_output_parser.get_format_instructions()
        },
    )

    rewrite_chain = rewrite_prompt | llm | rewrite_output_parser

    rewrite_result = rewrite_chain.invoke(
        {
            "job_description": job_description,
            "analysis_result": analysis_result.model_dump_json(),
        }
    )

    # Finalize --------------------
    finalize_prompt = PromptTemplate(
        template=FINALISE_BASE_PROMPT,
        input_variables=["job_description", "rewrite_result"],
    )

    finalize_chain = finalize_prompt | llm

    finalize_result = finalize_chain.invoke(
        {
            "job_description": job_description,
            "rewrite_result": rewrite_result.model_dump_json(),
        }
    )

    return ReviewedApplication(
        overall_summary=analysis_result.overall_summary,
        revised_description=finalize_result.content,
    )


def get_vector_store() -> QdrantVectorStore:
    if settings.PRODUCTION:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large", api_key=settings.OPENAI_API_KEY
        )
        vector_store = QdrantVectorStore.from_existing_collection(
            url=str(settings.QDRANT_URL),
            api_key=settings.QDRANT_API_KEY,
            embedding=embeddings,
            collection_name="resumes",
        )
        return vector_store
    else:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large", api_key=settings.OPENAI_API_KEY
        )
        vector_store = QdrantVectorStore.from_existing_collection(
            embedding=embeddings, collection_name="resumes", path="qdrant_store"
        )
        return vector_store


def inmemory_vector_store():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large", api_key=settings.OPENAI_API_KEY
    )

    client = QdrantClient(":memory:")
    client.create_collection(
        collection_name="resumes",
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
    )
    vector_store = QdrantVectorStore(
        client=client, collection_name="resumes", embedding=embeddings
    )
    try:
        yield vector_store
    finally:
        client.close()


def ingest_resume(
    resume_content: str, filename: str, resume_id: int, vector_store: QdrantVectorStore
):
    document = Document(
        page_content=resume_content,
        metadata={
            "url": filename,
        },
    )
    vector_store.add_documents(
        [document],
        ids=[resume_id],
    )


def get_recommendatation(job_description: str, vector_store: QdrantVectorStore):
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})
    result = retriever.invoke(job_description)
    return result[0]


test_job_description = """
We’re seeking a Forward Deployed Engineer.
We want someone with 3+ years of software engineering experience with production systems.
They should be rockstar programmers and problem solvers.
They should have experience in a customer-facing technical role with a background in systems integration or professional services
"""

if __name__ == "__main__":
    result = review_application(test_job_description)
    print("\n\nOverall summary:")
    print(result.overall_summary)
    print("\n\nRevised Description:")
    print(result.revised_description)
