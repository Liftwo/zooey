mysql_uuid = input()
mongo_uuid = mysql_uuid[0:8]+'-'+mysql_uuid[8:12]+'-'+mysql_uuid[12:16]+'-'+mysql_uuid[16:20]+'-'+mysql_uuid[20::]
print(mongo_uuid)


def mongo_aid(mysql_uuid):
    mongo_uuid = mysql_uuid[0:8] + '-' + mysql_uuid[8:12] + '-' + mysql_uuid[12:16] + '-' + mysql_uuid[16:20] + '-' + mysql_uuid[20::]
    return mongo_uuid

def test(a, b):
    return a+b