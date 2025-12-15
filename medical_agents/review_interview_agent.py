from pydantic import BaseModel, Field
from openai.types.shared import Reasoning
from agents import Agent, ModelSettings, WebSearchTool

from medical_agents.tools import report_progress


class ReviewInterviewOutput(BaseModel):
    review_judge: bool = Field(
        ..., description="問診票の合否結果(合格: True、不合格: False)"
    )
    overall_comment: str = Field(
        ..., description="レビューの総括コメント(不合格の場合は理由を記載)"
    )


review_interview_agent = Agent(
    name="Review Interview Agent",
    instructions="""
    あなたは医療のエキスパートで病院の問診票のレビュアーです。
    患者さんとの問診を担当するAIエージェントから問診表の内容を受け取ってレビューを行います。
    
    ## 処理内容
    1. 初めにツール「report_progress」を実行してレビュー中であることを通知して下さい。
    2. 問診担当AIエージェントから受け取った問診票の内容を確認する。<br>
       **問診票の内容が渡されていない場合は提出するようにすぐに差し戻して下さい。**
    3. 問診の内容が十分か、追加質問が必要かどうかを確認する。
    4. 結果をまとめて問診担当AIエージェントに返却する。
    
    ## レビュー観点
    - 以下の観点で問診の内容に**不完全**や**矛盾**した部分が無いか確認する。
        - 受診の理由
        - 症状
        - 持続期間
        - 重症度
        - 服用中の薬
        - アレルギー
    - 問診の内容を受けて医療のエキスパートとして追加確認が必要な内容が無いか確認する。
    """,
    model="gpt-5-mini",
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="medium"), verbosity="medium"
    ),
    tools=[report_progress, WebSearchTool()],
    output_type=ReviewInterviewOutput,
)
