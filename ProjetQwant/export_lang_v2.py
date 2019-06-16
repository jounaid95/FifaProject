import pymongo
import json
from pymongo import MongoClient
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from langdetect import detect_langs

client = MongoClient("176.31.43.33", 27017, maxPoolSize=50)
db=client.mydatabase
db = client['music']
db.authenticate('esieestudents', 'esiee2017projecte4qwant', mechanism = 'SCRAM-SHA-1', source='music')
collection=db['genius_collection_copy']
cursor = collection.find()
list_of_dict = list()
for document in cursor:
    list_of_dict.append(document)

list_of_lyrics = list()
list_of_url = list()
list_of_lng = list()
for x in range(len(list_of_dict)):

    if list_of_dict[x].get("lyrics") and list_of_dict[x].get("url"):
        
        list_of_lyrics.append(list_of_dict[x]["lyrics"])
        list_of_url.append(list_of_dict[x]["url"])

test_dict = dict(zip(list_of_url, list_of_lyrics))

dict_langue = {}
for key, value in test_dict.items():
    try:
        if detect(value) == 'ro' and 'Instrumental' in value:
            dict_langue[key] = "NA"
        else:
            if float(str(detect_langs(value)[0]).split(":")[1]) > 0.9:
                dict_langue[key] = detect(value)
            else:
                dict_langue[key] = "NA"
    except LangDetectException:
        dict_langue[key] = "NA"

for key, value in dict_langue.items():
    print(key, value)

for key, value in dict_langue.items():
	collection.update_one({'url': key}, {"$set": {"lang": value}}, upsert=False)
	print("Language added to the song!")
