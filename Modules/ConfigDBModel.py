from asgiref.sync import async_to_sync, sync_to_async
import os
import chromadb
import ollama
from chromadb.config import Settings
from dotenv import load_dotenv
from Modules.FuncionesIA import FuncionesIA

load_dotenv(override=True)
class ModelDB:
    def __init__(self):
        self.is_persistent = os.environ.get("IS_PERSISTENT", "False").lower() in ("true", '1', 't')
        self.persist_directory = os.environ.get("PERSIST_DIRECTORY")
        self.systemContent = os.environ.get("SYS_CONTENT")
        # client Chroma para que cree la db y se guarde
        self.ChromaClient = chromadb.Client(
            settings=Settings(
                is_persistent=self.is_persistent,
                persist_directory=self.persist_directory,
            )
        )

    def embeddingsDataBase(self, nameCollection, dataContext):
        try:
            generalObj = FuncionesIA()
            operacion = True
            filterData = dataContext.strip().split('\n\n')
            Collection = self.ChromaClient.get_or_create_collection(name=nameCollection)
            for i, d in enumerate(filterData):
                try:
                    response = async_to_sync(generalObj._callEmbedding)(prompt=d.strip())
                    embedding = response["embedding"]
                    id_unico = f'{nameCollection}_{i}'
                    Collection.add(
                        ids=[id_unico],
                        embeddings=[embedding],
                        documents=[d.strip()]
                    )
                except Exception as e:
                    print(f"Error al agregar el documento {d}: {str(e)}")
                    operacion = False
            return operacion
        except Exception as e:
            return {"Exception": f"Error al obtener Embedding Database: {str(e)}"}

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
                print(f'doc: {doc}')
                try:
                    to_embedding = await self.funcionesIA._callEmbedding(prompt=doc['documento'])
                    print('to embedding: ', to_embedding['embedding'])
                    collecion.add(
                        ids=str(doc['id']),
                        embeddings=to_embedding["embedding"],
                        metadatas={"content": doc['documento']}
                    )
                except Exception as e:
                    return {"Embedding error": f"{str(e)}"}
            return {"success": "Embedding creada Exitosamente"}
        except Exception as e:
            return {"Exception": f"{str(e)}"}