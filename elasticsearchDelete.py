import urllib3
import datetime
from elasticsearch import Elasticsearch

urllib3.disable_warnings()

# Create the client instance
client = Elasticsearch(['https://192.168.1.108:9200'], basic_auth=("elastic", "00110011aa@A"), verify_certs=False)

search = input("Digite uma palavra para ser buscada: ")

res = client.search(index="bd-python-elastic", body={"query": {"match": {"nome": "" + search + ""}}})

print("\n retorno da busca: %d hits" % res['hits']['total']['value'])

for hit in res['hits']['hits']:
    id = hit["_id"]
    print("\n ID: %s" % hit["_id"])
    print("\n%(timestamp)s \n %(nome)s \n %(sexo)s \n %(hobbies)s" % hit["_source"])
    option = input("deseja deletar o registro?: (s/n) -> ")
    if option == "s":
        # index="python-elasticsearch"
        res = client.delete(index="bd-python-elastic", id=id)
        print("\n status do documento: " + str(res['result']))

