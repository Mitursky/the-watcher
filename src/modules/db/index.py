import pymongo
    
class USERS_DB:
    def __init__(self):
        self.db = pymongo.MongoClient("localhost", 27017)
        self.db = self.db.test.users
        
    def find(self, id):
        user = self.db.find_one({"_id":id})
     
        if not user:
            user = {"_id":id, "tracking":{}}
            self.db.insert_one(user)
            
        return user
    
    def save(self, id, change):
        self.db.update_one({"_id":id}, change)
        
db = USERS_DB()
