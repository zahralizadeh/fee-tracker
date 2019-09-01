import requests
from bs4 import BeautifulSoup
import mysql.connector
import re
from sklearn import tree
import numpy as np


# initialize the connection to the database
cnx = mysql.connector.connect(user='root',password='',host='127.0.0.1',database='maktabkhooneh')
cursor = cnx.cursor()


#-------------------------------------------------------------------------------------#
#--------------------------------*******************----------------------------------#
#--------------------------------******Methods******----------------------------------#
#--------------------------------*******************----------------------------------#
#-------------------------------------------------------------------------------------#


#-------------------------------------------------------------------------------------#
#---@desc    get Offer type from user and check the input format 
#---@param   nothing
#---@return  string - user input for offer type
#-------------------------------------------------------------------------------------#
def get_offer_type():
    check = False
    while not check:
        offer_type = input('\
        Are you going to Buy or Rent a property,\n\
        for Buy press number 1\n\
        for Rent press 2   >>>>>>>>> ')

        if offer_type in ['1','2']:
            check = True
            return offer_type
        else:
            print('WRONG INPUT!')


#-------------------------------------------------------------------------------------#
#---@desc    get property type from user and check the input format 
#---@param   nothing
#---@return  string - user input for property type
#-------------------------------------------------------------------------------------#
def get_property_type():
    check = False
    while not check:
        property_type = input ('\
        Select property type...\n\
        Residential: press 1\n\
        Commercial press 2   >>>>>>>>> ')

        if property_type in ['1','2']:
            check = True
            return property_type
        else:
            print('WRONG INPUT!!!')


#-------------------------------------------------------------------------------------#
#---@desc    test if location is valid or not
#---@param   string city - city which user has inputed
#---@return  bool - valid city or not
#-------------------------------------------------------------------------------------#
def test(city):
    link = 'https://www.ihome.ir/خرید-فروش/مسکونی/'
    link = link+city
    print (link)
    r = requests.get(link)
    print(r)
    if r.status_code == 200:
        return True
    else:
        return False


#-------------------------------------------------------------------------------------#
#---@desc    get city from user
#---@param   nothing
#---@return  string - user input for city name
#-------------------------------------------------------------------------------------#
def get_user_city():
    check = False
    while not check:
        city = input ('Enter city name in persian   >>>>>>>>> ')

        if test(city):
            check = True
            return city
        else:
            print('WRONG INPUT!!!')


#-------------------------------------------------------------------------------------#
#---@desc    read locations from file "locations.txt" and load them in a list of dictionaries
#---@param   nothing
#---@return  list of dictionary - list of locations [code,title]
#-------------------------------------------------------------------------------------#
def save_locations_to_dic():
    ls=[]
    f =open("project/locations.txt", "r", encoding="utf-8")
    locations = f.readlines()
    code = 100
    for l in locations:
        location = l[:-1]
        dic = {'code': code , 'title':location }
        print('%s (%i)'%(location,code))
        ls.append(dic)
        code += 1
    f.close
    return ls


#-------------------------------------------------------------------------------------#
#---@desc    get the location from user
#---@param   nothing
#---@return  string - the selected location
#-------------------------------------------------------------------------------------#
def get_user_location():
    a = input('Select the location from following list..\n\
        You must enter location code! \n\
        press any key to continue   >>>>>>>>> ')
    ls = save_locations_to_dic()
    last_code = 100 + len(ls)
    check = False
    while not check:
        user_code = input('Enter a valid location code   >>>>>>>>> ')
        try:
            location_code = int(user_code)
            if(99<location_code<last_code):
                check = True
            else:
                print('The code is out  of range!')
        except:
            print('The location code is not valid!')
    location = next(item for item in ls if item['code'] == location_code)
    return location.get('title')


