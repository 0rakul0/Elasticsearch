import urllib3
from elasticsearch import Elasticsearch

urllib3.disable_warnings()
client = Elasticsearch(['https://192.168.1.108:9200'], basic_auth=("elastic", "00110011aa@A"), verify_certs=False)
# Create the client instance

client.info()
