import pprint
import pymongo as pyM

# Criando conexão do MongoDB
client = pyM.MongoClient("dados de conexao aqui")

# Criando o BD e a collection
db = client.banco
collection = db.test_collection

# teste de funcionamento
# print(db.list_collection_names())

# Definindo as informações do documento
novos_clientes = [{
                "agencia": "9101",
                "nome": "Fabio Cruz",
                "cpf": "12345678912",
                "endereco": "Rua Osvaldo Amaral, 128",
                "conta": ["cp", 305577],
                "saldo":12500
                },
                {
                "agencia": "1082",
                "nome": "Aparecida Ferreira",
                "cpf": "98765432101",
                "endereco": "Rua Ivan Maia, 14",
                "conta": ["cc", 452057],
                "saldo":36000
                }]

print("Salvando as informações no MongoDB")
clients = db.clients
result = clients.insert_many(novos_clientes)
print(result.inserted_ids)

print("\n Recuperando as informações da cliente Aparecida:")
pprint.pprint(db.clients.find_one({"nome": "Aparecida Ferreira"}))

print("\n Listagem dos clientes presentes na coleção clients:")
for client in clients.find():
    pprint.pprint(client)

print("\n Recuperando informação dos clientes de maneira ordenada pelo nome:")
for client in clients.find({}).sort("nome"):
    pprint.pprint(client)

print("\n Clientes da agência 9101-0:")
for client in clients.find({"agencia": "9101-0"}):
    pprint.pprint(client)

print("\n Clientes com conta poupança:")
for client in clients.find({"conta": "cp"}):
    pprint.pprint(client)

print("\n Clientes com conta corrente:")
for client in clients.find({"conta": "cc"}):
    pprint.pprint(client)
