from tika import parser
from PyPDF2 import PdfReader
from datetime import datetime
import os
import hashlib
from elasticsearch import Elasticsearch
es = Elasticsearch('http://localhost:9200')


DOCS_PATH = './docs/'


def extract_page_text(path):
    pages = []
    reader = PdfReader(path)
    totalPages = len(reader.pages)
    for x in range(totalPages):
        page = reader.pages[x]
        page_text = page.extract_text()
        pages.append({'number': x+1, 'text': page_text})

    print(pages)
    return pages


# Indexando pagina a pagina
for root, dirs, files in os.walk(os.path.abspath(DOCS_PATH)):
    for file in files:
        pages = extract_page_text(os.path.join(root, file),)
        # parsed_pdf = parser.from_file(os.path.join(root, file))
        # data = parsed_pdf['content']
        for page in pages :
            pageObj = {
                "page-number": page["number"],
                "file-name": file,
                "file-path": os.path.join(root, file),
                "timestamp": datetime.now(),
                "content": page["text"]
            }
            res = es.index(index="documents-pages", id=hashlib.md5(page["text"].encode("utf-8")).hexdigest(), document=pageObj)
            print(res["result"])




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



GET documents-pages/_search 
  {
    "query": 
      { "bool" :
          {
           "should": [
             {"match_phrase":{"content": "critically examine" }},
             {"match_phrase":{"content": "Vegan" }}
           ]
          } 
      },
      "fields": [
        "file-name",
        "file-path",
        "page-number"
      ],
      "_source": false
  }
"""