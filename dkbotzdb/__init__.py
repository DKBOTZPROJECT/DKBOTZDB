import requests
import json
import logging
import colorlog

# Colored log formatter
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    fmt='%(log_color)s[#] %(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
))

logger = colorlog.getLogger('dkbotzdb')
logger.addHandler(handler)
logger.setLevel(logging.INFO)  # Change to DEBUG if needed
logger.propagate = False

class DkBotzDB:
    def __init__(self, token=None):
        self.token = token
        self.collection = None

    def __getitem__(self, key):
        if not self.token:
            self.token = key
        elif not self.collection:
            self.collection = key
        else:
            logger.warning("Token and Collection already set.")
        return self

    def __getattr__(self, name):
        if not self.token:
            logger.error("Token not set. Use DkBotzDB()['YOUR_TOKEN'] before setting collection.")
            return self
        if not self.collection:
            self.collection = name
            logger.info(f"Collection set to: {name}")
        return self

    def insert_one(self, data):
        if not self.token or not self.collection:
            logger.error("Token or Collection not set.")
            return None
        try:
            response = requests.post(
                f"https://db.dkbotzpro.in/add.php?token={self.token}&collection={self.collection}",
                json=data
            )
            if response.status_code == 200:
                res_data = response.json()
                if res_data.get('status'):
                    logger.info("Records added successfully.")
                    return res_data.get('result')
                else:
                    logger.warning(f"Record addition failed: {res_data.get('message')}")
            else:
                logger.error(f"Upload failed: {response.status_code} - {response.text}")
        except Exception as e:
            logger.exception(f"Exception while uploading: {e}")
        return None

    def find(self, query):
        if not self.token or not self.collection:
            logger.error("Token or Collection not set.")
            return None
        try:
            response = requests.post(
                f"https://db.dkbotzpro.in/search.php?token={self.token}&collection={self.collection}",
                json=query
            )
            if response.status_code == 200:
                res_data = response.json()
                if res_data.get('status') and res_data.get('count', 0) > 0:
                    return res_data.get('results')
                else:
                    logger.info("No matching entry found.")
            else:
                logger.error(f"Search failed: {response.status_code} - {response.text}")
        except Exception as e:
            logger.exception(f"Exception while searching: {e}")
        return None

    def find_one(self, query):
        results = self.find(query)
        if results:
            logger.info(f"Found matching entry: {results[0]}")
            return results[0]
        return None

    def update_one(self, query, update_data):
        if not self.token or not self.collection:
            logger.error("Token or Collection not set.")
            return None
        try:
            response = requests.post(
                f"https://db.dkbotzpro.in/update.php?token={self.token}&collection={self.collection}",
                json={"query": query, "update": update_data}
            )
            if response.status_code == 200:
                res_data = response.json()
                if res_data.get('status'):
                    logger.info("Data updated successfully.")
                    return res_data.get('result')
                else:
                    logger.warning(f"Update failed: {res_data.get('message')}")
            else:
                logger.error(f"Update failed: {response.status_code} - {response.text}")
        except Exception as e:
            logger.exception(f"Exception while updating: {e}")
        return None

    def deletemany(self, query):
        if not self.token or not self.collection:
            logger.error("Token or Collection not set.")
            return None
        try:
            response = requests.post(
                f"https://db.dkbotzpro.in/delete.php?token={self.token}&collection={self.collection}",
                json={"query": query}
            )
            if response.status_code == 200:
                res_data = response.json()
                if res_data.get('status'):
                    logger.info("Records deleted successfully.")
                    return res_data.get('result')
                else:
                    logger.warning(f"Deletion failed: {res_data.get('message')}")
            else:
                logger.error(f"Deletion failed: {response.status_code} - {response.text}")
        except Exception as e:
            logger.exception(f"Exception while deleting: {e}")
        return None

    def delete_one(self, query):
        if not self.token or not self.collection:
            logger.error("Token or Collection not set.")
            return None
        try:
            response = requests.post(
                f"https://db.dkbotzpro.in/delete_one.php?token={self.token}&collection={self.collection}",
                json={"query": query}
            )
            if response.status_code == 200:
                res_data = response.json()
                if res_data.get('status'):
                    logger.info("One record deleted successfully.")
                    return res_data.get('result')
                else:
                    logger.warning(f"Deletion failed: {res_data.get('message')}")
            else:
                logger.error(f"Deletion failed: {response.status_code} - {response.text}")
        except Exception as e:
            logger.exception(f"Exception while deleting one record: {e}")
        return None

    def count_documents(self, query={}):
        if not self.token or not self.collection:
            logger.error("Token or Collection not set.")
            return 0
        try:
            response = requests.post(
                f"https://db.dkbotzpro.in/count.php?token={self.token}&collection={self.collection}",
                json={"query": query}
            )
            if response.status_code == 200:
                res_data = response.json()
                if res_data.get('status'):
                    logger.info(f"Matching Documents: {res_data['count']}")
                    return res_data['count']
                else:
                    logger.warning(f"Count failed: {res_data.get('message')}")
            else:
                logger.error(f"Count failed: {response.status_code} - {response.text}")
        except Exception as e:
            logger.exception(f"Exception while counting documents: {e}")
        return 0
