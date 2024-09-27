*** Settings ***
Library     RequestsLibrary


*** Variables ***
${HOST}    http://127.0.0.1:8000


*** Test Cases ***
Post portrait
    ${author_id}=    Get id of first user

    ${portrait}=    Get file for streaming upload    path=${ROOT}/intro_robotframework/rf_logo.png
    ${files}=   Create dictionary   uploaded_file=${portrait}   type=image/png
    ${query_params}=    Create dictionary    replace=${TRUE}
    ${response}=    POST
    ...    url=${HOST}/authors/${author_id}/upload_portrait
    ...    files=${files}
    ...    params=${query_params}
    ...    expected_status=201


*** Keywords ***
Get id of first user
    ${response}=    GET    url=${HOST}/authors
    VAR    ${authors_list}    ${response.json()}
    VAR    ${author_id}    ${authors_list[0]}[id]
    RETURN    ${author_id}
