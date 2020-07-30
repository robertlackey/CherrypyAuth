import os
import cherrypy
from routes import Root

current_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    cherrypy.server.socket_port = 8080

    conf = {
        '/':    {'tools.staticdir.root': current_dir},
        '/css': {'tools.staticdir.on': True, 'tools.staticdir.dir': 'static/css'},
        '/js':  {'tools.staticdir.on': True, 'tools.staticdir.dir': 'static/js'},
        '/images': {'tools.staticdir.on': True, 'tools.staticdir.dir': 'static/img'}
    }
    cherrypy.config.update({
        'tools.sessions.on': True,
        'tools.auth.on': True

    })

    cherrypy.tree.mount(Root(), "/", conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
