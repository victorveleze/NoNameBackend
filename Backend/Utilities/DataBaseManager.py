from xml.dom.expatbuilder import FragmentBuilderNS
from Backend.Utilities.CouchBD import CouchBD
from Backend.Utilities.Singleton import Singleton


class DataBaseManager(metaclass=Singleton):
    def __init__(self):
        print("[DataBaseManager] DataBaseManager instanced")

        self._username = None
        self._password = None
        self._userIsLogged = False


    def login(self, username, password):
        db = CouchBD()
        user = db.get_user_by_key("NoName-Bucket", "Users", "Info", username)
        if user is not None:
            if  user["password"] == password:
                self._userIsLogged = True
                self._username = username
                self._password = password
                status = "Login success"
                success = True
            else:
                status = "Incorrect password"
                success = False
        else:
            status = "User does not exist"
            success = False

        print(status)
        return (success, status)


    def insert_user(self, doc):
        key = doc["user_email"]
        db = CouchBD()
        insertSuccess = db.insert_document(doc, "NoName-Bucket", "Users", "Info", key)
        return insertSuccess
