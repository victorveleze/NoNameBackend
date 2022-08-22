from datetime import timedelta
# needed for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
# needed for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,
                               QueryOptions)

HOST = 'couchbase://localhost'
DB_USER = 'Victor'
DB_PASS = 'victor'

class CouchBD():
    def __init__(self):
        print("[CouchBD] DataBaseInstance created")
        self._bucket_name = "Test-bucket-big"
        cert_path = "path/to/certificate"

        self._auth = PasswordAuthenticator(
                    DB_USER,
                    DB_PASS,
                    # NOTE: If using SSL/TLS, add the certificate path.
                    # We strongly reccomend this for production use.
                    # cert_path=cert_path
                    )
        self._cluster = Cluster(HOST, ClusterOptions(self._auth))
        self._cluster.wait_until_ready(timedelta(seconds=1))      
        #self._cb = self._cluster.bucket(self._bucket_name)
        #self._cb_coll = self._cb.scope("events").collection("city")    


    def insert_document(self, doc, bucketName, scopeName, collectionName, key) -> bool:
        print("\nInsert CAS: ")
        try:
            bucket = self._cluster.bucket(bucketName)
            bucketCollection = bucket.scope(scopeName).collection(collectionName)
            result = bucketCollection.insert(key, doc)
            insertSuccess = True
            print(result.cas)
        except Exception as e:
            insertSuccess = False
            print(e)

        return insertSuccess


    def upsert_document(self, doc, bucketName, scopeName, collectionName, key) -> bool:
        print("\nUpsert CAS: ")
        try:
            bucket = self._cluster.bucket(bucketName)
            bucketCollection = bucket.scope(scopeName).collection(collectionName)
            result = bucketCollection.upsert(key, doc)
            upsertSuccess = True
            print(result.cas)
        except Exception as e:
            upsertSuccess = False
            print(e)

        return upsertSuccess


    def get_user_by_key(self, bucketName, scopeName, collectionName, key) -> dict:
        print("\nGet Result: ")
        try:
            bucket = self._cluster.bucket(bucketName)
            bucketCollection = bucket.scope(scopeName).collection(collectionName)
            user = bucketCollection.get(key).content_as[dict]
        except Exception as e:
            print(e)
            user = None

        return user


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