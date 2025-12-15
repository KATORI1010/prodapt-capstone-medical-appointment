from typing import Annotated, Literal
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")


Text = Annotated[str, Field(min_length=1)]


# --- Symptom Entity ---
class Symptom(BaseSchema):
    name: Text = Field(description="症状名（例: 発熱、頭痛、咳、腹痛など）")
    detail: str | None = Field(default=None, description="補足（部位・性質など、短く）")
    onset: str | None = Field(
        default=None, description="いつから（例: 今日の朝、2日前）"
    )
    severity_0_10: Annotated[int, Field(ge=0, le=10)] | None = Field(
        default=None, description="その症状のつらさ（0〜10、不明なら省略）"
    )


# --- Medication Entity ---
class Medication(BaseSchema):
    name: Text = Field(description="薬の名前（分かる範囲。商品名/一般名どちらでも可）")
    dose: str | None = Field(default=None, description="用量（例: 10mg、1錠）")
    frequency: str | None = Field(default=None, description="頻度（例: 1日1回、頓服）")
    notes: str | None = Field(
        default=None, description="補足（例: お薬手帳なしで不明など）"
    )


# --- Allergy Entity ---
class Allergy(BaseSchema):
    allergen: Text = Field(description="原因（例: ペニシリン、卵、そば、造影剤など）")
    reaction: str | None = Field(
        default=None, description="反応（例: 発疹、息苦しさなど）"
    )
    severity: Literal["mild", "moderate", "severe", "unknown"] = Field(
        default="unknown", description="重症度（不明ならunknown）"
    )


# --- IntakeForm Schema ---
class IntakeForm(BaseSchema):
    version: int = Field(
        default=1, description="スキーマバージョン（将来変更に備える）"
    )
    updated_at: datetime | None = Field(
        default=None, description="最終更新（サーバ側で入れてもOK）"
    )

    # Patient demographics (prototype-friendly)
    full_name: str | None = Field(default=None, description="Patient full name.")
    age_years: Annotated[int, Field(ge=0, le=130)] | None = Field(
        default=None, description="Patient age in years."
    )
    sex: Literal["male", "female", "other", "unknown"] = Field(
        default="unknown", description="Patient sex."
    )

    # Patient's initial message (set once by server; NOT updatable by model)
    initial_patient_message: str | None = Field(
        default=None,
        description="The very first free-text message from the patient. Set by server only; do not modify via LLM tools.",
    )

    # Chief items
    visit_reason: str | None = Field(default=None, description="受診理由（主訴の要約）")
    duration: str | None = Field(default=None, description="持続期間（例: 2日前から）")
    severity_0_10: Annotated[int, Field(ge=0, le=10)] | None = Field(
        default=None, description="全体のつらさ（0〜10）"
    )

    symptoms: list[Symptom] = Field(default_factory=list, description="症状リスト")
    medications: list[Medication] = Field(
        default_factory=list, description="服用中の薬リスト"
    )
    allergies: list[Allergy] = Field(
        default_factory=list, description="アレルギーリスト"
    )

    notes: str | None = Field(default=None, description="その他メモ（自由記述）")


# --- IntakeForm Update Schema ---
class IntakeFormPatch(BaseSchema):
    visit_reason: str | None = None
    duration: str | None = None
    severity_0_10: Annotated[int, Field(ge=0, le=10)] | None = None

    symptoms: list[Symptom] | None = None
    medications: list[Medication] | None = None
    allergies: list[Allergy] | None = None

    notes: str | None = None
