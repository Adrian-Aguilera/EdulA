import ollama
from dotenv import load_dotenv
import os
import chromadb
from chromadb.config import Settings
from asgiref.sync import sync_to_async
from EduGeneralApp.models import General_Collection

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


    async def _callGenerate(self, message_user, contextEmbedding=None):
        '''
            funcion que se encarga de llamar a la api de ollama para generar la respuesta, y devuelve la respuesta
            pd: contextEmbedding es el embedding de la informacion de la base de datos
            pd: message_user es el mensaje que se esta enviando

            info: solo se encarga de generar texto sin formato para un chat (generate function)
        '''
        try:
            print(contextEmbedding)
            responseCall = await self.ollamaClient.generate(
                model=self.MODELLM,
                prompt=f"Usa esta informacion: {contextEmbedding}. Responde a este mensaje: {message_user}",
                stream=False,
                options={'num_predict': 200, 'temperature': 0.1, 'num_gpu':80}
            )
            return responseCall["response"]
        except Exception as e:
            return {"error": f"Error en la generación de respuesta: {str(e)}"}

    async def _callChatGenerate(self, message_user):
        '''
            funcion que se encarga de llamar a la api de ollama para generar la respuesta, y devuelve la respuesta

            info: esta si tiene formato chat (chat function)
            pd: consultar la documetnacion de chat de la libreria OpenIA
        '''
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
        '''
            funcion que se encarga de convertir el texto en un embedding, y devuelve el embedding

            pd: consultar la documentacion  de como funciona los embeddings
        '''
        try:
            responseEmbeddings = await self.ollamaClient.embeddings(
                prompt=prompt, model=self.modelEmbedding
            )
            return responseEmbeddings
        except Exception as e:
            return {"error": f"Error en la obtención de embeddings: {str(e)}"}

    async def _responseEmbedding(self, userMessage, nameCollection):
        '''
            Es es la funcion que se encarga de obtener primero el embedding del mensaje entrante (convertirlo a numerico la respuesta).
            Luego hace la consulta en la db de chroma para obtener una respuesta de la base de datos, con base a la similitud del mensaje del usuario
        '''
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
