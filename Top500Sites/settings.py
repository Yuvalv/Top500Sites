class Settings:
    WEB_LIST_URL = "https://moz.com/top500"
    SITE_LINK_SELECTOR = "#top-500-domains>table>tbody>tr>td>a"
    CONNECTION_STRING = 'mongodb+srv://yuval:Aa123456@cluster0-ufdnr.mongodb.net/test?retryWrites=true&w=majority'
    DB_NAME = "sitesDB"
    COLLECTION_NAME = "sites"
    PING_TIMEOUT = 300
    TIME_BETWEEN_PINGS = 5
