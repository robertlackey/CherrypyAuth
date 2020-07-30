import os
import cherrypy
import bcrypt
from jinja2 import Environment, FileSystemLoader
from auth import AuthController, require, login_required, Session
from forms import AddPlay
from models import User

#class level variables
current_dir = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = str(current_dir)+"/templates"
#setup some rendering templates
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), trim_blocks=True)

class Root():
    """main route class"""

    auth = AuthController()

    @cherrypy.expose
    @require(login_required())
    def index(self):
        """home page"""
        template_index = env.get_template('index.html')
        return template_index.render()

    #Define Account Functions
    @cherrypy.expose
    def login(self):
        """login route"""
        template_index = env.get_template('login.html')
        return template_index.render()

    @cherrypy.expose
    def register(self, *args, **kwargs):
        """user registration route"""
        template_index = env.get_template('register.html')
        if cherrypy.request.method == "POST":
            username = cherrypy.request.params['username_input']
            password = cherrypy.request.params['pwd_input']
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()).decode("utf-8")
            group = cherrypy.request.params['group_input']
            print("username: " + username + " , password: " + password + " group: " +group)
            user = User(username=username, password=hashed_password, user_group=group)
            session = Session()
            session.add(user)
            session.commit()

            raise cherrypy.HTTPRedirect("/login")
        return template_index.render()
