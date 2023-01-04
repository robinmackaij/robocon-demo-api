*** Settings ***
Resource    variables.resource
Library     REST    ${HOST}


*** Test Cases ***
Get First Author's Name
    GET    /authors/
    ${author_id}=    Output      $[0].id

    GET    /authors/${author_id}
    Integer    response status    200
    String    response body name

