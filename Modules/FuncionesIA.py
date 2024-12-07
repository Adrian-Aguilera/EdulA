import ollama
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from ModelCustomApp.models import SettingLLM, SettingsChatGeneral, SettingsChatAsistente, SettingsChroma
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
load_dotenv(override=True)


class FuncionesIA:
    def __init__(self):
        settings_Chroma = self.getChromaSettings()
        settings_Ollama = self.clientOllama()
        self.is_persistent = settings_Chroma.is_persistent
        self.persist_directory = settings_Chroma.persist_directory
        # client Chroma para que cree la db y se guarde
        self.ChromaClient = chromadb.Client(
            settings=Settings(
                is_persistent=self.is_persistent,
                persist_directory=self.persist_directory,
            )
        )
        self.ollamaClient = ollama.AsyncClient(host=settings_Ollama.host)

    @staticmethod
    def getChromaSettings():
        """Obtiene la configuración de SettingsChroma desde la base de datos."""
        try:
            return SettingsChroma.objects.get()
        except ObjectDoesNotExist:
            raise Exception("No se encontró configuración en SettingsChroma. Por favor, agrega un registro en la base de datos.")

    @staticmethod
    def clientOllama():
        '''
            Funcion que se encarga de crear un cliente de ollama
        '''
        try:
            return SettingLLM.objects.get()
        except ObjectDoesNotExist:
            raise Exception("No se encontró configuración en SettingsLLM. Por favor, agrega un registro en la base de datos.")

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

    async def _callChatGenerate(self, historial, contexto=None):
        '''
            funcion que se encarga de llamar a la api de ollama para generar la respuesta, y devuelve la respuesta

            info: esta si tiene formato chat (chat function)
            pd: consultar la documetnacion de chat de la libreria OpenIA
        '''
        try:
            settings_Asistente = await sync_to_async(SettingsChatAsistente.objects.select_related('Model_LLM').first)()
            modelo = settings_Asistente.Model_LLM.model
            max_tokens = settings_Asistente.max_Tokens
            temperature = settings_Asistente.temperature
            num_gpu = settings_Asistente.num_gpu
            # Crear el mensaje con el contexto, si existe
            print(f'modelo asistente: {modelo}')
            conversacion = []
            if contexto:
                conversacion.append({"role": "system", "content": f'Eres un asistente virtual llamado Edula creado por ITCA FEPADE en El Salvador y solo hablas en español. Tu función es proporcionar asistencia estrictamente en temas educativos Debes mantener un enfoque educativo en todas tus respuestas. Ademas responde con menos de 200 palabras. Esta es la informacion de contexto: {contexto}. Si no conoces una respuesta, responde con "No se puede responder en este momento". Si en el contexto se menciona una url debes proporcionarla como una referencia.'})
            conversacion+=historial
            responseCall = await self.ollamaClient.chat(
                model=modelo,
                messages=conversacion,
                stream=False,
                options={'num_predict': int(max_tokens), 'temperature': float(temperature), 'num_gpu':int(num_gpu)}
            )
            print(f'historial: {historial}')
            return responseCall["message"]['content']
        except Exception as e:
            return {"error": f"{str(e)}"}

    async def _callEmbedding(self, prompt):
        '''
            funcion que se encarga de convertir el texto en un embedding, y devuelve el embedding

            pd: consultar la documentacion  de como funciona los embeddings
        '''
        try:
            settings_llm = await sync_to_async(SettingLLM.objects.first)()
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
            print(f'embeding: {userMessageEmbedding["embedding"]}')
            Collection = self.ChromaClient.get_collection(name=nameCollection)
            results = Collection.query(
                query_embeddings=userMessageEmbedding["embedding"], n_results=1
            )
            respuesta = results["metadatas"][0][0].get('content')
            # print('respuesta embeding: ',respuesta)
            return respuesta
        except Exception as e:
            return {"error": f"Error en la respuesta de embedding: {str(e)}"}

    async def _checkResponse(self, documento, claim):
        '''
            Necesitamos verificar la informacion de la respuesta generada es consistente con la informacion existnete en la bade de datos
        '''
        try:
            prompt =f'Document: {documento} \n Claim: {claim}'
            response = await self.ollamaClient.generate(
                model='bespoke-minicheck',
                prompt=prompt,
                stream=False,
                options={'num_predict': int(2), 'temperature': float(0.0), 'num_gpu':int(1)}
            )
            return response["response"].strip()
        except Exception as e:
            return {"error": f"Error en la verificacion de la respuesta: {str(e)}"}