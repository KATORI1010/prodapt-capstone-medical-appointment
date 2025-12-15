from pathlib import Path

from openai.types.shared import Reasoning
from agents import Agent, ModelSettings

from medical_agents.tools import update_intake_form, report_completion
from medical_agents.review_interview_agent import review_interview_agent


def load_prompt_md(relative_path: str) -> str:
    base_dir = Path(__file__).resolve().parent
    prompt_path = base_dir / relative_path
    return Path(prompt_path).read_text(encoding="utf-8-sig")


# ORCHESTRATE_PROMPT = load_prompt_md("./prompts/orchestrate_interview_prompt.md")
ORCHESTRATE_PROMPT = load_prompt_md("./prompts/test.md")


def medical_interview_agent(model: str) -> Agent:
    return Agent(
        name="Medical Interview Orchestrate Agent",
        instructions=ORCHESTRATE_PROMPT,
        model=model,
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium"), verbosity="low"
        ),
        tools=[
            # read_medical_interview,
            # update_medical_interview,
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
