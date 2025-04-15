import requests
import json

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
            print("[!] Token and Collection already set.")
        return self

    def __getattr__(self, name):
        if not self.token:
            print(f"[!] Error: Token not set. Use DkBotzDB()['YOUR_TOKEN'] before setting collection.")
            return self
        if not self.collection:
            self.collection = name
            print(f"[✓] Collection set to: {name}")
        return self

    def insert_one(self, data):
        if not self.token or not self.collection:
            print("[!] Error: Token or Collection not set.")
            return None
        try:
            response = requests.post(
                f"https://db.dkbotzpro.in/add.php?token={self.token}&collection={self.collection}",
                json=data
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('status'):
                    print("[✓] Records added successfully.")
                    return data.get('result')
                else:
                    print("[!] Record addition failed:", data.get('message'))
            else:
                print(f"[!] Upload failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[!] Exception while uploading: {e}")
        return None

    def find(self, query):
        if not self.token or not self.collection:
            print("[!] Error: Token or Collection not set.")
            return None
        try:
            response = requests.post(
                f"https://db.dkbotzpro.in/search.php?token={self.token}&collection={self.collection}",
                json=query
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('status') and data.get('count', 0) > 0:
                    return data.get('results')
                else:
                    print("[!] No matching entry found.")
            else:
                print(f"[!] Search failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[!] Exception while searching: {e}")
        return None

    def find_one(self, query):
        results = self.find(query)
        if results:
            print("[✓] Found matching entry:", results[0])
            return results[0]
        return None

    def update_one(self, query, update_data):
        if not self.token or not self.collection:
            print("[!] Error: Token or Collection not set.")
            return None
        try:
            response = requests.post(
                f"https://db.dkbotzpro.in/update.php?token={self.token}&collection={self.collection}",
                json={"query": query, "update": update_data}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('status'):
                    print("[✓] Data updated successfully.")
                    return data.get('result')
                else:
                    print("[!] Update failed:", data.get('message'))
            else:
                print(f"[!] Update failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[!] Exception while updating: {e}")
        return None

    def deletemany(self, query):
        if not self.token or not self.collection:
            print("[!] Error: Token or Collection not set.")
            return None
        try:
            response = requests.post(
                f"https://db.dkbotzpro.in/delete.php?token={self.token}&collection={self.collection}",
                json={"query": query}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('status'):
                    print("[✓] Records deleted successfully.")
                    return data.get('result')
                else:
                    print("[!] Deletion failed:", data.get('message'))
            else:
                print(f"[!] Deletion failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[!] Exception while deleting: {e}")
        return None

    def delete_one(self, query):
        if not self.token or not self.collection:
            print("[!] Error: Token or Collection not set.")
            return None
        try:
            response = requests.post(
                f"https://db.dkbotzpro.in/delete_one.php?token={self.token}&collection={self.collection}",
                json={"query": query}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('status'):
                    print("[✓] One record deleted successfully.")
                    return data.get('result')
                else:
                    print("[!] Deletion failed:", data.get('message'))
            else:
                print(f"[!] Deletion failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[!] Exception while deleting one record: {e}")
        return None

    def count_documents(self, query={}):
        if not self.token or not self.collection:
            print("[!] Error: Token or Collection not set.")
            return 0
        try:
            response = requests.post(
                f"https://db.dkbotzpro.in/count.php?token={self.token}&collection={self.collection}",
                json={"query": query}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('status'):
                    print(f"[#] Matching Documents: {data['count']}")
                    return data['count']
                else:
                    print("[!] Count failed:", data.get('message'))
                    return 0
            else:
                print(f"[!] Count failed: {response.status_code} - {response.text}")
                return 0
        except Exception as e:
            print(f"[!] Exception while counting documents: {e}")
            return 0

