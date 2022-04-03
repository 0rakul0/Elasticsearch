import urllib3
import datetime
from elasticsearch import Elasticsearch

urllib3.disable_warnings()

# Create the client instance
client = Elasticsearch(['https://192.168.1.108:9200'], basic_auth=("elastic", "00110011aa@A"), verify_certs=False)

doc = {
    "nome": "Jefferson Silva dos Anjos",
    "idade": 30,
    "sexo": "masculino",
    "hobbies": ["desenvolvedor web", "python", "Java"],
    "pets": "gato",
    "nome_pet": "berus",
    "timestamp": datetime.datetime.now(),
}
#crud com elastic

#create se for a primeira vez, update se for o mesmo id
res = client.index(index="bd-python-elastic", id=2, document=doc)
print(f"estatus inserção: {res['result']}")

#read index="python-elasticsearch"
res = client.get(index="bd-python-elastic", id=2)
print(res['_source'])

