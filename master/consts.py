from os.path import expanduser

USER_HOME = expanduser("~")
RESOURCES_HOME = USER_HOME + '/masterpass/resources'
SESSION_TIMEOUT = 180000
USER_ID = "id"
USER_FIRST_NAME = "first"
USER_LAST_NAME = "last"
USER_HASH_PW = "hashpw"
DB_SERVER_HOST = "localhost"
DB_SERVER_PORT = 27017
SESSION_USER_ID = "uid"
# operations
CHANGE_PW_ACTION = "changepw"
CURRENT_USER_ACTION = "current"
ALL_ACTIVE_SESSION = "active"
GET_PWS_OWNER = "pwsowner"
GET_ACTION = "get"
ADD_ACTION = "add"
UPDATE_ACTION = "update"
DELETE_ACTION = "delete"
RESET_ACTION = "reset"
DEFAULT_PORT = 8009
