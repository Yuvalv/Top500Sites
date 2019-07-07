import pymongo
from settings import Settings


class SitesRepository:
    def __init__(self):
        self.__client = pymongo.MongoClient(Settings.CONNECTION_STRING)
        self.__db = self.__client[Settings.DB_NAME]
        self._coll = self.__db[Settings.COLLECTION_NAME]

    def get_site(self, site_name):
        query = {"site_name": site_name}
        site = self._coll.find_one(query)
        return site

    def insert_site(self, site_name):
        doc = {"site_name": site_name, "latency": []}
        self._coll.insert_one(doc)

    def push_latency(self, site_name, latency):
        query = {"site_name": site_name}
        values = {"$push": {"latency": latency}}
        self._coll.update_one(query, values)

    def get_sites_last_latency(self):
        sites = list(self._coll.find({}, {"'ObjectId": 0, "latency": {"$slice": -1}}))
        return sites

    def __del__(self):
        self.__client.close()
