from pydantic import BaseModel, Field

class CreditApplication(BaseModel):
    income: float = Field(..., gt=0, description="Applicant's annual income in USD")
    credit_score: int = Field(..., ge=300, le=850, description="FICO Credit Score (300-850)")
    dti_ratio: float = Field(..., ge=0, le=1, description="Debt-to-Income Ratio (0.0 to 1.0)")