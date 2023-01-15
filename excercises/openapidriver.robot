*** Settings ***
Resource            variables.resource
Library             OpenApiDriver
...                    source=${HOST}/openapi.json
...                    origin=${HOST}
...                    response_validation=DISABLED
Test Template        Validate Using Test Endpoint Keyword


*** Test Cases ***
Test Endpoint for ${method} on ${endpoint} where ${status_code} is expected

*** Keywords ***
Validate Using Test Endpoint Keyword
    [Arguments]    ${endpoint}    ${method}    ${status_code}
    IF    $status_code == "404"
        Test Invalid Url    endpoint=${endpoint}    method=${method}
    ELSE
        Test Endpoint
        ...    endpoint=${endpoint}    method=${method}    status_code=${status_code}
    END