#-------------------------------------------------------------------------------------#
#---@desc    due to the user input get value of offer type to build url further 
#---@param   string user_input - user input for offer type
#---@return  string -  proper string that will be used in url
#---@return  None -  if the input is wrong
#-------------------------------------------------------------------------------------#
def rebuild_offer(user_input):
    if user_input == '1':
        return 'خرید-فروش'
    elif user_input == '2':
        return 'رهن-اجاره'
    else: 
        print('WRONG offer type!!!')
        return None


#-------------------------------------------------------------------------------------#
#---@desc    due to the user input get value of property type to build url further 
#---@param   string user_input - user input for property type
#---@return  string -  proper string that will be used in url
#---@return  None -  if the input is wrong
#-------------------------------------------------------------------------------------#
def rebuild_property(user_input):
    if user_input == '1':
        return 'مسکونی'
    elif user_input == '2':
        return 'اداری-تجاری'
    else: 
        print('WRONG property type!!!')
        return None


#-------------------------------------------------------------------------------------#
#---@desc    build url regarding offer and property type 
#---@param   string offer_type - proper string that shows offer type in url
#---@param   string property_type - proper string that shows property type in url
#---@param   string location - shows location in url
#---@return  string -  url for web scrapping
#-------------------------------------------------------------------------------------#
def build_URL(offer_type,property_type,city,location):
    offer__type = rebuild_offer(offer_type)
    property__type = rebuild_property(property_type)
    return 'https://www.ihome.ir/%s/%s/%s/%s'%(offer__type,property__type,city,location)


#-------------------------------------------------------------------------------------#
#---@desc    Check if the table exists in database or not 
#---@param   nothing
#---@return  bool -  exists or not
#-------------------------------------------------------------------------------------#
def tableIsNotExist():
    query = 'SHOW TABLES LIKE \'ihome2\''
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:  
        return True
    return False


#-------------------------------------------------------------------------------------#
#---@desc    extract location of the property file 
#---@param   soup file - property file 
#---@return  string -  location of property
#-------------------------------------------------------------------------------------#
def get_location(file):
    return file.find('div',class_='location').span.extract().get_text(strip=True)


#-------------------------------------------------------------------------------------#
#---@desc    extract area of the property file 
#---@param   soup file - property file 
#---@return  int -  area of property
#-------------------------------------------------------------------------------------#
def get_area(file):
    try:
        area_str =  file.find('i',class_ = 'ihome-arrows').next_sibling.replace(' متر مربع','').strip()
        return int(area_str.replace(',',''))
    except:
        return 0


#-------------------------------------------------------------------------------------#
#---@desc    extract price of the property file 
#---@param   soup file - property file 
#---@param   string offer_type - shows offer is buy or rent? 
#---@return  list -  list of prices, for BUY [price], for RENT [rent,deposit] 
#-------------------------------------------------------------------------------------#
def get_price(file,offer_type):
    price = [] 
    if offer_type=='1':     #extract price for BUY cases
        p = file.find('div',class_ = 'price')
        try:
            p.span.extract()
            price_str = p.get_text(strip = True).replace(',','').replace('تومان','')
            price.append(int(price_str))    
        except:
            price.append(0)
    if offer_type=='2':     #extract price for RENT cases
        p = file.find_all('div',attrs = {'class':['deposit','price']})
        if len(p)>1:        #it means that there is two prices including rent and deposit
            for q in p:
                try:
                    q.span.extract()
                    price_str = q.get_text(strip = True).replace(',','').replace('تومان','')
                    price.append(int(price_str))    
                except:
                    price.append(0)
        else:               #it means that there is one price, so the property is for full deposit
            price.append(0)
            try:
                p[0].span.extract()
                price_str = p[0].get_text(strip = True).replace(',','').replace('تومان','')
                price.append(int(price_str))    
            except:
                price.append(0)       
    return price


#-------------------------------------------------------------------------------------#
#---@desc    extract number of rooms from the property file 
#---@param   soup file - property file 
#---@return  int -  number of rooms of property
#-------------------------------------------------------------------------------------#
def get_rooms(file):
    try:
        rooms_str =  file.find('i',class_ = 'ihome-bed').next_sibling.strip()
        return int(rooms_str)
    except:
        return 0


