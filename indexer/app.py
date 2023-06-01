from tika import parser
from datetime import datetime
import os
import hashlib
from elasticsearch import Elasticsearch
es = Elasticsearch('http://localhost:9200')


DOCS_PATH = './docs/'

for root, dirs, files in os.walk(os.path.abspath(DOCS_PATH)):
    for file in files:
        parsed_pdf = parser.from_file(os.path.join(root, file))
        data = parsed_pdf['content']
        doc = {
            'content': data,
            'file-name': file,
            'file-path': os.path.join(root, file),
            'timestamp': datetime.now(),
        }
        res = es.index(index="documents", id=hashlib.md5(file.encode('utf-8')).hexdigest(), document=doc)
        print(res['result'])



"""
GET _search
{
  "query": {
    "match_phrase": {
      "content":"Cooking Chinese"
    }
  }
}



# the document need to match with the two conditions
GET _search
{
  "_source": "file-name",
  "query": 
    { "bool" :
        {
         "must": [
           {"match_phrase":{"content": "chinese" }}
           
         ]
        } 
    } 
}



GET documents/_search 
{
  "fields": [
    {
      "field": "file-name"
    },
    {
      "field": "file-path"
    }
  ],
  "_source": "file-name",
  "query": 
    { "bool" :
        {
         "must": [
           {"match_phrase":{"content": "lebanese" }}
         ]
        } 
    } 
}
"""