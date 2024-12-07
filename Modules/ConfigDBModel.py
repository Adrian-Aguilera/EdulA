import chromadb
from chromadb.config import Settings
from Modules.FuncionesIA import FuncionesIA

class ModelDBRag:
    def __init__(self):
        self.funcionesIA = FuncionesIA()
        self.is_persistent = self.funcionesIA.getChromaSettings().is_persistent
        self.persist_directory = self.funcionesIA.getChromaSettings().persist_directory
        configuracion = Settings(is_persistent=self.is_persistent, persist_directory=self.persist_directory)
        self.ChromaClient = chromadb.Client(settings=configuracion)

    async def CargarDocumentos(self, nombre_Coleccion, documentos: list):
        try:
            collecion = self.ChromaClient.get_or_create_collection(name=nombre_Coleccion)
            print(documentos)
            for doc in documentos:
                print(f'doc: {doc["referencia_url"]}')
                try:
                    to_embedding = await self.funcionesIA._callEmbedding(prompt=doc['documento'])
                    print('to embedding: ', to_embedding['embedding'])
                    collecion.add(
                        ids=str(doc['id']),
                        embeddings=to_embedding["embedding"],
                        metadatas={"content": doc['documento'], "url": doc['referencia_url']}
                    )
                except Exception as e:
                    return {"Embedding error": f"{str(e)}"}
            return {"success": "Embedding creada Exitosamente"}
        except Exception as e:
            return {"Exception": f"{str(e)}"}