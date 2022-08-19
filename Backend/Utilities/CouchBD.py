from datetime import timedelta

# needed for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
# needed for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,
                               QueryOptions)

import time

class CouchBD():
    def __init__(self):
        print("BD creada")


    def login(self, username, password):
        self.username = username
        self.password = password
        self.bucket_name = "Test-bucket-big"
        cert_path = "path/to/certificate"

        self.auth = PasswordAuthenticator(
                    self.username,
                    self.password,
                    # NOTE: If using SSL/TLS, add the certificate path.
                    # We strongly reccomend this for production use.
                    # cert_path=cert_path
                    )
        
        self.cluster = Cluster('couchbase://localhost', ClusterOptions(self.auth))
        if self.cluster is None:
            return False

        self.cluster.wait_until_ready(timedelta(seconds=1))      
        self.cb = self.cluster.bucket(self.bucket_name)
        self.cb_coll = self.cb.scope("events").collection("city")

        return True

    def upsert_document(self, doc):
        print("\nUpsert CAS: ")
        try:
            # key will equal: "airline_8091"
            
            key = doc["type"] + "_" + str(doc["id"])
            result = self.cb_coll.upsert(key, doc)
            print(result.cas)
        except Exception as e:
            print(e)



    def get_airline_by_key(self, key):
        print("\nGet Result: ")
        try:
            result = self.cb_coll.get(key)
            print(result.content_as[str])
        except Exception as e:
            print(e)


    def lookup_by_callsign(self, cs):
        print("\nLookup Result: ")
        try:
            sql_query = 'SELECT VALUE name FROM `travel-sample`.inventory.airline WHERE callsign = $1'
            row_iter = self.cluster.query(
                sql_query,
                QueryOptions(positional_parameters=[cs]))
            for row in row_iter:
                print(row)
        except Exception as e:
            print(e)