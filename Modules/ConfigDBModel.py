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
                    Collection.add(
                        ids=[str(i)],
                        embeddings=[embedding],
                        documents=[d.strip()]
                    )
                except Exception as e:
                    print(f"Error al agregar el documento {d}: {str(e)}")
                    operacion = False
            return operacion
        except Exception as e:
            return {"Exception": f"Error al obtener Embedding Database: {str(e)}"}