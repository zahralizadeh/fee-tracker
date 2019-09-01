import mysql.connector
import re
import requests

error = []

def test(location):
    link = 'https://www.ihome.ir/خرید-فروش/مسکونی/تهران/'
    link = link+location
    print (location)
    r = requests.get(link)
    print(r)
    if r.status_code == 200:
        return True
    else:
        return False


# initialize the connection to the database
cnx = mysql.connector.connect(user='root',password='',host='127.0.0.1',database='maktabkhooneh',charset="utf8", use_unicode=True)
cursor = cnx.cursor()

query = 'SELECT DISTINCT location FROM ihome2'
cursor.execute(query)
result = cursor.fetchall()
final_result = [list(i) for i in result]
#f= open("locations.txt","w+",encoding="utf-8")
f =open("locations.txt", "w+", encoding="utf-8")
e= open('error.txt','w+', encoding = 'utf-8')
for j in final_result:
        location = j[0].decode('utf8').replace('تهران','').replace('،','').replace(' ','-').strip()
        location = re.sub('^-', '',location)
        location = re.sub('-$', '',location)
        if test(location):
            location =location +'\n'
            f.write(location)
        else:
            location =location +'\n'
            e.write(location)  
f.close
e.close
#cursor.close()
#cnx.close()
