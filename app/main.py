from fastapi import FastAPI, status, Request
from credit_policies.policies import policy_0, not_found_json_response, policy_check_responses
from credit_policies.models import CheckCredPolicyRequest, Message

app = FastAPI()


@app.post("/check_policy/{policy_id}",
          responses=policy_check_responses,
          tags=["policies"])
async def check_policy(policy_id: int, req: CheckCredPolicyRequest):
    """
        Validate a policy (policy_id) against the given information:
        - **customer_income**: given in EUR, required
        - **customer_debt**: given in EUR, required
        - **payment_remarks_12m**: required
        - **payment_remarks**: required
        - **customer_age**: required
    """
    # switch/case like implementation to select the credit policy to be used
    switcher = {
        0: policy_0,
        # more policies can be handled here...
    }
    func = switcher.get(policy_id, not_found_json_response)
    return func(req)
