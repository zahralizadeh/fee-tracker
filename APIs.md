# /webservice/register
1.  POST,  returns a json
        input:  username, email, password
        output: status--->(ok/Fail), 
                message-->(activation-link / Email already exists. / Username already exists.)
2.  GET, returns a json
        input:  activationcode(questionstring)
        output: status--->(ok/Fail), 
                message-->(You successfully registered / Invalid activation code!!! / error in reading code, Empty request / Empty request)


# /webservice/login
POST, returns a json
input:  username(username/email), password
output: status--->(ok/Fail), 
        message-->(You successfully logged in. / Invalid username or password!)
        token---->token(optional)     


