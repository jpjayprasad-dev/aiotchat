from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port':9200, 'scheme':'http'}])

result = es.search(index="aiot-index", body={"query":{"match_all":{}}}, size=1000)

for doc in result['hits']['hits']:
    print (doc['_source'])
