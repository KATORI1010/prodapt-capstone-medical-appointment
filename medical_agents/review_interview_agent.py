from pydantic import BaseModel, Field
from openai.types.shared import Reasoning
from agents import Agent, ModelSettings, WebSearchTool

from medical_agents.tools import load_prompt_md, report_progress, read_intake_form


class ReviewInterviewOutput(BaseModel):
    review_judge: bool = Field(
        ..., description="問診票の合否結果(合格: True、不合格: False)"
    )
    overall_comment: str = Field(
        ..., description="レビューの総括コメント(不合格の場合は理由を記載)"
    )


REVIEW_PROMPT = load_prompt_md("./prompts/review_interview_prompt.md")

review_interview_agent = Agent(
    name="Review Interview Agent",
    instructions=REVIEW_PROMPT,
    model="gpt-5.2",
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="medium"), verbosity="medium"
    ),
    tools=[report_progress, read_intake_form, WebSearchTool()],
    output_type=ReviewInterviewOutput,
)
