from Modules.ConfigDBModel import ModelDBRag
from asgiref.sync import async_to_sync

class ControllerDataBase:
    def createCollection(self, documentos, nombre_Coleccion):
        try:
            objeto = ModelDBRag()
            crear_Coleccion = async_to_sync()(objeto.CargarDocumentos)(nombre_Coleccion=nombre_Coleccion, documentos=documentos)
            print(f'crear_Coleccion: {crear_Coleccion}')
            if crear_Coleccion.get('success'):
                return {"success": "Colleccion Embedding creada Exitosamente"}
            else:
                return {'error': crear_Coleccion}
        except Exception as e:
            return {'Collection error': f' {str(e)}'}