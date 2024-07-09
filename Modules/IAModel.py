from openai import OpenAI
import ollama
from dotenv import load_dotenv
import os
import chromadb
from chromadb.config import Settings

load_dotenv()
class LModel:
    def __init__(self, api_key=None, model_point=None):
        self.modelo = os.environ.get("MODELLM")
        self.modelEmbedding = os.environ.get("MODELEMBEDDING")
        self.is_persistent = os.environ.get("IS_PERSISTENT", "False").lower() in ("true", '1', 't')
        self.persist_directory = os.environ.get("PERSIST_DIRECTORY")
        self.systemContent = os.environ.get("SYS_CONTENT")
        # client Chroma para que cree la db y se guarde
        self.ChromaClient = chromadb.Client(
            settings=Settings(
                is_persistent=self.is_persistent,
                persist_directory=self.persist_directory
            )
        )
        self.ollamaClient = ollama.AsyncClient(host="127.0.0.1:11434")

    async def av_chat(self, mode, system_content, message_user):
        return message_user

    # Función principal
    def responseGeneral(self, message_user):
        try:
            nameCollection = 'Tcollection'
            userEmbeddings =  self._responseEmbedding(message_user, nameCollection=nameCollection)
            response =  self._callGenerate(message_user, contextEmbedding=userEmbeddings)
            if response:
                return {"message": response}
        except Exception as e:
            return ({"error": f"Error al conectar con el motor: {str(e)}"})

    def _callGenerate(self, message_user, contextEmbedding):
        output = []
        try:
            responseCall = self.ollamaClient.generate(
                model=self.modelo,
                prompt=f"{self.systemContent}{contextEmbedding}. Responde a este mensaje: {message_user}",
                stream=True,
            )
            for fragmento in responseCall:
                output.append(fragmento["response"])

            return ''.join(output)
        except Exception as e:
            return ({"error": f"Error en la generación de respuesta: {str(e)}"})

    def _callEmbedding(self, prompt):
        try:
            responseEmbeddings = self.ollamaClient.embeddings(
                prompt=prompt,
                model=self.modelEmbedding
            )
            return responseEmbeddings
        except Exception as e:
            return ({"error": f"Error en la obtención de embeddings: {str(e)}"})

    def _embeddingsDataBase(self, nameCollection, dataContext):
        try:
            operacion = True
            Collection= self.ChromaClient.get_or_create_collection(name=nameCollection)
            for i, d in enumerate(dataContext):
                try:
                    response =  self._callEmbedding(prompt=d)
                    embedding = response["embedding"]
                    Collection.add(
                        ids=[str(i)],
                        embeddings=[embedding],
                        documents=[d]
                    )
                except Exception as e:
                    print(f"Error al agregar el documento {d}: {str(e)}")
                    operacion = False
            return operacion
        except Exception as e:
            return ({"Exception": f"Error al obtener Embedding Database: {str(e)}"})

    def _responseEmbedding(self, userMessage, nameCollection):
        try:
            userMessageEmbedding =  self._callEmbedding(prompt=userMessage)
            Collection = self.ChromaClient.get_or_create_collection(name=nameCollection)
            results = Collection.query(
                query_embeddings=[userMessageEmbedding["embedding"]],
                n_results=1
            )
            respuesta = results['documents'][0][0]
            return respuesta
        except Exception as e:
            return ({"error": f"Error en la respuesta de embedding: {str(e)}"})
