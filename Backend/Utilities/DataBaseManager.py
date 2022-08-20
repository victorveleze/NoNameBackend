from xml.dom.expatbuilder import FragmentBuilderNS
from Backend.Utilities.CouchBD import CouchBD
from Backend.Utilities.Singleton import Singleton


class DataBaseManager(metaclass=Singleton):
    def __init__(self):
        print("[DataBaseManager] DataBaseManager instanced")

        self._database = CouchBD()
        self._username = None
        self._password = None
        self._userIsLogged = False


    def login(self, username, password):
        loginSuccess = self._database.login(username, password)
        if loginSuccess:
            self._database.close()
            self._userIsLogged = True
            self._username = username
            self._password = password
            log = "[DataBaseManager] Login success"
        else:
            log = "[DataBaseManager] Login failed"
        
        print(log)
        return loginSuccess


    def upsert(self, doc):
        if self._userIsLogged:
            self._database.login(self._username, self._password)
            self._database.upsert_document(doc)
            return True

        return False