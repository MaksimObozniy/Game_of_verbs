import json
import os
from google.cloud import dialogflow_v2 as dialogflow
from dotenv import load_dotenv


def create_intent(project_id: str, display_name: str, training_phrases: list[str], message_texts: list[str], language_code: str = "ru"):
    
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    
    training_phrases_objects = []
    for pharse in training_phrases:
        part = dialogflow.Intent.TrainingPhrase.Part(text=pharse)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases_objects.append(training_phrase)
        
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    
    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases_objects,
        messages=[message]
    )
    
    intents_client.create_intent(
        request={
            "parent": parent,
            "intent": intent,
            "language_code": language_code,
        }
    )

def main():
    with open("questions.json", 'r', encoding="utf-8") as file:
        questions = json.load(file)

    load_dotenv()
    project_id = os.environ["PROJECT_ID"]
    
    for intent_name, intent_data in questions.items():
        create_intent(
            project_id=project_id,
            display_name=intent_name,
            training_phrases=intent_data["questions"],
            message_texts=[intent_data["answer"]],
        )

if __name__ == "__main__":
    main()