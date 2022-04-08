from datetime import datetime
import uuid

import urllib3
from elasticsearch import Elasticsearch


urllib3.disable_warnings()
es = Elasticsearch(['https://192.168.1.108:9200'], basic_auth=("elastic", "00110011aa@A"), verify_certs=False)

nome_banco = "bd-python-elastic"

# CRUD - create
def create():
    new_nome = input("\n Digite o nome: ")
    new_idade = input("\n Digite a idade: ")
    new_sexo = input("\n Digite o sexo: ")
    new_hobbies = input("\n Digite os hobbies: ")
    new_pets = input("\n Digite o tipo de pets: ")
    new_nome_pet = input("\n Digite o nome do pet: ")

    doc = {
        "nome": new_nome,
        "idade": new_idade,
        "sexo": new_sexo,
        "hobbies": new_hobbies,
        "pets": new_pets,
        "nome_pet": new_nome_pet,
        "timestamp": datetime.now(),
    }
    res = es.index(index=nome_banco, id=str(uuid.uuid4()), document=doc)
    print("\n status do documento: " + str(res['result']))

    return res['_source']


# CRUD - Read
def readAll():
    res = es.search(index=nome_banco, body={
        "query": {
            "match_all": {}
        }
    })
    print("\n retorno da busca: %d hits" % res['hits']['total']['value'])
    for hit in res['hits']["hits"]:
        print("\n %(nome)s \n %(idade)s \n %(sexo)s \n %(hobbies)s \n %(pets)s \n %(nome_pet)s"
              % hit["_source"])

def readOne(search):
        res = es.search(index=nome_banco, body={
            "query": {
                "match": {
                    "nome": {
                        "query": "" + search + "",
                        "operator": "and",
                        "fuzziness": "AUTO"
                    }
                }
            }
        })
        for hit in res['hits']['hits']:
            print("\n %(nome)s \n %(idade)s \n %(sexo)s \n %(hobbies)s \n %(pets)s \n %(nome_pet)s"
                  % hit["_source"])

def Update():
    search = input("Digite uma palavra para ser buscada: ")

    res = es.search(index="bd-python-elastic", body={
        "query": {
            "match": {
                "nome": "" + search + ""
            }
        }
    })

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
                "timestamp": datetime.now(),
            }

            res = es.index(index=nome_banco, id=id, document=doc)
            print("\n status do documento: " + str(res['result']))

            res = es.get(index=nome_banco, id=id)
            print("\n\n Resultado da busca: \n" + str(res['_source']))

if __name__ == "__main__":
    readOne("guilhem")
