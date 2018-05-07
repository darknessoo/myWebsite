#!/usr/bin/env python
# encoding=utf-8

import sys

from py2neo import *

from config import *

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'xlzd'

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DB = 'zhihu'
MONGO_USER_COLL = 'zhrelauser'

NEO4J_ADDRESS = 'http://neo4j:xlzd@127.0.0.1:7474/db/data/'
NODE_NAME = 'zhUser'

ZHIHU_COOKIE = ''

GRAPH = Graph(NEO4J_ADDRESS)
CYPHER_FIND_USER = "MATCH (user:" + NODE_NAME + " {%s:'%s'}) RETURN user LIMIT 1"
CYPHER_FIND_RELA = "MATCH (a:{node})-[:FOLLOWING]->(b:{node}) WHERE a._id = '%s' AND b._id = '%s' RETURN a, b".format(node=NODE_NAME)
CYPHER_MIN_PATHS = "MATCH (a:{node} {{ _id:'%s' }}),(b:{node} {{ _id:'%s' }}), p = allShortestPaths((a)-[*..%s]->(b)) RETURN p".format(node=NODE_NAME)


def find_user_by_uid(uid, tp='_id'):
    cypher = CYPHER_FIND_USER % (tp, uid)
    for user in GRAPH.cypher.execute(cypher):
        return user['user']
    return False


def push_user_node(param):
    user = find_user_by_uid(param['_id'])
    if user:
        if user['selfuid'] == param['selfuid'] and user['nickname'] == param['nickname']:
            return user
        new = False
    else:
        user = Node(NODE_NAME)
        new = True
    user.properties['_id'] = param['_id']
    user.properties['selfuid'] = param['selfuid']
    user.properties['nickname'] = param['nickname']
    if new:
        GRAPH.create(user)
    user.push()
    return user


def create_relationship(user1, user2):
    cypher = CYPHER_FIND_RELA % (user1['_id'], user2['_id'])
    if len(GRAPH.cypher.execute(cypher)):
        return
    rela = Relationship(user1, 'FOLLOWING', user2)
    GRAPH.create(rela)


def find_relationship(user1, user2, max=6):
    cypher = CYPHER_MIN_PATHS % (user1['_id'], user2['_id'], max)
    p = GRAPH.cypher.execute(cypher)
    for record in p:
        print record.p

