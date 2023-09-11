from datetime import datetime
from elasticsearch import Elasticsearch

class GeneralLogger:
    def __init__(self, es_host):
        self._es = Elasticsearch([{'host': es_host.split(':')[0], 'port':int(es_host.split(':')[1]), 'scheme':'http'}])

    def log(self, role_type, text):
        doc = {
            'role': role_type,
            'text': text,
            'timestamp': datetime.now(),
        }
        self._es.index(index="aiot-index", document=doc)
        self._es.indices.refresh(index="aiot-index")