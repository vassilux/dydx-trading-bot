import requests
from decouple import config
import time

MSG_QUIT = "quit"
MSG_EXIT = "exit"
MSG_HELLO = "hello"
MSG_GET_POSITIONS = "getpositions"
MSG_ABORT_POSITIONS = "abortpositions"
MSG_NOTHING_TO_DO = "what"
telegram_delay=12

# Send Message
def send_message(message):
  bot_token = config("TELEGRAM_TOKEN")
  chat_id = config("TELEGRAM_CHAT_ID")
  url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
  res = requests.get(url)
  if res.status_code == 200:
    return "sent"
  else:
    return "failed"

def get_message():
  bot_token = config("TELEGRAM_TOKEN")
  strr='https://api.telegram.org/bot'+bot_token+'/getUpdates'
  response = requests.get(strr)
  rs=response.json()
  if(len(rs['result'])>0):
    rs2=rs['result'][-1]
    rs3=rs2['message']
    textt=rs3['text'].lower()
    datet=rs3['date']
    
    if(time.time()-datet) < telegram_delay:
      if MSG_QUIT in textt:
        return MSG_QUIT
      if MSG_EXIT in textt:
        return MSG_EXIT
      if MSG_HELLO in textt:
        return MSG_HELLO
      if MSG_GET_POSITIONS in textt:
        return MSG_GET_POSITIONS
      if MSG_ABORT_POSITIONS in textt:
        return MSG_ABORT_POSITIONS
  
  return MSG_NOTHING_TO_DO