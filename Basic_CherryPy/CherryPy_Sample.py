"""
CherryPy Sample
"""

import random
import string

import cherrypy

class MyHandler(object):
    
    @cherrypy.expose
    def index(self):
        return """<html>
          <head></head>
          <body>
            <form method="get" action="name">
              <input type="text" value="" name="name" />
              <button type="submit">What is your name?</button>
            </form>
          </body>
        </html>"""

    @cherrypy.expose
    def name(self, name="Bruce"):
        body = """<html>
          <head></head>
          <body>
             <h1>Hello {0}</h1>
          </body>
        </html>""".format(name)
        return body


if __name__ == '__main__':
    cherrypy.quickstart(MyHandler())
