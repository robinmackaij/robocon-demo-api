*** Settings ***
Resource    variables.resource
Library     String
Library     RequestsLibrary


*** Test Cases ***
Get First Author's Name
    ${response}=    GET    url=${HOST}/authors/
    ${authors_list}=    Set Variable    ${response.json()}
    ${author_id}=    Set Variable    ${authors_list[0]}[id]

    ${response}=    GET    url=${HOST}/authors/${author_id}
    Should Be String    ${response.json()}[name]

