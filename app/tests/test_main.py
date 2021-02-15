from fastapi.testclient import TestClient
from fastapi import status
import pytest

from main import app

client = TestClient(app)

# Test cases for policy_0
# Data comes as [(<description>, <policy_id>, <request>, <expected_status_code>, <expected_reponse>),...]
testdata_policy_0 = [
    (
        "Pass all checks",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 100,
            "payment_remarks_12m": 0,
            "payment_remarks": 0,
            "customer_age": 20,
        },
        status.HTTP_200_OK,
        {'message': 'ACCEPT', 'reason': 'OK'},
    ),
    (
        "Customer income lower than 500",
        "0",
        {
            "customer_income": 499,
            "customer_debt": 100,
            "payment_remarks_12m": 0,
            "payment_remarks": 0,
            "customer_age": 20,
        },
        status.HTTP_200_OK,
        {'message': 'REJECT', 'reason': 'LOW_INCOME'},
    ),
    (
        "Customer income higher or equal than 500",
        "0",
        {
            "customer_income": 500,
            "customer_debt": 200,
            "payment_remarks_12m": 0,
            "payment_remarks": 0,
            "customer_age": 20,
        },
        status.HTTP_200_OK,
        {'message': 'ACCEPT', 'reason': 'OK'},
    ),
    (
        "Customer debt higher than half of customer income",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 501,
            "payment_remarks_12m": 0,
            "payment_remarks": 0,
            "customer_age": 20,
        },
        status.HTTP_200_OK,
        {'message': 'REJECT', 'reason': 'HIGH_DEBT_FOR_INCOME'},
    ),
    (
        "Customer debt higher than half of customer income 2",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 500.1,
            "payment_remarks_12m": 0,
            "payment_remarks": 0,
            "customer_age": 20,
        },
        status.HTTP_200_OK,
        {'message': 'REJECT', 'reason': 'HIGH_DEBT_FOR_INCOME'},
    ),
    (
        "Customer debt lower or equal than half of customer income 3",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 500,
            "payment_remarks_12m": 0,
            "payment_remarks": 0,
            "customer_age": 20,
        },
        status.HTTP_200_OK,
        {'message': 'ACCEPT', 'reason': 'OK'},
    ),
    (
        "Payment remarks 12 higher than 0",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 100,
            "payment_remarks_12m": 1,
            "payment_remarks": 0,
            "customer_age": 20,
        },
        status.HTTP_200_OK,
        {'message': 'REJECT', 'reason': 'PAYMENT_REMARKS_12M'},
    ),
    (
        "Payment remarks higher than 1",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 100,
            "payment_remarks_12m": 0,
            "payment_remarks": 2,
            "customer_age": 20,
        },
        status.HTTP_200_OK,
        {'message': 'REJECT', 'reason': 'PAYMENT_REMARKS'},
    ),
    (
        "Payment remarks lower or equal than 1",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 100,
            "payment_remarks_12m": 0,
            "payment_remarks": 1,
            "customer_age": 20,
        },
        status.HTTP_200_OK,
        {'message': 'ACCEPT', 'reason': 'OK'},
    ),
    (
        "Customer age lower than 18",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 100,
            "payment_remarks_12m": 0,
            "payment_remarks": 0,
            "customer_age": 17,
        },
        status.HTTP_200_OK,
        {'message': 'REJECT', 'reason': 'UNDERAGE'},
    ),
    (
        "Customer age higher or equal than 18",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 100,
            "payment_remarks_12m": 0,
            "payment_remarks": 0,
            "customer_age": 18,
        },
        status.HTTP_200_OK,
        {'message': 'ACCEPT', 'reason': 'OK'},
    ),
    (
        "Fail more than one checks",
        "0",
        {
            "customer_income": 499,
            "customer_debt": 250,
            "payment_remarks_12m": 1,
            "payment_remarks": 0,
            "customer_age": 17,
        },
        status.HTTP_200_OK,
        {'message': 'REJECT',
            'reason': 'LOW_INCOME,HIGH_DEBT_FOR_INCOME,PAYMENT_REMARKS_12M,UNDERAGE'},
    ),
    (
        "Policy id not found",
        "1",
        {
            "customer_income": 1000,
            "customer_debt": 100,
            "payment_remarks_12m": 0,
            "payment_remarks": 0,
            "customer_age": 20,
        },
        status.HTTP_404_NOT_FOUND,
        {"message": "Policy Not Found"},
    ),
    (
        "Customer income type validation",
        "0",
        {
            "customer_income": "thousand",
            "customer_debt": 500,
            "payment_remarks_12m": 0,
            "payment_remarks": 0,
            "customer_age": 20,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {'detail': [{'loc': ['body', 'customer_income'],
                     'msg': 'value is not a valid float',
                     'type': 'type_error.float'}]},
    ),
    (
        "Customer debt type validation",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": "thousand",
            "payment_remarks_12m": 0,
            "payment_remarks": 0,
            "customer_age": 20,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {'detail': [{'loc': ['body', 'customer_debt'],
                     'msg': 'value is not a valid float',
                     'type': 'type_error.float'}]},
    ),
    (
        "Payment Remarks 12m type validation (cast)",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 100,
            "payment_remarks_12m": 1.2,
            "payment_remarks": 0,
            "customer_age": 20,
        },
        status.HTTP_200_OK,
        {'message': 'REJECT', 'reason': 'PAYMENT_REMARKS_12M'},
    ),
    (
        "Payment Remarks 12m type validation",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 100,
            "payment_remarks_12m": "one",
            "payment_remarks": 0,
            "customer_age": 20,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {'detail': [{'loc': ['body', 'payment_remarks_12m'],
                     'msg': 'value is not a valid integer',
                     'type': 'type_error.integer'}]},
    ),
    (
        "Payment Remarks type validation (cast)",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 100,
            "payment_remarks_12m": 0,
            "payment_remarks": 2.2,
            "customer_age": 20,
        },
        status.HTTP_200_OK,
        {'message': 'REJECT', 'reason': 'PAYMENT_REMARKS'},
    ),
    (
        "Payment Remarks type validation",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 100,
            "payment_remarks_12m": 0,
            "payment_remarks": "one",
            "customer_age": 20,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {'detail': [{'loc': ['body', 'payment_remarks'],
                     'msg': 'value is not a valid integer',
                     'type': 'type_error.integer'}]},
    ),
    (
        "Customer age type validation (cast)",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 100,
            "payment_remarks_12m": 0,
            "payment_remarks": 0,
            "customer_age": 17.9,
        },
        status.HTTP_200_OK,
        {'message': 'REJECT', 'reason': 'UNDERAGE'},
    ),
    (
        "Customer age type validation",
        "0",
        {
            "customer_income": 1000,
            "customer_debt": 100,
            "payment_remarks_12m": 0,
            "payment_remarks": 0,
            "customer_age": "twenty",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {'detail': [{'loc': ['body', 'customer_age'],
                     'msg': 'value is not a valid integer',
                     'type': 'type_error.integer'}]},
    ),
]


@pytest.mark.parametrize("description, policy_id,req_payload,expected_status,expected_response", testdata_policy_0)
def test_check_policy_0(description, policy_id, req_payload, expected_status, expected_response):
    response = client.post(
        "/check_policy/{id}".format(id=policy_id), json=req_payload)
    assert response.status_code == expected_status
    assert response.json() == expected_response
