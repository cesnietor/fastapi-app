from fastapi import status
from fastapi.responses import JSONResponse
from .models import CheckCredPolicyRequest, CheckCredPolicyResponse, Message

MESSAGE_REJECT = "REJECT"
MESSAGE_ACCEPT = "ACCEPT"
REASON_LOW_INCOME = "LOW_INCOME"
REASON_HIGH_DEBT_FOR_INCOME = "HIGH_DEBT_FOR_INCOME"
REASON_PAYMENT_REMARKS_12M = "PAYMENT_REMARKS_12M"
REASON_PAYMENT_REMARKS = "PAYMENT_REMARKS"
REASON_UNDERAGE = "UNDERAGE"
REASON_OK = "OK"

# Custom policy check response definitions for OpenAPI schemas
policy_check_responses = {
    status.HTTP_404_NOT_FOUND: {
        "model": Message,
        "description": "Policy Not Found"
    },
    status.HTTP_200_OK: {
        "model": CheckCredPolicyResponse,
        "description": "Request valid"
    },
}


def policy_0(req: CheckCredPolicyRequest):
    """
        Performs the following checks:
            - income
            - debt
            - payment remarks
            - age
        If the request passes the policy, it returns an `ACCEPT`
        CheckCredPolicyResponse, else, it will return a `REJECT`
        CheckCredPolicyResponse, both with the corresponding 
        message and reasons.
    """

    min_required_income = 500
    max_debt = req.customer_income*0.5
    max_payment_remarks_12m = 0
    max_payment_remarks = 1
    min_age = 18

    reject_reasons = []
    if req.customer_income < min_required_income:
        reject_reasons.append(REASON_LOW_INCOME)
    if req.customer_debt > max_debt:
        reject_reasons.append(REASON_HIGH_DEBT_FOR_INCOME)
    if req.payment_remarks_12m > max_payment_remarks_12m:
        reject_reasons.append(REASON_PAYMENT_REMARKS_12M)
    if req.payment_remarks > max_payment_remarks:
        reject_reasons.append(REASON_PAYMENT_REMARKS)
    if req.customer_age < min_age:
        reject_reasons.append(REASON_UNDERAGE)

    # return reject reasons in a single comma-separated string
    if len(reject_reasons) > 0:
        return policy_check_response_to_json(
            status_code=status.HTTP_200_OK,
            message=MESSAGE_REJECT,
            reason=",".join(reject_reasons),
        )
    else:
        return policy_check_response_to_json(
            status_code=status.HTTP_200_OK,
            message=MESSAGE_ACCEPT,
            reason=REASON_OK,
        )


def policy_check_response_to_json(status_code: int, message: str, reason: str = None):
    """
        Returns a CheckCredPolicyResponse as JSONResponse
    """
    return JSONResponse(
        status_code=status_code,
        content=CheckCredPolicyResponse(
            message=message,
            reason=reason,
        ).dict()
    )


def not_found_json_response(req: CheckCredPolicyRequest):
    """
        Returns a HTTP 404 json response
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=Message(message="Policy Not Found").dict()
    )
