import os
from dotenv import load_dotenv

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

def main():
    load_dotenv()
    token = os.environ["VK_GROUP_TOKEN"]
    
    vk_session = vk_api.VkApi(token=token)
    longpool = VkLongPoll(vk_session)
    
    print("VK Listener Started")
    
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            print("Новое сообщение:")
            print("От:", event.user_id)
            print("Текст:", event.text)
            print("-" * 30)
            
if __name__ == "__main__":
    main()