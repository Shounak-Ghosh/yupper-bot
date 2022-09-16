from http.client import HTTPSConnection
import requests
import sys
from json import dumps
from time import sleep
from random import random

file = open("/Users/shounakg/Documents/GitHub/yupper-bot/info.txt")
text = file.read().splitlines()

if len(sys.argv) > 1 and sys.argv[1] == "--setall" and input("Configure bot? (y/n)") == "y":
    file.close()
    file = open("info.txt", "w")
    text = []
    text.append(input("User agent: "))
    text.append(input("Discord token: "))
    text.append(input("Discord channel URL: "))
    text.append(input("Discord channel ID: "))

    for parameter in text:
        file.write(parameter + "\n")

    file.close()
    exit()
elif len(sys.argv) > 1 and sys.argv[1] == "--setchannel" and input("Set channel? (y/n)") == "y":
    user_agent = text[0]
    token = text[1]
    text = text[0:2]
    file.close()
    file = open("info.txt", "w")
    text.append(input("Discord channel URL: "))
    text.append(input("Discord channel ID: "))
    for parameter in text:
        file.write(parameter + "\n")

    file.close()
    exit()
elif len(sys.argv) > 1 and sys.argv[1] == "--setauth" and input("Set authentication? (y/n)") == "y":
    channelurl = text[2]
    channelid = text[3]
    text = text[2:4]
    file.close()
    file = open("info.txt", "w")
    text.insert(0, input("Discord token: "))
    text.insert(0, input("User agent: "))
    for parameter in text:
        file.write(parameter + "\n")

    file.close()
    exit()
elif len(sys.argv) > 1 and sys.argv[1] == "--help":
    print("Showing help for discord-auto-message")
    print("Usage:")
    print("  'python3 bot.py'               :  Runs the autotyper. Fill in the messages and wait times.")
    print("  'python3 bot.py --setall'      :  Configure all settings.")
    print("  'python3 bot.py --setchannel'  :  Set channel to send message to. Includes Channel ID and Channel URL")
    print("  'python3 bot.py --setauth'     :  Set authentication. Includes User Token and User Agent")
    print("  'python3 bot.py --help'        :  Show help")
    exit()

if len(text) != 4:
    print("An error was found inside the user information file. Run the script with the 'Set All' flag ('python3 bot.py --setall') to reconfigure.")
    exit()
    
if len(sys.argv) > 1:
    exit()
    
header_data = {
    "content-type": "application/json",
    "user-agent": text[0],
    "authorization": text[1],
    "host": "discordapp.com",
    "referrer": text[2],
}

guild_id = '673765434243153930' # RMNA server id
yupper_id = '931312699047026698'

#print("Messages will be sent to " + header_data["referrer"] + ".")

def get_connection():
    return HTTPSConnection("discordapp.com", 443)


def send_message(conn, channel_id, message_data):
    try:
        # get yupper sticker info
        # r = requests.get(f"https://discordapp.com/api/v6/guilds/{guild_id}/stickers/{yupper_id}",headers=header_data)
        # print(r.text)
        conn.request("POST", f"/api/v6/channels/{channel_id}/messages", message_data, header_data)
        resp = conn.getresponse()
        
        if 199 < resp.status < 300:
            # print("Message sent!")
            pass

        else:
            sys.stderr.write(f"Received HTTP {resp.status}: {resp.reason}\n")
            pass

    except:
        sys.stderr.write("Failed to send_message\n")
        for key in header_data:
            print(key + ": " + header_data[key])


def main(msg):
    message_data = {
        "content": msg,
        "tts": "false",
        "sticker_ids": [yupper_id]
    }

    send_message(get_connection(), text[3], dumps(message_data))


if __name__ == '__main__':
    message = '' #input("Message to send: ")
    messages = 1 #int(input("Amount of messages: "))
    main_wait = 1 #int(input("Seconds between messages: "))
    human_margin = 1 #int(input("Human error margin: "))
    # print()
    for i in range(0,messages):
        sleep(main_wait)
        sleep(random()*human_margin)
        main(message)
    #     print("Estimated time to complete: " + str((messages-i) * (human_margin // 2 + main_wait) // 60) + " minutes.")
    #     print("Iteration " + str(i) + " complete.\n")

    # print("Session complete! " + str(messages) + " messages sent.")

