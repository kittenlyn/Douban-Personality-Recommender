
import os
import time

NO_DIR = True
# NO_DIR = False

TIME = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
BASE_DIR = os.path.dirname(__file__)

SAVE_PATH = os.path.join(BASE_DIR, TIME).replace('\\', '/')
if not os.path.exists(SAVE_PATH) and NO_DIR is False:
    os.makedirs(SAVE_PATH)


# HEADER = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
HEADER = {
          'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:37.0) Gecko/20100101 Firefox/37.0',
          'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
          'Accept-Encoding':'gzip, deflate',
          }


GROUP_MEMBER_URL = u'http://www.douban.com/group/20031/members?start={}'
LOGIN_POST_URL = u'https://accounts.douban.com/login'
LOGIN_URL = u'https://www.douban.com/accounts/login'
MEMBER_PAGE = u'http://www.douban.com/people/{}/'

BOOK_URL = (
            u'http://book.douban.com/people/{}/do',
            u'http://book.douban.com/people/{}/wish',
            u'http://book.douban.com/people/{}/collect',
           )

USERNAME = u''
PASSWORD = u''

HOST = u'http://www.douban.com/'

