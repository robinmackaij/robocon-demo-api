*** Settings ***
Resource            variables.resource
Library             OpenApiDriver
...                     source=${HOST}/openapi.json
...                     origin=${HOST}
...                     ignored_paths=${IGNORED_PATHS}
...                     response_validation=DISABLED
...                     mappings_path=${ROOT}/excercises/mappings.py
...                     extra_headers=${EXTRA_HEADERS}

Test Template       Validate Using Test Endpoint Keyword


*** Test Cases ***
Test Endpoint for ${method} on ${path} where ${status_code} is expected


*** Keywords ***
Validate Using Test Endpoint Keyword
    [Arguments]    ${path}    ${method}    ${status_code}
    IF    $status_code == "404"
        Test Invalid Url    path=${path}    method=${method}
    ELSE
        Test Endpoint
        ...    path=${path}    method=${method}    status_code=${status_code}
    END
