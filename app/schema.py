from pydantic import BaseModel
from typing import List


class MomsVerdict(BaseModel):
    summary_en: str
    summary_ar: str
    pros: List[str]
    cons: List[str]
    common_issues: List[str]
    recommended_age: str
    confidence_score: float
    uncertainty_flag: bool