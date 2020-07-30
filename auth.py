import cherrypy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import bcrypt
from models import Base, User

SESSION_KEY = '_cp_username'

DB_CONN = 'postgres+psycopg2://USERNAME:PASSWORD@localhost:5432/DATABASE_TABLE'
db = create_engine(DB_CONN)
Base.metadata.create_all(db)
Session = sessionmaker(bind=db)

def check_credentials(username, password):
    """Verifies credentials for username and password.
    Returns None on success or a string describing the error on failure"""
    sess = Session()
    user = sess.query(User).filter_by(username=username).first()

    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return None
    else:
        return u"Incorrect username or password."

def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a list of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                # A condition is just a callable that returns true or false
                if not condition():
                    raise cherrypy.HTTPRedirect("auth/login")
        else:
            raise cherrypy.HTTPRedirect("auth/login")
cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)

#a decorator to control access
def require(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""
    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f
    return decorate

def login_required():
    """Adds a method to require logins to specific pages"""
    def check():
        sess = Session()
        username = cherrypy.request.login
        user = sess.query(User).filter_by(username=username).first()
        print(user.user_group)
        if not user:
            return False
        else:
            return True
    return check

def member_of(groupname):
    """requires group membership ex: @require(member_of("admin"))"""
    def check():
        username = cherrypy.request.login
        sess = Session()
        user = sess.query(User).filter_by(username=username).first()
        #print(str(info))
        if not user:
            return False
        return groupname == user.user_group
    return check

# Controller to provide login and logout actions
class AuthController(object):
    """checks credentials using the above methods"""
    @cherrypy.expose
    def login(self, username=None, password=None, from_page="/login"):
        """check is user has entered correct credentials and redirects appropriately"""
        if username == None and password == None:
            raise cherrypy.HTTPRedirect("/login")

        error_msg = check_credentials(username, password)
        if error_msg:
            #print("return self.get_loginform(username, error_msg, from_page)")
            raise cherrypy.HTTPRedirect("/login")
        else:
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
            raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def logout(self):
        """kills the sessions and returns to login page"""
        sess = cherrypy.session
        username = sess.get(SESSION_KEY, None)
        sess[SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
            cherrypy.session.clear()
        raise cherrypy.HTTPRedirect("/login")
