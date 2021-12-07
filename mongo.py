import pymongo

# client = pymongo.MongoClient('3.1.114.42', 10002)
client_local = pymongo.MongoClient('mongodb://localhost:27017/')
db_local = client_local["local"]
# db = client["hinh"]
# db.authenticate("ecb", "ecb")

# # 資料查找
def find_data():
    query = {"country":"spain"}
    data = db_local.fun.find(query) #fun是table name
    for i in data:
        print(i)

# # 刪除資料
def delete_data():
    query = {"continent": "asia"}
    db_local.fun.delete_one(query)

# # 新增資料
def insert_data():
    d = [{"country":"canada", "population":4000000, "continent":"northamerica"}, {"country":"korea",
                                                                                 "population":1000000,
                                                                         "continent":"asia"}]
    for i in d:
        result = db_local.fun.insert_one(i)
        print(result)

# # 修改資料
def update_data():
    query = {"country":"korea"}
    new_values = {"$set":{"population":"3800000"}}
    # db_local.fun.update_one(query, new_values)  # 單筆
    db_local.fun.update(query, new_values, multi=True)  # 多筆



if __name__ == '__main__':
    # insert_data()
    # delete_data()
    # find_data()
    update_data()