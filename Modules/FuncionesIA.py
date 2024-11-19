import ollama
from dotenv import load_dotenv
import os
import chromadb
from chromadb.config import Settings
from ModelCustomApp.models import SettingsLLM, SettingsChatGeneral, SettingsChatAsistente, SettingsChroma
from asgiref.sync import sync_to_async
load_dotenv(override=True)


class FuncionesIA:
    def __init__(self):
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
            settings_chat = await sync_to_async(SettingsChatGeneral.objects.select_related('Model_LLM').first)()
            modelo = settings_chat.Model_LLM.model
            max_tokens = settings_chat.max_Tokens
            temperature = settings_chat.temperature
            num_gpu = settings_chat.num_gpu
            print(f'max tokens: {max_tokens} \n temperature: {temperature} \n num gpu: {num_gpu}')
            responseCall = await self.ollamaClient.generate(
                model=modelo,
                prompt=f"Usa esta informacion: {contextEmbedding}. Responde a este mensaje: {message_user}",
                stream=False,
                options={'num_predict': int(max_tokens), 'temperature': float(temperature), 'num_gpu':int(num_gpu)}
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
            settings_llm = await sync_to_async(SettingsLLM.objects.first)()
            embedding_model = settings_llm.Model_Embedding
            print(f'embedding model: {embedding_model}')
            responseEmbeddings = await self.ollamaClient.embeddings(
                prompt=prompt, model=embedding_model
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
