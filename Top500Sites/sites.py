import threading
import time
from requests_html import HTMLSession
from settings import Settings
from site_manager import SiteManager
session = HTMLSession()


class Sites:
    @classmethod
    def thread_function(cls, site):
        # create document for site
        SiteManager.create_site_document_if_needed(site)
        while True:

            # make ping store the result and wait Settings.TIME_BETWEEN_PINGS
            SiteManager.ping_site_and_store(site)
            time.sleep(Settings.TIME_BETWEEN_PINGS)

    """
    This method get data for the sits and sore in db
    """
    @classmethod
    def get_data_from_site_and_store(cls):
        threads = list()
        # Limit the sites to 10 because the poor free DB
        sites = SiteManager.get_sites_from_web(Settings.WEB_LIST_URL)[:10]

        # for each site create  thread
        for site in sites:
            x = threading.Thread(target=cls.thread_function, args=(site,))
            threads.append(x)
            x.start()

        # join the threads
        for index, thread in enumerate(threads):
            thread.join()

    """
    This method get list of sites and each site the last latency check
    @:return list of sites and latencies
    """
    @classmethod
    def get_sites_from_db(cls):
        return SiteManager.get_sites_from_db()
