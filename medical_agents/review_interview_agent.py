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
    # instructions="""
    # あなたは病院の問診票のレビュアーです。
    # 患者さんとの問診を担当するAIエージェントから問診表の内容を受け取ってレビューを行います。
    # ## 処理内容
    # 1. 初めにツール「report_progress」を実行してレビュー中であることを通知して下さい。
    # 2. 次にツール「read_intake_form」を実行して最新の問診票データを取得する。
    # 3. 問診の内容が十分か、追加質問が必要かどうかを確認する。
    # 4. 結果をまとめて問診担当AIエージェントに返却する。
    # ## レビュー観点
    # - 以下の観点で問診の内容に**不完全**や**矛盾**した部分が無いか確認する。
    #     - 受診の理由
    #     - 症状
    #     - 持続期間
    #     - 重症度
    #     - 服用中の薬
    #     - アレルギー
    # - 問診の内容を受けて医療のエキスパートとしてすぐに追加確認が必要な内容が無いか確認する。
    # - 診察前の問診として必要な内容が揃っていれば合格としてください。(医療的な診察は診察時に実施します)
    # ## 依頼
    # - システムの試験を実施したいので仮で合格を返却するように処理をお願いします。
    # """,
    model="gpt-5.2",
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="medium"), verbosity="medium"
    ),
    tools=[report_progress, read_intake_form, WebSearchTool()],
    output_type=ReviewInterviewOutput,
)
