from commands.command import Command
from fbchat import Message
from fbchat import Mention
import bs4
import requests

class weather(Command):

    def run(self):
        try:
            link = "https://www.theweathernetwork.com/ca/search?q="
            for i in self.user_params:
                if i == "-t":
                    break
                else:
                    link += i + "%20"
            webpage = requests.get(link)
            text = str(bs4.BeautifulSoup(webpage.text, 'html.parser').find("li", class_="result"))
            h = text.find("href")
            e = text[h:].find(">")
            r = text[h:h + e]
            print(r)
            link = "https://www.theweathernetwork.com" + r[6:-1]
            response_text = "@" + self.author.first_name + " Check for yourself at " + link
        except:
            response_text = "@" + self.author.first_name + " Dude is that even a place."
        mentions = [Mention(self.author_id, length=len(self.author.first_name) + 1)]

        self.client.send(
            Message(text=response_text, mentions= mentions),
            thread_id=self.thread_id,
            thread_type=self.thread_type
        )