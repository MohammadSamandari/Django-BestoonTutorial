/submit/expense/
    POST, returns a json
    input : date (optional), text, amount, token
    output: status:ok

/submit/income
    POST, returna a json
    input: date(optional), text, amount, token
    output: status:ok

/accounts/register/
    step1:
        POST
        input: username,email,password
        output: status: ok
    step2:
        GET
        input: email,code
        output: status: ok (shows the token)

    NOTE: because POSTMAN doesn't work anymore, it merged the two steps together.

/q/generralstat/
    POST: returns a json
    input: fromdate (optional), todate(optional), token
    output: json from some general stat related to this user.