*** Settings ***
Resource            variables.resource
Library             String
Library             OpenApiLibCore
...                    source=${HOST}/openapi.json
...                    origin=${HOST}


*** Test Cases ***
Get A Random Author's Name
    ${url}=    Get Valid Url    endpoint=/authors/{author_id}    method=GET
    ${response}=    Authorized Request    url=${url}    method=GET
    Should Be Equal As Integers    ${response.status_code}    200
    Should Be String    ${response.json()}[name]

