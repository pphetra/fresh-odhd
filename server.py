import web
import sys

urls = (
    '/', 'Main'
)

app = web.application(urls, globals())

class Main:
    def GET(self):
        raise web.seeother('/static/index.html')
        
if __name__ == '__main__':
    app.run()