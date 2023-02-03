*** Settings ***
Resource    variables.resource
Library     OperatingSystem
Library     String
Library     RequestsLibrary


*** Test Cases ***
Get First Author's Name
    ${response}=    GET    url=${HOST}/authors
    ${authors_list}=    Set Variable    ${response.json()}
    ${author_id}=    Set Variable    ${authors_list[0]}[id]

    ${response}=    GET    url=${HOST}/authors/${author_id}
    Should Be String    ${response.json()}[name]
    Log    ${response.url}

Post Portrait
    ${response}=    GET    url=${HOST}/authors
    ${authors_list}=    Set Variable    ${response.json()}
    ${author_id}=    Set Variable    ${authors_list[0]}[id]

    ${portrait}=    Get File For Streaming Upload    path=${ROOT}/excercises/rf_logo.png
    ${files}=   Create Dictionary   uploaded_file=${portrait}   type=image/png
    ${query_params}=    Create Dictionary    replace=${TRUE}
    ${response}=    POST
    ...    url=${HOST}/authors/${author_id}/upload_portrait
    ...    files=${files}
    ...    params=${query_params}
