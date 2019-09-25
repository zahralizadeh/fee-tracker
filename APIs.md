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

# /query/price
GET, returns a json
input:  location, area, rooms, offertype, age
output: status---->(ok/Fail/400 Bad Request), 
        message--->(You successfully logged in. / Invalid username or password!)(status=Fail)
        firstdata-> PropertyPredictResponse.firstdata(status=ok)
        lastdata--> PropertyPredictResponse.lastdata(status=ok)
        filter----> PropertyPredictResponse.filtering(status=ok)
        count-----> PropertyPredictResponse.recordcount(status=ok)
        answer----> PropertyPredictResponse.price1 , PropertyPredictResponse.price2(optional) (status=ok)
        
# /query/area

# /query/locationlist


