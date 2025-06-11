from typing import List, Optional
from pydantic import BaseModel

class PlanStep(BaseModel):
    agent: str
    task: str

class Plan(BaseModel):
    steps: List[PlanStep]

class SelectedPlan(BaseModel):
    planner_name: str
    reasoning: Optional[str] = None

class PlanEvaluation(BaseModel):
    change_plan: bool
    suggested_plan: Optional[str] = None
    confidence: Optional[float] = None
    reasoning: Optional[str] = None
