import tornado.ioloop
import tornado.web

import sqlite3
import cgitb
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!\n")




if __name__ == "__main__":
	settings = {
		"autoreload": True,
		"debug": True,
	}
	application = tornado.web.Application([
		("/", MainHandler)
	], **settings)
	application.listen(8080)
	tornado.ioloop.IOLoop.instance().start()