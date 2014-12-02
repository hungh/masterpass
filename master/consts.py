from os.path import expanduser

# user home directory (Linux system)
USER_HOME = expanduser("~")

# path to web application's resources
RESOURCES_HOME = USER_HOME + '/masterpass/resources'

# web application session time-out
SESSION_TIMEOUT = 180000

# keys
USER_ID = "id"
USER_FIRST_NAME = "first"
USER_LAST_NAME = "last"
USER_HASH_PW = "hashpw"
SESSION_USER_ID = "uid"

# database server name
DB_SERVER_HOST = "localhost"
# database listening port
DB_SERVER_PORT = 27017

# web application server name
WEB_SERVER_HOST = "localhost"
# web application binding port
DEFAULT_PORT = 8009

# operations (in controllers)
GET_ACTION = "get"
ADD_ACTION = "add"
UPDATE_ACTION = "update"
DELETE_ACTION = "delete"
RESET_ACTION = "reset"
REDIRECT_ACTION = "redirect"

CHANGE_PW_ACTION = "changepw"
CURRENT_USER_ACTION = "current"
ALL_ACTIVE_SESSION = "active"
GET_PWS_OWNER = "pwsowner"

#mail options
MAIL_USER_NAME = "publicsmtp1@gmail.com"
GMAIL_SMTP = "smtp.gmail.com"
# GOOGLE TSL port
TSL_PORT = 587

# allowed paths in application
ALLOWED_PATHS = ['/login', '/account/reset', '/account/redirect', '/account/update', '/index.html', '/', 'reset.html']

# black list of IP addresses
BLACK_LIST = ['10.9.11.19']

# request speed threshold
SPEED_THRESHOLD = 0.00001

