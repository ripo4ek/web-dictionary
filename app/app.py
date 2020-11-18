from flask import Flask, Response, request, render_template
import requests
import pymongo
from flask_cors import CORS

app = Flask(__name__)
client = pymongo.MongoClient('mongodb',27017)
db = client['test-database']
collection = db['test-collection']

CORS(app)

def getFromSupApp(word):
    r = requests.get('http://dictionary:8080/' + word)
    if r.status_code == 404:
        return None
    return r.text
    

def getFromMongo(word):
    entity = collection.find_one({"word": word.upper()})
    print(entity)
    if entity == None:
        return None
    return entity['definition']


@app.route('/', methods=['GET'])
def mainpage():
    return render_template('index.html')


@app.route('/add',methods=['POST'])
def addWord():
    content = request.get_json()
    word = content['word']
    definition = content['definition']
    print(content)
    print(word)
    print(definition)
    upperWord = word.upper()
    print(upperWord)
    entity = collection.find_one({"word":upperWord})
    if entity == None:
        collection.insert_one({"word":upperWord, "definition":definition})
    else:
        collection.update_one(
        {"_id": entity['_id']},
        {"$set":
        {"word": upperWord,
        "definition":definition
        }})
    return Response(definition)


@app.route('/get/<word>',methods=['GET'])
def getWord(word):
    upperWord = word.upper()
    defSupApp = getFromSupApp(upperWord)
    defMongo = getFromMongo(upperWord)
    if defMongo != None:
        return defMongo
    if defSupApp != None:
        return defSupApp
    return "Word not found",404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=9090)