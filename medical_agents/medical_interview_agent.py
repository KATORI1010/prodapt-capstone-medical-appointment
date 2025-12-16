from pathlib import Path

from openai.types.shared import Reasoning
from agents import Agent, ModelSettings

from medical_agents.tools import load_prompt_md, update_intake_form, report_completion
from medical_agents.review_interview_agent import review_interview_agent


INTERVIEW_PROMPT = load_prompt_md("./prompts/medical_interview_prompt.md")


def medical_interview_agent(model: str) -> Agent:
    return Agent(
        name="Medical Interview Orchestrate Agent",
        instructions=INTERVIEW_PROMPT,
        model=model,
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium"), verbosity="low"
        ),
        tools=[
            update_intake_form,
            review_interview_agent.as_tool(
                tool_name="review_interview_agent",
                tool_description="""
                    問診内容に不十分な部分が無いか確認するレビュアーエージェントです。
                    問診票の内容を受け渡してレビューを依頼して下さい。
                    結果として合否と総括コメントを受け取れます。
                """,
            ),
            report_completion,
        ],
    )