#-------------------------------------------------------------------------------------#
#---@desc    extract building age of the property file 
#---@param   soup file - property file 
#---@return  int -  bulding age of property
#-------------------------------------------------------------------------------------#
def get_building_age(file):
    try:
        age_str =  file.find('i',class_ = 'ihome-building-age').next_sibling.replace('سن بنا','').strip()
        return int(age_str.replace(',',''))
    except:
        return 0


#-------------------------------------------------------------------------------------#
#---@desc    Append a new row of data to the database 
#---@param   string offer_type - shows offer is buy or rent? 
#---@param   string location - location of property
#---@param   int area -  area of property
#---@param   list price -  list of prices, for BUY [price], for RENT [rent,deposit] 
#---@return  bool - suucess or failure
#-------------------------------------------------------------------------------------#
def save_in_database(offer_type,location,area,price,rooms,age):
    if offer_type == '1':   #save data in database for BUY cases
        if price[0] > 0 and rooms > 0 and area > 0:
            query = 'INSERT INTO ihome2 VALUES (\'%s\',\'%s\',\'%i\',\'%i\',0,\'%i\',\'%i\')'\
                %(offer_type,location,area,price[0],rooms,age)
            cursor.execute(query)
            cnx.commit()
            return(True)
        return(False)
    elif offer_type == '2': #save data in database for RENT cases
        if price == [0,0] or rooms == 0 or area == 0:  #means data is not valid and usefull 
            return(False)
        else:
            query = 'INSERT INTO ihome2 VALUES (\'%s\',\'%s\',\'%i\',\'%i\',\'%i\',\'%i\',\'%i\')'\
                %(offer_type,location,area,price[0],price[1],rooms,age)
            cursor.execute(query)
            cnx.commit()
            return(True)


#-------------------------------------------------------------------------------------#
#---@desc    scrap for records of data and save them in database
#---@param   string base_link - specific link for web scrabbing 
#---@return  int - count of saved files
#-------------------------------------------------------------------------------------#
def webscarping(base_link):
    # variables used for logic 
    page_number = 1             #number of last web page that is checked
    count = 0                   #number of records saved in database successfully
    num_target_records = 150   #target number of records that should be saved in database
    target_page = 1
    #a loop that according to the number of target records runs
    while count < num_target_records and page_number <= target_page:
        #get the page content of the link from internet and make a soup of it
        #then extract the property files from the soup
        if page_number > 1:
            link = base_link + '/%i/'%(page_number)
        else:
            link = base_link
        print('I am analyzing:   %s'%(link))
        page = requests.get(link)
        soup = BeautifulSoup(page.text,'html.parser')
        if page_number == 1:
            records_info = soup.find('div',class_='right pg_counts').get_text(strip=True).replace(',','').split()
            record_num = 0
            try:
                record_num = int(records_info[2].strip())
                target_page = int(record_num/24)
                if (record_num%24) > 0:
                    target_page += 1
                #print('target page %i'%target_page)
            except:
                #print('%s is not number'%records_info[2])
                return count
            if (record_num < num_target_records):
                    if (record_num > 50):
                        num_target_records = record_num
                        #print('terget changed to %i'%num_target_records)
                    else:
                        print('SO Sorry! There is not enough data about this location')
                        return count
        
        all_files = soup.find_all('li', class_ =re.compile('blocks'))
        #extract each file and save it in the database
        for file in all_files:
            if count < num_target_records:
                if(save_in_database(offer_type,get_location(file),get_area(file),get_price(file,offer_type),\
                    get_rooms(file),get_building_age(file)) == True):
                    count += 1
        page_number += 1
    #print('%i records sucessfully saved in the database'%(count))
    return count


