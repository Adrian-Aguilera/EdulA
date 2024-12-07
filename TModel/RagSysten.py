import chromadb
import ollama
from chromadb.config import Settings

configuracion = Settings(is_persistent=True, persist_directory="./DB/Chroma_storageDB")

def main():
    while True:
        mensaje = input('Ingresa una duda: ')
        contexto = obtenerContexto(mensaje=mensaje)
        conversacion = []
        conversacion.append({"role": "system", "content": f'Eres un asistente virtual llamado Edula creado por ITCA FEPADE en El Salvador y solo hablas en español. Tu función es proporcionar asistencia estrictamente en temas educativos Debes mantener un enfoque educativo en todas tus respuestas o respuestas fuera de tema. Ademas responde con menos de 200 palabras, empieza cada respuesta con el nombre con base a la conversacion. Esta es la informacion de contexto: {contexto}'})
        conversacion.append({'role': 'user', 'content': mensaje})
        response = ollama.chat(
            model='PI-Edula:Chat',
            messages=conversacion,
            stream=True,
            options={'num_ctx': 50, 'temperature': 0.1, "num_predict":150}
        )
        for chunk in response:
            print(chunk['message']['content'], end='', flush=True)
        print('\n')
        print(f'conversacion: {conversacion}')

def createCollection():
    client = chromadb.Client(settings=configuracion)
    collection = client.get_or_create_collection(name='urls4')
    documentos = [
        {"id": '1', "content": "Python es un lenguaje de programación popular para el desarrollo web y análisis de datos.", "url": "https://www.python.org/"},
        {"id": '2', "content": "Django es un framework de Python para desarrollo rápido de aplicaciones web.", "url": "https://www.djangoproject.com/"},
        {"id": '3', "content": "No se ha encontrado ningun resultado  similar", "url": "https://www.google.com/"},
    ]

    for doc in documentos:
        print(f"Agregando documento {doc['id']} a la colección...")
        print(f'Documento: {doc["content"]}')
        print(f'URL: {doc["url"]}')

        # Pasamos la URL como lista
        collection.add(
            ids=doc["id"],
            embeddings=createEmbeddings(doc["content"]),
            metadatas={"content": doc["content"], "url": doc["url"]},
            documents=doc["content"],
        )
    print('Documentos agregados a la colección.')

def createEmbeddings(texto):
    print(f'texto: {texto}')
    resonseEmbedding = ollama.embeddings(model="mxbai-embed-large", prompt=texto)
    print(f'embedding: {resonseEmbedding["embedding"]}')
    return resonseEmbedding["embedding"]

def obtenerContexto(mensaje):
    client = chromadb.Client(settings=configuracion)
    collection = client.get_collection(name='urls4')
    mensaje_Embedding = createEmbeddings(texto=mensaje)
    resultados = collection.query(
        query_embeddings=mensaje_Embedding,
        n_results=1
    )
    full_contexto = [f"{item.get('content', '')} referencias: {item.get('url', '')}" for item in resultados["metadatas"][0]]
    print(f'full contexto: {full_contexto[0]}')
    return full_contexto[0]

def obtenerColeciones():
    client = chromadb.Client(settings=configuracion)
    collection = client.get_collection(name='urls4')
    results = collection.peek()
    urls = [resultado.get('url') for resultado  in results["metadatas"]]
    print(urls)

if __name__ == "__main__":
    #createCollection()
    main()
    #obtenerColeciones()