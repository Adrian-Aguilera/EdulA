import chromadb
import ollama
from chromadb.config import Settings

configuracion = Settings(is_persistent=True, persist_directory="./DB/Chroma_storageDB")

def main():
    while True:
        mensaje = input('Ingresa una duda: ')
        contexto = obtenerContexto(mensaje=mensaje)
        conversacion = [{'role': 'system', 'content':f'con base a este contexto {contexto}, response la pregunta, solo en español'}]
        conversacion.append({'role': 'user', 'content': mensaje})
        response = ollama.chat(
            model='llama2:chat',
            messages=conversacion,
            stream=True,
            options={'num_ctx': 50, 'temperature': 0.1}
        )
        for chunk in response:
            print(chunk['message']['content'], end='', flush=True)
        print('\n')

def createCollection():
    client = chromadb.Client(settings=configuracion)
    collection = client.get_or_create_collection(name='RagCollection3')
    documentos = [
        {"id": '1', "content": "Python es un lenguaje de programación popular para el desarrollo web y análisis de datos."},
        {"id": '2', "content": "Django es un framework de Python para desarrollo rápido de aplicaciones web."},
    ]

    for doc in documentos:
        print(f"Agregando documento {doc['id']} a la colección...")
        print(f'Documento: {doc["content"]}')
        collection.add(
            ids=doc["id"],
            embeddings=createEmbeddings(doc["content"]),
            metadatas={"content": doc["content"]}
        )
    print('Documentos agregados a la colección.')

def createEmbeddings(texto):
    print(f'texto: {texto}')
    resonseEmbedding = ollama.embeddings(model="mxbai-embed-large", prompt=texto)
    print(f'embedding: {resonseEmbedding}')
    return resonseEmbedding["embedding"]

def obtenerContexto(mensaje):
    client = chromadb.Client(settings=configuracion)
    collection = client.get_collection(name='RagCollection3')
    mensaje_Embedding = createEmbeddings(texto=mensaje)
    resultados = collection.query(
        query_embeddings=mensaje_Embedding,
        n_results=1
    )
    contexto = resultados["metadatas"]
    print(f'contexto: {contexto[0]}')
    return contexto

def eliminarCollection():
    client = chromadb.Client(settings=configuracion)
    collection = client.get_collection(name='RagCollection')
    collection.delete()
    print('Colección eliminada.')

if __name__ == "__main__":
    #createCollection()
    main()