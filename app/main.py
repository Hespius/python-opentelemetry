import sqlite3
import logging
import logging.config
from os import path
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from src.util.utils import print_something

# Carrega as configurações de log do arquivo logging.conf
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)

# Configurar o provedor de rastreamento
tracer_provider = TracerProvider(
    resource=Resource.create({SERVICE_NAME: "sqlite3-crud"})
)

# Configurar o exportador Jaeger
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",  # Endereço do agente Jaeger (pode variar)
    agent_port=6831,  # Porta padrão para comunicação com o agente Jaeger
)

# Configurar exportador de rastreamento para a saída no console
span_processor = SimpleSpanProcessor(jaeger_exporter)
tracer_provider.add_span_processor(span_processor)

# Configurar o provedor de rastreamento como provedor global
trace.set_tracer_provider(tracer_provider)



# Função para criar a tabela SQLite
def create_table():
    with trace.get_tracer(__name__).start_as_current_span("Criação de tabela"):
        logging.info("Criando tabela SQLite...")
        connection = sqlite3.connect('mydb.sqlite')
        cursor = connection.cursor()
        logging.debug("Criando tabela 'users'")
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')
        logging.debug("Tabela 'users' criada")
        connection.commit()
        connection.close()

# Função para inserir um novo usuário
def insert_user(name, email):
    logging.info("Inserindo usuário...")
    connection = sqlite3.connect('mydb.sqlite')
    cursor = connection.cursor()
    logging.debug("Inserindo usuário %s", name)
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    logging.debug("Usuário %s inserido", name)
    connection.commit()
    connection.close()

# Função para buscar todos os usuários
def fetch_all_users():
    logging.info("Buscando usuários...")
    connection = sqlite3.connect('mydb.sqlite')
    cursor = connection.cursor()
    logging.debug("Buscando todos os usuários")
    cursor.execute('SELECT * FROM users')
    logging.debug("Usuários buscados")
    users = cursor.fetchall()
    connection.close()
    return users

# Função para atualizar um usuário por ID
def update_user(user_id, name, email):
    logging.info("Atualizando usuário...")
    connection = sqlite3.connect('mydb.sqlite')
    cursor = connection.cursor()
    logging.debug("Atualizando usuário de ID %s", user_id)
    cursor.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (name, email, user_id))
    logging.debug("Usuário de ID %s atualizado", user_id)
    connection.commit()
    connection.close()

# Função para excluir um usuário por ID
def delete_user(user_id):
    logging.info("Excluindo usuário...")
    connection = sqlite3.connect('mydb.sqlite')
    cursor = connection.cursor()
    logging.debug("Excluindo usuário de ID %s", user_id)
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    logging.debug("Usuário de ID %s excluído", user_id)
    connection.commit()
    connection.close()



# Exemplo de uso
if __name__ == '__main__':
    create_table()
    
    with trace.get_tracer(__name__).start_as_current_span("Inserção de usuário"):
        insert_user("Alice", "alice@example.com")
        print_something()
    
        with trace.get_tracer(__name__).start_as_current_span("Leitura de usuários"):
            users = fetch_all_users()
            print("Usuários no banco de dados:")
            for user in users:
                print(user)
        
            with trace.get_tracer(__name__).start_as_current_span("Atualização de usuário"):
                update_user(1, "Bob", "bob@example.com")
            
                with trace.get_tracer(__name__).start_as_current_span("Exclusão de usuário"):
                    delete_user(1)


