from settings import Settings
from pythonping import ping
from requests_html import HTMLSession
from sites_repository import SitesRepository
session = HTMLSession()


class SiteManager:
    """
    This method get list of sites URL from the provided site
    @:param web_list_url: the provided site url
    @:return List of sites urls
    """
    @classmethod
    def get_sites_from_web(cls, web_list_url):
        sites = []
        r = session.get(web_list_url)

        # to get the specific column we use html element selector
        sits_elements = r.html.find(Settings.SITE_LINK_SELECTOR, first=False);
        if len(sits_elements) is not None:
            for site in sits_elements:
                sites.append(site.text)

        return sites

    """
    This method make ping to specific site and store the latency in the DB
    @:param site_url: the site url
    """
    @classmethod
    def ping_site_and_store(cls, site_url):
        latency = cls.__ping_site(site_url)
        rep = SitesRepository()
        rep.push_latency(site_url, latency)


    """
    This method make ping to specific site (used by ping_site_and_store)
    If its doesnt success the method try to add www prefix and ping again
    @:param site_url: the site url
    @:param add_prefix: used for the retrying recursing
    @:return time of latency or -1 if no pong
    """
    @classmethod
    def __ping_site(cls, site_url, add_prefix=False):
        try:
            if add_prefix:
                site_url = "www.{}".format(site_url)

            response_list = ping(site_url, size=40, count=1, timeout=(Settings.PING_TIMEOUT / 1000))
            # if equal to timeout limitation
            if response_list.rtt_avg_ms == Settings.PING_TIMEOUT:
                raise Exception("timeout")

            return response_list.rtt_avg_ms
        except:
            # if failed after the adding prefix return -1
            if add_prefix:
                return -1
            # If failed try to add prefix
            else:
                return cls.__ping_site(site_url, True)


    """
    This method create document in db for site if not exist
    @:param site_url: the site url
    """
    @classmethod
    def create_site_document_if_needed(cls, site_url):
        if not cls.__check_site_document_exist(site_url):
            rep = SitesRepository()
            rep.insert_site(site_url)
            return

    """
    This method get list of sites and each site the last latency check
    @:return list of sites and latencies
    """
    @classmethod
    def get_sites_from_db(cls):
        rep = SitesRepository()
        sites = rep.get_sites_last_latency()
        return sites

    """
    This method if the site has document in db
    @:param site_url: the site url
    @:return True - if document exist otherwise False
    """
    @classmethod
    def __check_site_document_exist(cls, site_url):
        rep = SitesRepository()
        return rep.get_site(site_url) is not None


