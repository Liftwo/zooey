import pymysql.cursors
import pymongo
import transfer_uuid

'''Mongo'''
client_formal = pymongo.MongoClient('3.1.114.42', 10002)
client_test = pymongo.MongoClient('18.141.69.164', 10002)  # 路徑連接
db = client_formal["hinh"]  # 資料庫連接
table = db.drflog_podcastchannel  # 資料表連接

'''MySQL'''
# connection = pymysql.connect(host='18.141.69.164', port=10000, user='root', password='nicc1314', db='hinh')
connection = pymysql.connect(host='3.1.114.42', port=10000, user='root', password='easycatchball168', db='hinh')

cursor = connection.cursor()
query = "SELECT * FROM hinh.drfuser_user"
query_khands = "SELECT * FROM hinh.drfcreator_khandsstar"
cursor.execute(query)
result = cursor.fetchall()
cursor.execute(query_khands)
result_khands = cursor.fetchall()

'''drfuser查詢'''
pod = []
for i in table.find():
    for j in result:
        # uuid = j[30][0:8]+'-'+j[30][8:12]+'-'+j[30][12:16]+'-'+j[30][16:20]+'-'+j[30][20::]
        uuid = transfer_uuid.mongo_aid(str(j[0]))  # j[0]是mysql的uuid
        if i['aid'] == uuid:
            update = f"UPDATE `hinh`.`drfuser_user` SET `isPc_bind` = 1  WHERE (`uuid` = '{j[0]}');"
            pod.append(i['aid'])
            try:
                cursor.execute(update)
                connection.commit()
            except:
                print('無法更新資料庫', i)
                continue
print(len(pod), pod)
connection.close()

'''Khandsstar查詢'''
# user_id = []
# for i in result:
#     for j in result_khands:
#         print(j[1])
#         if i[0] == j[1]:
#             user_id.append(j[1])
# print(len(user_id), user_id)
# connection.close()

mongo_aid=[]
mysql_uuid = []
b = []
for i in table.find():
    mongo_aid.append(i['aid'])
for j in result:
    if j[43]==1:
        uuid = transfer_uuid.mongo_aid(str(j[0]))
        mysql_uuid.append(uuid)

for i in mysql_uuid:
    if i in mongo_aid:
        b.append(i)
print(len(b))

connection.close()