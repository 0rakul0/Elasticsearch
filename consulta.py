import urllib3
import uuid
import datetime
from elasticsearch import Elasticsearch

urllib3.disable_warnings()

# Create the client instance
client = Elasticsearch(['https://192.168.1.108:9200'], basic_auth=("elastic", "00110011aa@A"), verify_certs=False)

search = input("Digite uma palavra para ser buscada: ")

# res = client.search(index="bd-python-elastic", body={"query": {"match": {"nome": "" + search + ""}}})

# com fuzz
res = client.search(index="bd-python-elastic", body={
    "query": {
        "match": {
            "nome": {
                "query": ""+search+"",
                "operator": "and",
                "fuzziness": "AUTO"
            }
        }
    }
})
"""
# {'took': 19, 'timed_out': False, 
# '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0}, 
# 'hits': {'total': {'value': 1, 'relation': 'eq'}, 'max_score': 1.2039728, 
# 'hits': [{'_index': 'python-elasticsearch', '_id': '3', '_score': 1.2039728, 
# '_source': {'nome': 'karen', 'idade': 29, 'sexo': 'feminino', 'hobbies': ['quimica', 'python'], 'pets': 'cachorro', 
'nome_pet': 'luck', 'timestamp': '2022-04-02T20:43:11.938024'}}]}}
"""
print("\n retorno da busca: %d hits" % res['hits']['total']['value'])

for hit in res['hits']['hits']:
    print("\n%(timestamp)s \n %(nome)s \n %(idade)s \n %(sexo)s \n %(hobbies)s \n %(pets)s \n %(nome_pet)s "
          % hit["_source"])
