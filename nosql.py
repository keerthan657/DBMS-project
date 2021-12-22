# install command - pip install elasicsearch
from elasticsearch import Elasticsearch

# set elasticsearch host
config = {'host': '127.0.0.1'}
es = Elasticsearch([config,], timeout=300)

# index a document - CREATE
# input params -> myIndex=>index name(string), myID=>document ID(int),
# 				  myBody=>document body(json)
# output params -> json result
def create_entry(myIndex, myId, myBody):
	return(es.index(index=myIndex, id=myId, body=myBody))

# read a document - READ
# input params -> myIndex=>index name(string), myID=>document ID(int)
# output params -> json result
def read_entry(myIndex, myId):
	return(es.get(index=myIndex, id=myId))

# update a document - UPDATE -> same as CREATE
# input params -> myIndex=>index name(string), myID=>document ID(int),
# 				  myBody=>document body(json)
# output params -> json result
def update_entry(myIndex, myId, myBody):
	return(es.index(index=myIndex, id=myId, body=myBody))

# delete a document - DELETE
# input params -> myIndex=>index name(string), myID=>document ID(int)
# output params -> json result
def delete_entry(myIndex, myId):
	return(es.delete(index=myIndex, id=myId))

# create a new index
# input params -> myIndex=>index name(string)
# output params -> json result
def create_new_index(myIndex):
	return(es.indices.create(index=myIndex))

# delete entire index
# input params -> myIndex=>index name(string)
# output params -> json result
def delete_entire_index(myIndex):
	return(es.indices.delete(index=myIndex))
	# original 
	# es.indices.delete(index='favourite_candy', ignore=[400,404])


# Database Initialization - fine_rate
# print("Initializing Elasticsearch database")
# print(create_new_index('traffic_db2_v1_fines'))
# print(create_entry('traffic_db2_v1_fines', 1, {
# 		'fine_type': 'insurance_expiry',
# 		'fine_amt': 320
# 		}))
# print(create_entry('traffic_db2_v1_fines', 2, {
# 		'fine_type': 'registration_expiry',
# 		'fine_amt': 235
# 		}))
# print(create_entry('traffic_db2_v1_fines', 3, {
# 		'fine_type': 'emissions_expiry',
# 		'fine_amt': 310
# 		}))
# print(create_entry('traffic_db2_v1_fines', 4, {
# 		'fine_type': 'no_helmet',
# 		'fine_amt': 500
# 		}))
print(read_entry('traffic_db2_v1_fines', 1))

# Database Initialization - user_auth
# print("Initializing Elasticsearch database")
# print(create_new_index('user_auth'))
# print(create_entry('user_auth', 1, {
# 		'username': 'keerthan',
# 		'password': '123456',
# 		'type': 'public'
# 		}))
# print(create_entry('user_auth', 2, {
# 		'username': 'admin',
# 		'password': 'password',
# 		'type': 'transport_dept'
# 		}))
# print(read_entry('user_auth', 1))
# print(read_entry('user_auth', 2))

def get_amt(fine_type_id):
	res = read_entry('traffic_db2_v1_fines', fine_type_id)
	return res['_source']['fine_amt']

def auth_user(username, password, type_):
	res1 = read_entry('user_auth', 1)
	res2 = read_entry('user_auth', 2)
	u,p,t = res1['_source']['username'], res1['_source']['password'], res1['_source']['type']
	if(username==u and password==p and type_==t):
		return True
	u,p,t = res2['_source']['username'], res2['_source']['password'], res2['_source']['type']
	if(username==u and password==p and type_==t):
		return True
	# else default
	return False