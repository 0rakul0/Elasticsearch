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
    option = input("deseja atualizar o registro?: (s/n) -> ")
    if option == "s":
        new_nome = input("\n Digite o novo nome: ")
        new_idade = input("\n Digite a idade: ")
        new_sexo = input("\n Digite o sexo: ")
        new_hobbies = input("\n Digite os novos hobbies: ")
        new_pets = input("\n Digite o tiopo de pets: ")
        new_nome_pet = input("\n Digite o nome do pet: ")

        doc = {
            "nome": new_nome,
            "idade": new_idade,
            "sexo": new_sexo,
            "hobbies": new_hobbies,
            "pets": new_pets,
            "nome_pet": new_nome_pet,
            "timestamp": datetime.datetime.now(),
        }

        res = client.index(index="bd-python-elastic", id=id, document=doc)
        print("\n status do documento: " + str(res['result']))

        res = client.get(index="bd-python-elastic", id=id)
        print("\n\n Resultado da busca: \n"+str(res['_source']))
