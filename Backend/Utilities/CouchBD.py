from datetime import timedelta
# needed for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
# needed for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,
                               QueryOptions)

HOST = 'couchbase://localhost'

class CouchBD():
    def __init__(self):
        print("[CouchBD] DataBaseInstance created")


    def login(self, username, password):
        self._bucket_name = "Test-bucket-big"
        cert_path = "path/to/certificate"

        self._auth = PasswordAuthenticator(
                    username,
                    password,
                    # NOTE: If using SSL/TLS, add the certificate path.
                    # We strongly reccomend this for production use.
                    # cert_path=cert_path
                    )
        try:
            self._cluster = Cluster(HOST, ClusterOptions(self._auth))
            self._cluster.wait_until_ready(timedelta(seconds=1))      
            self._cb = self._cluster.bucket(self._bucket_name)
            self._cb_coll = self._cb.scope("events").collection("city")
        except:
            print("[CouchBD] Login exception")
            return False

        return True

    def upsert_document(self, doc):
        print("\nUpsert CAS: ")
        try:
            # key will equal: "airline_8091"
            
            key = doc["type"] + "_" + str(doc["id"])
            result = self._cb_coll.upsert(key, doc)
            print(result.cas)
        except Exception as e:
            print(e)



    def get_airline_by_key(self, key):
        print("\nGet Result: ")
        try:
            result = self._cb_coll.get(key)
            print(result.content_as[str])
        except Exception as e:
            print(e)


    def lookup_by_callsign(self, cs):
        print("\nLookup Result: ")
        try:
            sql_query = 'SELECT VALUE name FROM `travel-sample`.inventory.airline WHERE callsign = $1'
            row_iter = self._cluster.query(
                sql_query,
                QueryOptions(positional_parameters=[cs]))
            for row in row_iter:
                print(row)
        except Exception as e:
            print(e)

    
    def close(self):
        self._cluster.close()
        print("[CouchBD] Closing DB connection")


    def __del__(self):
        self.close()