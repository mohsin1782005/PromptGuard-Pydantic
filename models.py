from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import List, Optional

class UserProfile(BaseModel):
    user_id: int = Field(..., alias="u_id")
    tier: str = "free"

class AIPromptRequest(BaseModel):
    # Data Fields
    user: UserProfile
    prompt: str = Field(..., min_length=10, max_length=1000)
    model_name: str = Field(default="gpt-4o")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    is_private: bool = False
    cloud_storage_path: Optional[str] = None
    tags: List[str] = []

    # Field Validator: Restricted Model List
    @field_validator('model_name')
    @classmethod
    def validate_model_name(cls, v: str) -> str:
        allowed = ["gpt-4o", "claude-3-opus", "gemini-1.5-pro"]
        if v not in allowed:
            raise ValueError(f"Model '{v}' is unsupported. Choose from {allowed}")
        return v

    # Model Validator: Security Logic
    @model_validator(mode='after')
    def check_privacy_rules(self) -> 'AIPromptRequest':
        if self.is_private and self.cloud_storage_path:
            raise ValueError("Security Violation: Private prompts cannot have a cloud path!")
        return self

    # Computed Field: Business Logic
    @computed_field
    @property
    def complexity(self) -> str:
        words = len(self.prompt.split())
        return "High" if words > 50 else "Medium" if words > 10 else "Low"