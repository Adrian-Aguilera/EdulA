import ollama
from dotenv import load_dotenv
import os
import chromadb
from chromadb.config import Settings
from asgiref.sync import sync_to_async
from EduGeneralApp.models import NameCollectionGeneral

load_dotenv(override=True)


class GeneralModel:
    def __init__(self):
        self.MODELLM = os.environ.get("MODELLM")
        self.modelEmbedding = os.environ.get("MODELEMBEDDING")
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
        self.ollamaClient = ollama.AsyncClient(host='127.0.0.1:11434')

    # funcion principal de general response
    async def responseGeneral(self, message_user):
        try:
            instancia = await sync_to_async(list)(NameCollectionGeneral.objects.all())
            #print(instancia[0].nameCollection)
            nameCollection = instancia[0].nameCollection
            userEmbeddings = await self._responseEmbedding(message_user, nameCollection=nameCollection)
            responseGenerate = await self._callGenerate(message_user=message_user, contextEmbedding=userEmbeddings)
            if 'error' in userEmbeddings:
                return ({'error': userEmbeddings['error']})
            elif 'error' in responseGenerate:
                return ({'error': responseGenerate['error']})
            else:
                return ({'response': responseGenerate})
        except Exception as e:
            return {"error": f"{str(e)}"}


    async def _callGenerate(self, message_user, contextEmbedding=None):
        try:
            print(contextEmbedding)
            responseCall = await self.ollamaClient.generate(
                model=self.MODELLM,
                prompt=f"Usa esta informacion: {contextEmbedding}. Responde a este mensaje: {message_user}",
                stream=False,
                options={'num_predict': 200, 'temperature': 0.1, 'num_gpu':80}
            )
           #print(f'response call: {responseCall}')
            return responseCall["response"]
        except Exception as e:
            return {"error": f"Error en la generación de respuesta: {str(e)}"}

    async def _callChatGenerate(self, message_user):
        try:
            responseCall = await self.ollamaClient.chat(
                model=self.MODELLM,
                messages=[{'role':'user','content':f'{message_user}'}],
                stream=False,
                options={'num_ctx': 150, 'temperature':0.5},
            )
            print(f'response call: {responseCall}')
            return responseCall["message"]['content']
        except Exception as e:
            return {"error": f"Error en la generación de respuesta: {str(e)}"}

    async def _callEmbedding(self, prompt):
        try:
            responseEmbeddings = await self.ollamaClient.embeddings(
                prompt=prompt, model=self.modelEmbedding
            )
            return responseEmbeddings
        except Exception as e:
            return {"error": f"Error en la obtención de embeddings: {str(e)}"}

    async def _responseEmbedding(self, userMessage, nameCollection):
        try:
            userMessageEmbedding = await self._callEmbedding(prompt=userMessage)
            Collection = self.ChromaClient.get_collection(name=nameCollection)
            results = Collection.query(
                query_embeddings=[userMessageEmbedding["embedding"]], n_results=1
            )
            respuesta = results["documents"][0][0]
            #print('respuesta embeding: ',respuesta)
            return respuesta
        except Exception as e:
            return {"error": f"Error en la respuesta de embedding: {str(e)}"}
