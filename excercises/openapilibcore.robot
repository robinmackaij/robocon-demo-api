*** Settings ***
Resource            variables.resource
Library             Collections
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

Update Generated Post Data With Specific Value
    ${author_requestdata}=    Get Request Data    /authors    POST
    ${author_dto}=    Set Variable    ${author_requestdata.dto}
    ${author_name}=    Set Variable    ${author_dto.name}
    Log    ${author_name}
    ${dict}=    Set Variable    ${author_dto.as_dict()}
    Log    ${dict}
    ${updated_dict}=    Set To Dictionary    ${dict}    name=our test user name
    Log    ${updated_dict}
    ${url}=    Get Valid Url    endpoint=/authors    method=post
    ${response}=    Authorized Request
    ...    url=${url}
    ...    method=post
    ...    params=${author_requestdata.params}
    ...    headers=${author_requestdata.headers}
    ...    json_data=${updated_dict}
    Should Be Equal As Strings    ${response.json()}[name]    our test user name
