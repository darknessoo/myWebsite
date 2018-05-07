#!/usr/bin/env python
# encoding=utf-8

import json
from time import sleep
from pymongo import MongoClient
from xtls.basecrawler import BaseCrawler
from xtls.codehelper import no_exception, timeit
from xtls.logger import get_logger
from xtls.util import BeautifulSoup

from util import *

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'xlzd'
logger = get_logger(__file__)
MONGO = MongoClient(MONGO_HOST, MONGO_PORT)


class ZhihuRelaCrawler(BaseCrawler):
    def __init__(self, data):
        super(ZhihuRelaCrawler, self).__init__(data=data)
        self._request.headers['Cookie'] = ZHIHU_COOKIE

    @no_exception([])
    def _find_following(self, offset):
        data = {
            'method': 'next',
            'params': '{"offset":%s,"order_by":"created","hash_id":"%s"}' % (offset, self.data['_id']),
            '_xsrf': '在登录之后的网页上复制出这个值',
        }
        html = self.post('http://www.zhihu.com/node/ProfileFolloweesListV2', data=data)
        data = json.loads(html)
        rst = []
        for item in data['msg']:
            soup = BeautifulSoup(item)
            a = soup.find('a')
            rst.append({
                'selfuid': a.get('href', '')[8:],
                '_id': soup.find('button')['data-id'],
                'nickname': a.get('title', '')
            })
        return rst

    def find_following(self):
        offset = 0
        while True: 
            rst = self._find_following(offset)
            for item in rst:
                yield item
            if len(rst) < 20:
                break
            offset += 20

    @no_exception(500)
    def run(self):
        del self.data['done']
        me = push_user_node(self.data)

        for item in self.find_following():
            current_user = push_user_node(item)
            create_relationship(me, current_user)

            if MONGO[MONGO_DB][MONGO_USER_COLL].find_one({'_id': item['_id']}):
                continue
            item['done'] = False
            MONGO[MONGO_DB][MONGO_USER_COLL].insert_one(item)
        return 200


@timeit
def task():
    now_item = MONGO[MONGO_DB][MONGO_USER_COLL].find_one({'done': False})
    logger.info('now : %s' % now_item['selfuid'])
    status = ZhihuRelaCrawler(now_item).run()
    if status == 200:
        now_item['done'] = True
    else:
        now_item['done'] = 'ERROR'
    MONGO[MONGO_DB][MONGO_USER_COLL].update_one(
        filter={'_id': now_item['_id']},
        update={'$set': now_item},
        upsert=False
    )


if __name__ == '__main__':
    while True:
        task()

