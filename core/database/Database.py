from pymongo import MongoClient
from config import DATEBASE



client = MongoClient(DATEBASE)
db = client["show"]
"""
4 БД
Менеджери 
Закази менеджеров 
Корзина покупателя
"""



class Base:
    def __init__(self, collections_name):
        self.collection = db[collections_name]
    
    async def get_all(self)->list:
        results = []
        for doc in self.collection.find(projection={'_id':False}):
            results.append(doc)
        return results
    
    async def add(self,data):
        self.collection.replace_one(filter={"name":data.get("name")},replacement=data,upsert=True)
   

class Manager(Base):
    def __init__(self):
        super().__init__("manager") 
    async def add(self,data:dict):
        self.collection.replace_one(filter={"id":data.get("id")},replacement=data,upsert=True)
    
    async def delete_manger(self,name:str)->bool:
        if name.isdigit():
            result = self.collection.delete_one(filter={"id":name})
        else: 
            result = self.collection.delete_one(filter={"name":name})
        if result == 1:
            return True
        else:
            return False

    

    
        
            
            


class Product(Base):
    def __init__(self):
        super().__init__("product") 

    

    

class Order(Base):
    def __init__(self):
        super().__init__("order")

    async def add(self,data:dict):
        self.collection.replace_one(filter={"Статус":"Открыт","id":data.get("id")},replacement=data,upsert=True)
    
    async def get_order(self,user_id):
        return self.collection.find_one(filter={"Статус":"Открыт","id":user_id},projection={"Статус":False,"id":False, "_id":0})
# """,projection={"Статус":"Открыт","id":0, "_id":0}"""
    async def delete_order(self,user_id):
        self.collection.delete_one(filter={"Статус":"Открыт","id":user_id})
  
    # async def get_order(self,user_id:str)->list:
    #     result=[]
    #     order = self.collection.find(filter={"Статус":"Открыт","id":{"$regex":f".*{user_id}$"}},projection={"_id":0})
    #     for doc in order:
    #         result.append(doc)
    #     return result
    
    async def get_order_open(self) -> list:
        results = []
        for doc in self.collection.find(filter={"Статус":"Открыт"},projection={'_id':False}):
            results.append(doc)
        return results
    
    async def delete_order_close(self) -> int:
        return self.collection.delete_many(filter={"Статус":"Закрыт"},projection={'_id':False})
  
    
class Basket(Base):
    def __init__(self):
        super().__init__("basket")
    

    async def read(self,data)->dict:
        return self.collection.find_one(filter={"id":data},projection={"id":0, "_id":0})
        
    async def drop(self,data)->dict:
        return self.collection.find_one_and_delete(filter={"id":data},projection={"_id":0})
    
    async def add(self,data:dict):
        a=self.collection.find_one_and_delete(filter={"id":data.get("id")})
        if a is not None:
            data.update(a)
        self.collection.replace_one(filter={"id":data.get("id")},replacement=data,upsert=True)