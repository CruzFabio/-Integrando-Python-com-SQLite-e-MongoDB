'''
    Desafio DIO - Implementando um Banco de Dados Relacional com SQLAlchemy
'''

from sqlalchemy import (Column,
                        Float,
                        Integer,
                        String,
                        ForeignKey,
                        create_engine,
                        inspect,
                        select,
                        func)
from sqlalchemy.orm import (declarative_base,
                            relationship,
                            Session)

from integration_with_sqlalchemy.integrationWithMongo.sqlAlchemyApplication import connection

Base = declarative_base()


class Cliente(Base):
    '''
        Essa classe representa a tabela cliente dentro do SQLite.
    '''
    __tablename__ = "cliente"
    # Definindo os atributos
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    cpf = Column(String(11))
    endereco = Column(String(50))

    # Definindo o relacionamento
    conta = relationship("Conta", back_populates="cliente")

    # criando uma representação par a classe
    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"


class Conta(Base):
    '''
        Essa classe representa a tabela conta dentro do SQLite.

        Os tipos de conta que iremos representar são: CC = Conta Corrente,
        CP = Conta Poupança, CI = Conta Investimento
    '''
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True)
    tipo = Column(String(2))
    agencia = Column(String(5))
    numero = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    saldo = Column(Float)

    # Definindo o relacionamento
    cliente = relationship("Cliente", back_populates="conta")

    # criando uma representação par a classe
    def __repr__(self):
        return (f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, numero={self.numero}, "
                f"id_cliente={self.id_cliente}, saldo={self.saldo})")


print(Cliente.__tablename__)
print(Conta.__tablename__)

# Criando a conexão ao BD
engine = create_engine("sqlite://")

# Criando as classes como tabelas no BD
Base.metadata.create_all(engine)

# Chamando o inspetor que será o responsável por buscar dentro da
# engine as informações que necessitamos
inspect_engine = inspect(engine)

print(inspect_engine.get_table_names())
print(inspect_engine.default_schema_name)

with Session(engine) as session:
    fabio = Cliente(
        nome="Fabio Cruz",
        cpf="12345678912",
        endereco="Rua Osvaldo Amaral, 128"
    )

    cida = Cliente(
        nome="Aparecida Ferreira",
        cpf="98765432101",
        endereco="Rua Ivan Maia, 14"
    )

    conta1 = Conta(
        tipo="cp",
        agencia="9101",
        numero=305577,
        id_cliente=1,
        saldo=12500
    )

    conta2 = Conta(
        tipo="cc",
        agencia="1082",
        numero=452057,
        id_cliente=2,
        saldo=36000
    )

    # Enviando para o BD (persistência de dados)
    session.add_all([fabio, cida])
    session.add_all([conta1, conta2])

    session.commit()

# consultando as informações no BD
print('\nRecuperando cliente através do nome')
stmt = select(Cliente).where(Cliente.nome.in_(["Fabio", "Aparecida"]))
for result in session.scalars(stmt):
    print(result)


print('\nRecuperando clientes de maneira ordenada')
stmt_order = select(Cliente).order_by(Cliente.nome.desc())
for result in session.scalars(stmt_order):
    print(result)


print('\nRecuperando contas de maneira ordenada')
stmt_order = select(Conta).order_by(Conta.tipo.desc())
for result in session.scalars(stmt_order):
    print(result)


print('\nRecuperando contas e clientes')
stmt_join = select(Cliente.nome, Conta.tipo, Conta.saldo).join_from(Cliente, Conta)
connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
for result in results:
    print(result)

session.close()