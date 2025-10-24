from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class PredictRequest (BaseModel):
    # Example: {"Income": 112.0, "CCAvg": 3.2, "Education_Graduate": 1, ...}
    features: Dict[str, float] = Field(..., description="Preprocessed numeric features keyed by column name")

class PredictResponse(BaseModel):
    probability: float
    decision_standard: int
    decision_high_recall: int
    decision_vip_promo: int
    thresholds: Dict[str, float]