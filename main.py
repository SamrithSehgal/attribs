from datetime import datetime
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

psql = psycopg2.connect(user='postgres', password='samrith123', dbname='attributes')
cursor = psql.cursor()

info = [{"Timestamp": "2023-04-30 14:08:40", "Mac": "DB-06-2C-F8-54-6A", "Png": "image1"}, {"Timestamp": "2023-04-30 14:11:40", "Mac": "84-21-5C-87-06-F3", "Png": "image2"},  {"Timestamp": "2023-04-30 14:14:40", "Mac": "DB-BE-F2-8B-EB-86", "Png": "image3"}, {"Timestamp": "2023-04-30 14:16:40", "Mac": "7C-70-0C-3A-35-63", "Png": "image4"}]
sensors = {}
sensorTypes = {}
activeAttribs = []
dataRequest = {"messages": 2, "timestart":"2023-04-30 14:05:40", "timeend": '2023-04-30 14:15:40', "attributes": [0, 2]}

def addAttr(id, attr):
    cursor.execute('INSERT INTO attributes VALUES (%s, %s)', (id, attr))

def strToDate(string):
    return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')


def activate(capabilities):
    for capability in capabilities:
        activeAttribs.append(capability)

activate([0, 1])

@app.route('/addType', methods=['POST'])
def addSensorType():
    attribs = []
    sensorType = request.json['sensorType']
    attribDescs = request.json['attribs']
    cursor.execute('SELECT * FROM sensortypes WHERE typename=%s', (sensorType,))    
    if len(cursor.fetchall()) != 0:
        print('This sensor type already exists')
        return    
    
    cursor.execute('SELECT * FROM attributes')
    results = cursor.fetchall()
    lastId = len(results)
    allAttribs = dict(results).values()
    
    for desc in attribDescs:
        if desc not in allAttribs:
            attribs.append(lastId)
            addAttr(lastId, desc)
            lastId = lastId + 1
        else:
            cursor.execute('SELECT id FROM attributes WHERE description=%s', (desc, ))
            attribs.append(cursor.fetchone())
    cursor.execute('INSERT INTO sensorTypes VALUES (%s, %s)', (sensorType, tuple(attribs)))
    psql.commit()
    return("Coolio")

@app.route('/addSensor', methods=['POST'])
def addSensor():
    sensorType = request.json['sensorType']
    cursor.execute('SELECT * FROM sensortypes WHERE typename=%s', (sensorType,))
    sensorAttribs = cursor.fetchone()[1]
    cursor.execute('SELECT * FROM sensors')
    id = len(cursor.fetchall())
    cursor.execute('INSERT INTO sensors VALUES (%s, %s)', (id, sensorAttribs))
    psql.commit()
    return("Joolio")

    
    
cursor.execute('SELECT * FROM attributes')
attributes = dict(cursor.fetchall())


for attr in dataRequest['attributes']:
            if attr in activeAttribs:
                attribute = attributes[attr]
                for entry in info:
                    if strToDate(dataRequest['timestart']) < strToDate(entry['Timestamp']) < strToDate(dataRequest["timeend"]):
                       print(entry[attribute])
            else:
                pass

        
app.run()
    

cursor.close()
psql.close()

