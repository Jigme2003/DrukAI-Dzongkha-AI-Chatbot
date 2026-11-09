import requests

from src.chat_engine import get_chat_response

# Stores previous messages
chat_history = []

print("=" * 45)
print("             DrukAI Chatbot")
print("=" * 45)
print("Ask your questions in English or Dzongkha.")
print("Type 'exit' to close the chatbot.")

while True:

    user_input = input("\nYou: ")

    if user_input.lower().strip() == "exit":
        print("DrukAI: Goodbye!")
        break

    try:
        answer = get_chat_response(user_input, chat_history)

        print("\nDrukAI:", answer)

    except requests.exceptions.ConnectionError:
        print("Error: Ollama is not running.")

    except Exception as error:
        print("An error occurred:", error)
