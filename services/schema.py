from typing import List

from pydantic import BaseModel, Field


class AlignmentPoint(BaseModel):
    policy_requirement: str = Field(description="A specific requirement or priority drawn from the policy text.")
    emp_feature: str = Field(description="The specific EMP feature that relates to it, drawn only from the supplied EMP description.")
    explanation: str = Field(description="1-3 sentences explaining how the feature supports the requirement.")


class FactSheet(BaseModel):
    title: str = Field(description='e.g. "How EMP Supports <Policy Name>"')
    jurisdiction: str = Field(description='e.g. "New South Wales, Australia"')
    policy_reference: str = Field(description="A short citation of the policy as understood from the supplied input.")
    policy_summary: str = Field(description="2-4 sentence plain-English summary of the policy, grounded only in the supplied policy text.")
    alignment_points: List[AlignmentPoint] = Field(description="4 to 6 alignment points.")
    evidence_section: str = Field(description="A paragraph on EMP's self-reported outcomes, using only the facts supplied.")
    scope_considerations: str = Field(description="A note on EMP's current year-level coverage and rollout timeline, as supplied.")
