# Elasticsearch
 crud com elastic

# Query dentro do Python e Elasticsearch
## estrutura do elastic
```json
{
  "took" : 5,
  "timed_out" : false,
  "_shards" : {
    "total" : 2,
    "successful" : 2,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 0.78125054,
    "hits" : [
      {
        "_index" : "nome_do_banco",
        "_id" : "2",
        "_score" : 0.78125054,
        "_source" : {
          "nome" : "nome",
          "idade" : integer,
          "sexo" : "sexo",
          "hobbies" : [
            "hobbie01",
            "hobbie02",
            "hobbie03"
          ],
          "pets" : "tipo_pet",
          "nome_pet" : "nome_pet",
          "timestamp" : "2022-04-03T14:10:09.925103"
        }
      }
    ]
  }
}
```
## conexao
```py
import datetime
from elasticsearch import Elasticsearch
client = Elasticsearch(['https://localhost:9200'], basic_auth=("usuario", "senha"), verify_certs=False)
```
## create
```py
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

#create se for a primeira vez, update se for o mesmo id
res = client.index(index="bd-python-elastic", id=2, document=doc)
print(f"estatus inserção: {res['result']}")
```

## consulta com fuzzy
```py
search = input("Digite uma palavra para ser buscada: ")

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

print("\n retorno da busca: %d hits" % res['hits']['total']['value'])

for hit in res['hits']['hits']:
    print("\n%(timestamp)s \n %(nome)s \n %(idade)s \n %(sexo)s \n %(hobbies)s \n %(pets)s \n %(nome_pet)s "
          % hit["_source"])
```
## update
```py
search = input("Digite uma palavra para ser buscada: ")

res = client.search(index="nome_do_banco", body={
    "query": {
        "match": {
            "nome": "" + search + ""
        }
    }
})

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
```
## delete
```py
search = input("Digite uma palavra para ser buscada: ")

res = client.search(index="bd-python-elastic", body={
    "query": {
        "match": {
            "nome": "" + search + ""
        }
    }
})

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

```

# Query dentro do elastic
```
    tipos: PUT, GET, POST, DELETE, HEAD
    
    tipo <nome_do_banco>/<tipo>/id     |||    PUT bd-python-elastic/_doc/3
```
## create
```json
PUT bd-python-elastic/_doc/3
{
  "nome" : "Guilherme",
  "idade" : 36,
  "sexo" : "Masculino",
  "hobbies" : ["progamador web","python","java"],
  "pets" : "gato",
  "nome_pet" : "juju"
}
```
## consultar tudo
```json
get _search
{
  "query":{
    "match_all":{}
  }
}
```
## consulta padrão
```json
get  bd-python-elastic/_search
{
  "_source" : ["nome", "idade", "sexo", "hobbies", "pets", "nome_pet"],
  "query":{
    "match": {
      "hobbies": "python"
    }
  }
}
```
## consulta por palavras próximas
```json
get _search
{
  "query":{
    "match": {
      "nome": {
        "query": "Jeffersom silva",
        "operator": "and",
        "fuzziness": "AUTO"
      }
    }
  }
}
```
## pinned Querry geral
```json
# o id <- em ids dentro de pinned dá o id que irá aparecer primeiro nas buscas
        
get  bd-python-elastic/_search
{
  "_source" : ["nome", "idade", "sexo", "hobbies", "pets", "nome_pet"],
  "query":{
    "pinned": {
      "ids" : ["3"],
      "organic" : {
        "match_all" : {}
      }
    }
  }
}
```

## pinned Querry <- é colocado como prioridade por id
```json
# o id <- em ids dentro de pinned dá o id que irá aparecer primeiro nas buscas
        
get  bd-python-elastic/_search
{
  "_source" : ["nome", "idade", "sexo", "hobbies", "pets", "nome_pet"],
  "query":{
    "pinned": {
      "ids" : ["2","3"],
      "organic" : {
        "match": {
        "hobbies": "python"
        }
      }
    }
  }
}
```
# enriquecimento de dados
### criando mapping MODEL
```json
put municipios
{
  "mappings": {
    "properties": {
      "codigo_ibge": {
        "type": "integer"
      },
      "cidade": {
        "type": "text"
      },
      "city_location": {
        "type": "geo_point"
      },
      "capital": {
        "type" : "text"
      },
      "codigo_uf": {
        "type": "integer"
      }
    }
  }
}
```
### delete
```json
delete municipios
```
### Criando cidades
```json
post municipios/_doc/1
{
  "codigo_ibge":33018,
  "cidade":"Rio de Janeiro",
  "city_location":"-22.9014423492259, -43.17885933025985",
  "capital":true,
  "codigo_uf":33001,
}
```
### criação da politica
```json
put /_enrich/policy/users-police-municipios
{
  "match":{
    "indices":"municipios",
    "match_field":"cidade",
    "enrich_fields":["city_location","codigo_ibge"]
  }
}
```
### execução da politica
```
post /_enrich/policy/users-police-municipios/_execute
```

### deletando politica 
```
delete /_enrich/policy/users-police-municipios
```
### adicionando pipeline
```json
put /_ingest/pipeline/user_lookup_municiopios
{
  "description":"Enriquecimento com dados de munipios",
  "processors":[
    {
      "enrich":{
        "policy_name" : "users-police-municipios",
        "field":"cidade",
        "target_field":"city"
      }
    }
  ]
}
```
### mapping de usuarios
```json
PUT users
{
  "mappings": {
    "properties": {
      "city.city_location":{
        "type": "geo_point"
      }
    }
  }
}
```
### criando usuarios
```json
post /users/_doc/1?pipeline=user_lookup_municiopios
{
  "email":"jefferson.ti@hotmail.com.br",
  "nome":"Jefferson",
  "sobrenome": "Silva dos Anjos",
  "cidade": "Rio de Janeiro",
  "Pais":"Brasil",
  "estado":"Rio de Janeiro"
}
```
### lendo os dados
```json
GET municipios/_search
{
  "query": {
    "match_all": {}
  }
}
```