#-------------------------------------------------------------------------------------#
#---@desc    fetch data from database
#---@param   nothing
#---@return  list -  list of records
#-------------------------------------------------------------------------------------#
def read_from_database():
    query = 'SELECT DISTINCT area, rooms, age, price1, price2 FROM ihome2'
    cursor.execute(query)
    return cursor.fetchall()


#-------------------------------------------------------------------------------------#
#---@desc    get area from user
#---@param   nothing
#---@return  int -  area of the building as condition
#-------------------------------------------------------------------------------------#
def get_user_area():
    check = False
    while check == False:
        area_str = input('enter area   >>>>>>>')
        try:
            area = int(area_str)
            check = True
        except:
            print('The input is not valid!')
    return area


#-------------------------------------------------------------------------------------#
#---@desc    get rooms from user
#---@param   nothing
#---@return  int -  number of rooms as condition
#-------------------------------------------------------------------------------------#
def get_user_rooms():
    check = False
    while check == False:
        rooms_str = input('enter rooms number   >>>>>>>')
        try:
            rooms = int(rooms_str)
            check = True
        except:
            print('The input is not valid!')
    return rooms


#-------------------------------------------------------------------------------------#
#---@desc    get building age from user
#---@param   nothing
#---@return  int -  building age as condition
#-------------------------------------------------------------------------------------#
def get_user_age():
    check = False
    while check == False:
        age_str = input('enter building age   >>>>>>>')
        try:
            age = int(age_str)
            check = True
        except:
            print('The input is not valid!')
    return age

#-------------------------------------------------------------------------------------#
#---@desc    get area, number of rooms and age of the building from user
#---@param   nothing
#---@return  list -  list of conditions
#-------------------------------------------------------------------------------------#
def get_area_rooms_age():
    area = get_user_area()
    rooms = get_user_rooms()
    age = get_user_age()
    #test = numpy.array([area,rooms,age])
    return [[area,rooms,age]]


#-------------------------------------------------------------------------------------#
#---@desc    predict the answer using decision tree 
#---@param   nothing
#---@return  numpy.ndarray -  price of property
#-------------------------------------------------------------------------------------#
def predict(offer_type):
    x = []
    y = []

    result = [list(i) for i in read_from_database()]

    if offer_type == 1:
        for j in result:
            x.append([j[k] for k in range(3)])
            y.append(j[3])
    else:
        for j in result:
            x.append([j[k] for k in range(3)])
            y.append([j[3],j[4]])
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x,y)
    conditions = get_area_rooms_age()
    answer = clf.predict(conditions)
    return answer

#-------------------------------------------------------------------------------------#
#-------------------------*********************************---------------------------#
#-------------------------******MAIN CODE STARTS HERE******---------------------------#
#-------------------------*********************************---------------------------#
#-------------------------------------------------------------------------------------#

#Check if table has been created or not
#If not, then create it in the database
if tableIsNotExist():
    cursor.execute("CREATE TABLE ihome2 (\
        offer_type CHAR,\
        location VARCHAR(255), \
        area INT, \
        price1 BIGINT,\
        price2 BIGINT, \
        rooms INT, \
        age INT)")
else:
    cursor.execute('DELETE FROM ihome2')

#gets input from user 
# 1. offer type: Buy / Rent
# 2. property type: Residental / commercial
# then builds the proper link due to the user input
print('Hi...we are going to Store information about the house you want in database')
offer_type = get_offer_type()
base_link = build_URL(offer_type,get_property_type(),get_user_city(),get_user_location())
result_num = webscarping(base_link)
if (result_num < 50):
    print('Sorry! There is not enough data about this location. just %i records are availbale!'%result_num)
else:
    print('ok! lets go for predicting the cost of property with %i records'%result_num)
    answer = predict(offer_type).tolist()
    if offer_type == '1':
        print('I predict its cost as %i tomans'%answer[0][0])
    else:
        print('I predict its cost as %i tomans for deposit and %i tomans as monthly rent'%(answer[0][1],answer[0][0]))

cursor.close()
cnx.close()
