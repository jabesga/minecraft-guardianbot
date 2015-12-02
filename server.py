import web
import requests
token = "168379145:AAHGio5lnirJ3Rcxa09BkU2MuQJz84JSMGI"

def sendMessage(chat_id, text):
        response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(token, 'sendMessage'), data={'chat_id': chat_id, 'text': text}).json()

urls = (
  '/', 'index'
)

class index:
    def GET(self):
        return "Hello, world!"
    def POST(self):
        data = web.input()
        sendMessage(2816783, data.text)
        return "Hello, POST STRANGER!"        


if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()


# r = requests.post("http://localhost:8080", data={'text': "Que tal"})