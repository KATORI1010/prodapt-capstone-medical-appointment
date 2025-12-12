import json
from openai import OpenAI

from config import settings

client = OpenAI(api_key = settings.OPENAI_API_KEY)

resume_eval_prompt = """
You are an expert hiring screener. Given the candidate resume text and a job description, evaluate candidate's fit.

Inputs (do not invent facts):
- RESUME_TEXT: {0}
- JOB_DESC: {1}

Return a JSON object with these fields:
{
  "overall_score": integer 0-100,  
  "strengths": [strings],         // 3 most important strengths
  "gaps": [strings],              // 3 main gaps or risks
  "match_by_section": {           // short mapping of job sections to match info
    "required_skills": "match summary",
    "experience_years": "match summary",
    "education": "match summary"
  },
  "rewrite_snippet": "one paragraph resume intro tailored to the job (50-70 words)",
  "actionable_recommendations": [strings]  // 3-5 concrete edits or next steps
}

Be concise. Use the resume text only for facts; do not hallucinate experience or dates. If the resume is very long, summarize conservatively.
"""


def build_system_and_user_messages(resume_text: str, job_desc: str):
    prompt = resume_eval_prompt.replace("{0}", resume_text).replace("{1}", job_desc)
    return [
        {"role": "system", "content": "You are a helpful, neutral, accurate recruiter assistant."},
        {"role": "user", "content": prompt}
    ]

def evaluate_resume_with_ai(resume_text: str, job_desc: str, model="gpt-4o-mini", temperature=0):
    messages = build_system_and_user_messages(resume_text, job_desc)
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=1000
    )
    return json.loads(resp.choices[0].message.content.strip())
