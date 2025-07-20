
import requests
import json
import logging
import colorlog

# Colored log formatter
handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        fmt='%(log_color)s[#] %(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }))

logger = colorlog.getLogger('dkbotzdb')
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False

BASE_API = "https://db.dkbotzpro.in/api"


class DKBOTZDB:

    def __init__(self, token=None, base_url=BASE_API):
        self.token = token
        self.base_url = base_url
        self.collection = None

    def __getitem__(self, key):
        """Support for db['token']['collection'] syntax"""
        if not self.token:
            self.token = key
            logger.info(f"Token set via bracket notation")
        elif not self.collection:
            self.collection = key
            logger.info(f"Collection set to: {key}")
        else:
            logger.warning("Token and Collection already set.")
        return self

    def __getattr__(self, name):
        """Support for db.token or db.collection syntax"""
        if not self.token:
            self.token = name
            logger.info(f"Token set via attribute: {name}")
        elif not self.collection:
            self.collection = name
            logger.info(f"Collection set to: {name}")
        return self

    def _validate_setup(self):
        """Validate token and collection are set"""
        if not self.token:
            logger.error("Token not set. Please set token first.")
            return False
        if not self.collection:
            logger.error("Collection not set. Please set collection first.")
            return False
        return True

    def _make_request(self, method, url, data=None, params=None, max_retries=3):
        """Make HTTP request with retry logic and error handling"""
        for attempt in range(1, max_retries + 1):
            try:
                if method.upper() == 'GET':
                    response = requests.get(url, params=params, timeout=30)
                else:
                    response = requests.post(url, json=data, params=params, timeout=30)
                
                if response.status_code == 200:
                    try:
                        result = response.json()
                        return result
                    except json.JSONDecodeError:
                        logger.error("Invalid JSON response from server")
                        return None
                else:
                    logger.warning(f"Attempt {attempt}: Server responded with {response.status_code} - {response.text}")
                    
            except requests.exceptions.Timeout:
                logger.warning(f"Attempt {attempt}: Request timeout")
            except requests.exceptions.ConnectionError:
                logger.warning(f"Attempt {attempt}: Connection error")
            except Exception as e:
                logger.warning(f"Attempt {attempt}: Request failed with exception: {e}")
                
            if attempt < max_retries:
                logger.info("Retrying...")
                
        logger.error(f"All {max_retries} attempts failed for URL: {url}")
        return None

    def _handle_response(self, response, success_message=None):
        """Handle API response and logging"""
        if not response:
            return None
            
        if response.get('status'):
            if success_message:
                logger.info(success_message)
            return response.get('result') or response.get('data') or response.get('results')
        else:
            error_msg = response.get('message', 'Unknown error')
            logger.error(f"Operation failed: {error_msg}")
            return None

    # CRUD Operations
    def insert_one(self, data):
        """Insert a single document"""
        if not self._validate_setup():
            return None
            
        params = {
            "action": "insertOne",
            "collection": self.collection,
            "token": self.token
        }
        
        response = self._make_request('POST', self.base_url, data=data, params=params)
        return self._handle_response(response, "Document inserted successfully")

    def insertOne(self, data):
        """Alias for insert_one"""
        return self.insert_one(data)

    def insert_many(self, data_list):
        """Insert multiple documents"""
        if not self._validate_setup():
            return None
            
        params = {
            "action": "insertMany",
            "collection": self.collection,
            "token": self.token
        }
        
        response = self._make_request('POST', self.base_url, data=data_list, params=params)
        return self._handle_response(response, f"Inserted {len(data_list)} documents successfully")

    def insertMany(self, data_list):
        """Alias for insert_many"""
        return self.insert_many(data_list)

    def find_one(self, query=None):
        """Find a single document"""
        if not self._validate_setup():
            return None
            
        params = {
            "action": "findOne",
            "collection": self.collection,
            "token": self.token
        }
        
        data = {"query": query} if query else {}
        response = self._make_request('POST', self.base_url, data=data, params=params)

        if not response:
            return None
        
        if response['status']:
            logger.info(response['message'])
            return response['data']
        else:
            logger.info(response['message'])
            return None


    def findOne(self, query=None):
        """Alias for find_one"""
        return self.find_one(query)

    def find(self, query=None, limit=None, sort=None, skip=None):
        """Find multiple documents"""
        if not self._validate_setup():
            return None
            
        params = {
            "action": "find",
            "collection": self.collection,
            "token": self.token
        }
        
        data = {}
        if query:
            data["query"] = query
        if limit:
            data["limit"] = limit
        if sort:
            data["sort"] = sort
        if skip:
            data["skip"] = skip
        
        response = self._make_request('POST', self.base_url, data=data, params=params)
        
        if not response:
            return None
        
        if response['status']:
            logger.info(response['message'])
            return response['data']
        else:
            logger.info(response['message'])
            return None

    def update_one(self, query, update):
        """Update a single document"""
        if not self._validate_setup():
            return None
            
        params = {
            "action": "updateOne",
            "collection": self.collection,
            "token": self.token
        }
        
        data = {
            "query": query,
            "update": update
        }
        
        response = self._make_request('POST', self.base_url, data=data, params=params)
        return self._handle_response(response, "Document updated successfully")

    def updateOne(self, query, update):
        """Alias for update_one"""
        return self.update_one(query, update)

    def update_many(self, query, update):
        """Update multiple documents"""
        if not self._validate_setup():
            return None
            
        params = {
            "action": "updateMany",
            "collection": self.collection,
            "token": self.token
        }
        
        data = {
            "query": query,
            "update": update
        }
        
        response = self._make_request('POST', self.base_url, data=data, params=params)
        return self._handle_response(response, "Documents updated successfully")

    def updateMany(self, query, update):
        """Alias for update_many"""
        return self.update_many(query, update)

    def delete_one(self, query):
        """Delete a single document"""
        if not self._validate_setup():
            return None
            
        params = {
            "action": "deleteOne",
            "collection": self.collection,
            "token": self.token
        }
        
        data = {"query": query}
        response = self._make_request('POST', self.base_url, data=data, params=params)
        return self._handle_response(response, "Document deleted successfully")

    def deleteOne(self, query):
        """Alias for delete_one"""
        return self.delete_one(query)

    def delete_many(self, query):
        """Delete multiple documents"""
        if not self._validate_setup():
            return None
            
        params = {
            "action": "deleteMany",
            "collection": self.collection,
            "token": self.token
        }
        
        data = {"query": query}
        response = self._make_request('POST', self.base_url, data=data, params=params)
        return self._handle_response(response, "Documents deleted successfully")

    def deleteMany(self, query):
        """Alias for delete_many"""
        return self.delete_many(query)

    # Advanced Operations
    def count_documents(self, query=None):
        """Count documents matching query"""
        if not self._validate_setup():
            return None
            
        params = {
            "action": "countDocuments",
            "collection": self.collection,
            "token": self.token
        }
        
        data = {"query": query} if query else {}
        response = self._make_request('POST', self.base_url, data=data, params=params)
        if not response:
            return 0
        
        if response['status']:
            logger.info(response['message'])
            return response['data']['count']
        else:
            logger.info(response['message'])
            return 0

    def countDocuments(self, query=None):
        """Alias for count_documents"""
        return self.count_documents(query)
    
    def count(self, query=None):
        """Alias for count_documents"""
        return self.count_documents(query)

    def aggregate(self, query=None, regex=None, range_filter=None, sort=None, limit=None, skip=None, count_only=False):
        """Advanced query with filters"""
        if not self._validate_setup():
            return None
            
        params = {
            "action": "aggregate",
            "collection": self.collection,
            "token": self.token
        }
        
        data = {}
        if query:
            data["query"] = query
        if regex:
            data["regex"] = regex
        if range_filter:
            data["range"] = range_filter
        if sort:
            data["sort"] = sort
        if limit:
            data["limit"] = limit
        if skip:
            data["skip"] = skip
        if count_only:
            data["count_only"] = count_only
        
        response = self._make_request('POST', self.base_url, data=data, params=params)
        if not response:
            return None
        
        if response['status']:
            logger.info(response['message'])
            return response['data']
        else:
            logger.info(response['message'])
            return None
        
    def smart_find(self, **kwargs):
        """Alias for aggregate"""
        return self.aggregate(**kwargs)

    def distinct(self, field, query=None):
        """Get distinct values for a field"""
        if not self._validate_setup():
            return None
            
        params = {
            "action": "distinct",
            "collection": self.collection,
            "token": self.token
        }
        
        data = {"field": field}
        if query:
            data["query"] = query
        
        response = self._make_request('POST', self.base_url, data=data, params=params)
        if not response:
            return None
        
        if response['status']:
            logger.info(response['message'])
            return response['data']
        else:
            logger.info(response['message'])
            return None
        
    def replace_one(self, query, replacement):
        """Replace a single document"""
        if not self._validate_setup():
            return None
            
        params = {
            "action": "replaceOne",
            "collection": self.collection,
            "token": self.token
        }
        
        data = {
            "query": query,
            "replacement": replacement
        }
        
        response = self._make_request('POST', self.base_url, data=data, params=params)
        return self._handle_response(response, "Document replaced successfully")

    def replaceOne(self, query, replacement):
        """Alias for replace_one"""
        return self.replace_one(query, replacement)

    # Collection Management
    def drop(self):
        """Drop current collection"""
        if not self._validate_setup():
            return None
            
        params = {
            "action": "drop",
            "collection": self.collection,
            "token": self.token
        }
        
        response = self._make_request('POST', self.base_url, data={}, params=params)
        return self._handle_response(response, f"Collection '{self.collection}' dropped successfully")

    def drop_all(self):
        """Drop all collections"""
        if not self.token:
            logger.error("Token not set")
            return None
            
        params = {
            "action": "dropall",
            "collection": "any",
            "token": self.token
        }
        
        response = self._make_request('POST', self.base_url, data={}, params=params)
        return self._handle_response(response, "All collections dropped successfully")

    def dropall(self):
        """Alias for drop_all"""
        return self.drop_all()

    def collections(self):
        """List all collections"""
        if not self.token:
            logger.error("Token not set")
            return None
            
        params = {
            "action": "collections",
            "collection": "any",
            "token": self.token
        }
        
        response = self._make_request('POST', self.base_url, data={}, params=params)
        if not response:
            return None
        
        if response['status']:
            logger.info(response['message'])
            return response['data']
        else:
            logger.info(response['message'])
            return None
        
    def usage_info(self):
        """Get usage information"""
        if not self.token:
            logger.error("Token not set")
            return None
            
        params = {
            "action": "usage_info",
            "collection": "any",
            "token": self.token
        }
        
        response = self._make_request('POST', self.base_url, data={}, params=params)
        if not response:
            return None
        
        if response['status']:
            logger.info(response['message'])
            return response['data']
        else:
            logger.info(response['message'])
            return None
        
    # Token & Plan Management
    def get_token_info(self, check_token=None):
        """Get token information"""
        token_to_check = check_token or self.token
        if not token_to_check:
            logger.error("No token provided")
            return None
            
        params = {
            "action": "get_token_info",
            "check_token": token_to_check
        }
        
        response = self._make_request('GET', self.base_url, params=params)
        if not response:
            return None
        
        if response['status']:
            logger.info(response['message'])
            return response['data']
        else:
            logger.info(response['message'])
            return None
        
    def token_info(self, check_token=None):
        """Alias for get_token_info"""
        return self.get_token_info(check_token)

    def token_details(self, check_token=None):
        """Alias for get_token_info"""
        return self.get_token_info(check_token)

    def plan_status(self, user_token=None):
        """Check plan status"""
        token_to_check = user_token or self.token
        if not token_to_check:
            logger.error("No token provided")
            return None
            
        params = {
            "action": "plan_status",
            "user_token": token_to_check
        }
        
        response = self._make_request('GET', self.base_url, params=params)
        if not response:
            return None
        
        if response['status']:
            logger.info(response['message'])
            return response['data']
        else:
            logger.info(response['message'])
            return None
        
    def check_plan(self, user_token=None):
        """Alias for plan_status"""
        return self.plan_status(user_token)

    def user_plan(self, user_token=None):
        """Alias for plan_status"""
        return self.plan_status(user_token)

    def list_plans(self):
        """List available plans"""
        params = {"action": "plans"}
        response = self._make_request('GET', self.base_url, params=params)
        if not response:
            return None
        
        if response['status']:
            logger.info(response['message'])
            return response['data']
        else:
            logger.info(response['message'])
            return None
        
    def plans(self):
        """Alias for list_plans"""
        return self.list_plans()

    def get_plans(self):
        """Alias for list_plans"""
        return self.list_plans()

    # Admin Operations (require admin token)
    def generate_token(self, name, plan_id, duration_days):
        """Generate new token (admin only)"""
        if not self.token:
            logger.error("Admin token not set")
            return None
            
        params = {
            "action": "generate_token",
            "token": self.token
        }
        
        data = {
            "name": name,
            "plan_id": plan_id,
            "duration_days": duration_days
        }
        
        response = self._make_request('POST', self.base_url, data=data, params=params)
        if not response:
            return None
        
        if response['status']:
            logger.info(response['message'])
            return response['data']
        else:
            logger.info(response['message'])
            return None
        
    def create_token(self, name, plan_id, duration_days):
        """Alias for generate_token"""
        return self.generate_token(name, plan_id, duration_days)

    def admin_token(self, name, plan_id, duration_days):
        """Alias for generate_token"""
        return self.generate_token(name, plan_id, duration_days)

    def activate_plan(self, user_token, plan_id, duration_days):
        """Activate plan for user (admin only)"""
        if not self.token:
            logger.error("Admin token not set")
            return None
            
        params = {
            "action": "activate_plan",
            "token": self.token
        }
        
        data = {
            "user_token": user_token,
            "plan_id": plan_id,
            "duration_days": duration_days
        }
        
        response = self._make_request('POST', self.base_url, data=data, params=params)
        if not response:
            return None
        
        if response['status']:
            logger.info(response['message'])
            return response['data']
        else:
            logger.info(response['message'])
            return None

DkBotzDB = DKBOTZDB
DKBOTZdb = DKBOTZDB
