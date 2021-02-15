from pydantic import BaseModel
from typing import Optional


class CheckCredPolicyRequest(BaseModel):
    """
        Request model needed to validate a credit
        policy
    """
    # mandatory parameters
    customer_income: float
    customer_debt: float
    payment_remarks_12m: int  # float and str will be cast to integer
    payment_remarks: int
    customer_age: int


class CheckCredPolicyResponse(BaseModel):
    """
        Credit policy validation results used
        when the request didn't pass the policy checks
        both `message` and `reason` are optional.
    """
    message: Optional[str]
    reason: Optional[str]


class Message(BaseModel):
    """
        Miscelaneus Message model
    """
    message: str
