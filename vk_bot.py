import os
from dotenv import load_dotenv
from dialogflow_api import detect_intent_text

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def send_message(vk_api_client, user_id: int, text: str) -> None:
    vk_api_client.messages.send(
        user_id=user_id,
        message=text,
        random_id=0,
    )


def main():
    load_dotenv()
    token = os.environ["VK_GROUP_TOKEN"]
    project_id = os.environ["PROJECT_ID"]

    vk_session = vk_api.VkApi(token=token)
    vk_api_client = vk_session.get_api()
    longpool = VkLongPoll(vk_session)
    
    print("VK Listener Started")
    
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            incoming_text = event.text
            user_id = event.user_id
            
            answer, is_fallback = detect_intent_text(
                project_id=project_id,
                session_id=str(user_id),
                text=incoming_text,
            )
            if not is_fallback:
                send_message(vk_api_client, user_id=user_id, text=answer)


if __name__ == "__main__":
    main()