from sklearn import tree
import mysql.connector
import numpy

# initialize the connection to the database
cnx = mysql.connector.connect(user='root',password='',host='127.0.0.1',database='maktabkhooneh',charset="utf8", use_unicode=True)
cursor = cnx.cursor()

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
def get_area():
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
def get_rooms():
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
#---@desc    get rooms from user
#---@param   nothing
#---@return  int -  number of rooms as condition
#-------------------------------------------------------------------------------------#
def get_age():
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
    area = get_area()
    rooms = get_rooms()
    age = get_age()
    #test = numpy.array([area,rooms,age])
    return [[area,rooms,age]]


offer_type = 1

x = []
y = []

result = [list(i) for i in read_from_database()]

if offer_type == 1:
    for j in result:
        x.append([j[k] for k in range(3)])
        #x.append([j[0],j[1],j[2]])
        y.append(j[3])
else:
    for j in result:
        x.append([j[0],j[1],j[2]])
        y.append([j[3],j[4]])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x,y)

conditions = get_area_rooms_age()
answer = clf.predict(conditions)
print('I predict its cost as %i tomans'%answer[0])
cursor.close()
cnx.close()