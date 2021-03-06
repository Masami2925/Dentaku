import json

from commands.command import Command
from fbchat import Message
from fbchat import Mention
import subprocess
import requests


class ngrok(Command):
    def run(self):
        try:
            response = json.loads(requests.get('http://localhost:4040/api/tunnels').text)
        except:
            p = subprocess.Popen("exec " + "~/ngrok tcp 22", stdout=subprocess.PIPE, shell=True)
            while(True):
                try:
                    response = json.loads(requests.get('http://localhost:4040/api/tunnels').text)
                    pub_url = response['tunnels'][0]['public_url']
                    break
                except:
                    print("Attempting ngrok connection again...")
        response_text = """
        @{}\nPublic URL: {}
        """.format(self.author.first_name, pub_url)
        mentions = [Mention(self.author_id, length=len(self.author.first_name) + 1)]

        self.client.send(
            Message(text=response_text, mentions=mentions),
            thread_id=self.thread_id,
            thread_type=self.thread_type
        )

    def define_documentation(self):
        self.documentation = {
            "parameters": "None",
            "function": "Sending the address for the ngrok tcp link."
        }