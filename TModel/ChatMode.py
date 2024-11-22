from ollama import chat

# Lista para almacenar la conversación
conversation = []

# Ciclo de conversación continua
print("Bienvenido al chat con Ollama. Escribe 'exit' o 'quit' para salir.")

while True:
    # Obtener entrada del usuario
    user_input = input("\nUser: ")

    # Condición para salir del chat
    if user_input.lower() in ['exit', 'quit']:
        print("Cerrando la conversación. ¡Hasta luego!")
        break

    # Añadir el mensaje del usuario a la conversación
    conversation.append({'role': 'user', 'content': user_input})

    # Hacer la consulta al modelo sin modo stream
    response = chat(
        model='llama2:chat',
        messages=conversation,
        stream=False  # Se desactiva el modo stream
    )

    # Obtener y mostrar la respuesta del modelo
    response_content = response['message']['content']
    print(f"Assistant: {response_content}")

    # Añadir la respuesta del modelo a la conversación
    conversation.append({'role': 'assistant', 'content': response_content})
