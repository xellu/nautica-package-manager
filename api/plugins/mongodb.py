from nautica import Service, Config, ConfigBuilder, Logger, Services

import threading
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from pymongo.errors import ServerSelectionTimeoutError

class MongoDB(Service):
    def __init__(self):
        super().__init__()
        
        self.client: MongoClient | None = None
        self.thread = None
        
        self.is_connected = False
        
    def onInstall(self):
        Config.Update("nautica", ConfigBuilder()
            .add("services.mongodb", False, comment="Enable MongoDB Connector")
            .build()
        )
        Config.New("mongodb",
            ConfigBuilder()
                .add("url", "mongodb://localhost:27017", comment="MongoDB connection string")
                .add("database", "nautica", comment="Database name")
                .add("timeout", 5000, comment="Connection timeout (in ms)")
                .add("crashOnTimeout", False, comment="Stop the server if the database fails to connect")
                .build()
        )
    
    def onStart(self, registry):
        self.thread = t = threading.Thread(target=self._connect, daemon=True)
        t.start()
    
    def onClose(self, reason):
        self.is_connected = False
        if self.client:
            self.client.close()
            
    def isEnabled(self):
        return Config("nautica")["services.mongodb"]
    
    def _connect(self) -> None:
        try:
            uri = Config("mongodb")["url"]    
            timeout = Config("mongodb")["timeout"]
            self.client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=timeout)

            try:
                self.client.admin.command('ping')
                Logger.ok("Connection established")
                self.is_connected = True
                
            except ServerSelectionTimeoutError:
                self.is_connected = False
                Logger.error(f"Connection to server timed out")
                if Config("mongodb")["crashOnTimeout"]:
                    Services.onClose("MongoDB failed to connect")
                return
                
            except Exception as e:
                self.is_connected = False
                Logger.trace(e)
                return


        except Exception as e:
            self.is_connected = False
            Logger.trace(e)
            return
        
    def __call__(self, collection) -> Collection:
        if not self.client:
            raise RuntimeError("MongoDB is not connected yet")
        
        return self.client.get_database(Config("mongodb")["database"]).get_collection(collection)
    
    
Service.Export(MongoDB)