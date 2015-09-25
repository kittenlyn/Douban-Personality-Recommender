

import urllib
import urllib2
import cookielib
import time
import StringIO
import gzip
import sys
import re
import time
import os
import zlib
import random
import urlparse
import setting
import json


_spec_char = [u'\\', u'/', u'*', u'|', u'<', u'>', u'?', u':', u'"']


def run(start=0, end=0, cookie=None, cookie_str=''):
    '''
      1. creat file
      2. get group member list
      3. goto member's home page
      4. get every member's book info, and save it to file
    '''
    fn = open('book.txt', 'w+')
    index = 1
    for i in get_group_member(start=start, end=end, cookie=cookie, cookie_str=cookie_str):
        if i is None:
            break
        print u'user:'
        # print i
        for j in i:
            try:
                print u'用户{}:'.format(str(index)), j[1]
            except:
                print ''
                pass
            finally:
                book_info = get_book_info(j[0], cookie)
                # print 'book_info'
                # print book_info
                info_to_write = (j[1] + u';').encode('utf-8')
                for k in book_info:
                    info_to_write += (u','.encode('utf-8')).join(k) + u';'.encode('utf-8')
                # fn.write(info_to_write.encode('gbk'))
                fn.write(info_to_write)
                fn.write('\n')
                index += 1
    fn.close()
    print u'完成'

def get_book_info(id, cookie):
    '''
      get user's book info
    '''
    # fn = open('test.txt', 'w+')
    book_info = []
    header = setting.HEADER
    header['Referer'] = setting.MEMBER_PAGE.format(id)
    for i in setting.BOOK_URL:      # three type: doing, wish and collect
        url = i.format(id)
        # print url
        retry_times = 0
        while True:
            page = ''
            page, cookie = get_page(url_in=url, header_in=header, data=None, cookie_set=cookie)
            retry_times += 1
            if page == '':
                if retry_times > 5:
                    book_info.append([])
                    break
                else:
                    time.sleep(1.1)
                    continue
            break
        # fn.write(page)
        # fn.write('\n\n\n\n\n')
        # page = page.decode('utf-8')
        book_info.append(book_info_extractor(page))
    # fn.close()
    return book_info

def book_info_extractor(page):
    pat = re.compile(u'(?<=\<ul class="interest-list"\>).+?(?=\</ul\>)', re.DOTALL)
    res = pat.findall(page)
    if len(res) == 0:
        return ['']

    pat = re.compile(u'(?<=\<li class="subject-item"\>).+?(?=\</li\>)', re.DOTALL)
    res = pat.findall(res[0])
    if len(res) == 0:
        return ['']

    titles = []
    for i in res:
        pat = re.compile(u'(?<=title=").+?(?=")', re.DOTALL)
        title = pat.findall(i)
        if len(title) > 0:
            titles.append(title[0])
            # print title[0]

    return titles

def get_group_member(url=setting.GROUP_MEMBER_URL, start=0, end=0, cookie=None, cookie_str=''):
    '''
      get group member from specific group
      start and end constrain member range
    '''
    group_url = ''
    start_member = start
    header = setting.HEADER
    while True:
        group_url = url.format(str(start_member))
        print 'group_url:', group_url
        cookie_str['bid'] = random_bid()
        header['Cookie'] = urllib.urlencode(cookie_str)
        page, cookie = get_page(url_in=group_url, header_in=setting.HEADER, data=None, cookie_set=cookie)
        page = page.decode('utf-8')
        with open('11.txt', 'w+') as f:
            f.write(page.encode('utf-8'))

        member_list = member_info_extractor(page)
        if member_list == False:
            break

        yield member_list
        if end > 0:
            if start_member > end or start_member == end:
                break
        start_member += 35
    yield None

def member_info_extractor(page):
    '''
      extract user's id and name from given page
    '''
    pat = re.compile(u'(?<=\<div class="member-list"\>).+?(?=\</ul\>)', re.DOTALL)
    res = pat.findall(page)
    if len(res) == 0:
        return False

    res = res[-1]
    pat = re.compile(u'(?<=\<div class="name"\>).+?(?=\</div\>)', re.DOTALL)
    res = pat.findall(res)
    member_list = []
    for i in res:
        pat = re.compile(u'(?<=\<a href=").+?(?=")', re.DOTALL)
        url = pat.findall(i)[0]

        pat = re.compile(u'(?<=\>).+?(?=\</a\>)', re.DOTALL)
        name = pat.findall(i)[0]

        index = url[-2::-1].index('/')
        index = len(url)-index-1
        id = url[index:-1]
        member_list.append([id, name])
        # print url, name, id
    return member_list


def login():
    '''
      登陆豆瓣
    '''
    post_data = {}
    header = setting.HEADER
    page, cookie = get_page(url_in = setting.LOGIN_URL, header_in=header)
    if page == '':
        print u'超时，请重新执行程序'
        return
        
    with open('11.txt', 'w+') as f:
        f.write(page)
        
    page = page.decode('utf-8')
    pat = re.compile(u'(?<=\<form).+?(?=\</form\>)', re.DOTALL)
    form = pat.findall(page)[0]
    with open('sdsd.txt', 'w+') as f:
        f.write(form.encode('gbk'))
    pat = re.compile(u'(?<=\<input).+?(?=\>)', re.DOTALL)
    res = pat.findall(form)
    for i in res:
        if 'captcha-solution' in i:
            pat = re.compile(u'(?<=src=").+?(?=")')
            src = pat.findall(form)[-1].replace('&amp;', '&')
            header['Referer'] = setting.LOGIN_URL
            page, cookie = get_page(url_in = src, header_in=header, cookie_set=cookie)
            with open('code.jpg', 'wb+') as f:
                f.write(page)
            print u'请输入code.jpg中的验证码:',
            code = raw_input()
            post_data['captcha-solution'] = code

        else:
            pat = re.compile(u'(?<=name=").+?(?=")')
            name = pat.findall(i)[0]
            pat = re.compile(u'(?<=value=").+?(?=")')
            value = pat.findall(i)
            if name == 'form_email' or name == 'form_password' or len(value) == 0:
                continue
            # print name, value[0]
            post_data[name] = value[0]

    # post_data = {}
    # post_data['source'] = 'None'
    # post_data['redir'] = 'https://www.douban.com'
    post_data['login'] = post_data['login'].encode('utf-8')
    post_data['form_email'] = setting.USERNAME
    post_data['form_password'] = setting.PASSWORD
    # print post_data
    post_data = urllib.urlencode(post_data)
    # post_data += '&login=%E7%99%BB%E5%BD%95'
    # print post_data

    header['Referer'] = setting.LOGIN_URL
    header['Content-Type'] = 'application/x-www-form-urlencoded'
    page, cookie = get_page(url_in = setting.LOGIN_POST_URL, header_in=header, data=post_data)
    if len(cookie) > 0:
        print u'登陆成功!'
        for i in cookie:
            print i.name, ':', i.value
        return cookie
    else:
        print u'登陆失败!'
        return False


def get_page(url_in=None, header_in=None, data=None, cookie_set=None):
    '''
      通用方法，请求页面
    '''
    url = url_in
    header = header_in
    header['Host'] = urlparse.urlparse(url).netloc


    opener = urllib2.OpenerDirector()
    http_handler = urllib2.HTTPHandler()
    https_handler = urllib2.HTTPSHandler()

    if cookie_set == None:
        cookie = cookielib.CookieJar()
    else:
        cookie = cookie_set

    cookie_handle = urllib2.HTTPCookieProcessor(cookie)
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    if cookie_set != False:
        opener.add_handler(cookie_handle)
    else:
        header['Cookie'] = 'bid=' + random_bid() + ';'
        pass

    req = urllib2.Request(url)
    for (name, val) in header.items():
        req.add_header(name, val)

    if data is not None:
        req.add_data(data)
        req.add_header(u'Content-Length', len(data))

    try:
        r = ''
        r = opener.open(req, timeout = 45)
        # Make sure everything is working ;
        # print r.info().get('Location')
        if r.info().get('Transfer-Encoding') == 'chunked':
            d = zlib.decompressobj(16+zlib.MAX_WBITS)
            content = ''
            while True:
                data = r.read()
                if not data:
                  break
                content += d.decompress(data)
            data = content
        else:
            if r.info().get('Content-Encoding') == 'gzip':
                buf = StringIO.StringIO(r.read())
                f = gzip.GzipFile(fileobj=buf)
                data = f.read()
            else:
                data = r.read()
    except KeyboardInterrupt:
        print 'EXIT: Keyboard Interrupt'
        sys.exit(0)
    except:
        data = ''
        # print 'Time Out'
    finally:
        if r != '':
            r.close()
        opener.close()

    return [data, cookie]

def random_bid():
    char_for_sel = [str(i) for i in range(0, 10)]
    char_for_sel += [chr(i) for i in range(97,123)]
    char_for_sel += [chr(i).upper() for i in range(97,123)]
    return ''.join([random.choice(char_for_sel) for i in range(0, 11)])
    print char_for_sel

if __name__ == "__main__":
    # a = ''
    # with open('page.txt', 'r') as f:
        # a = f.read()
    # a = a.decode('utf-8')
    # book_info_extractor(a)
    # member_info_extractor(a)
    # print get_book_info('45937907', None)
    # random_bid()
    # sys.exit(0)
    # cookie = login()
    cookie_str = {}
    # for i in cookie:
        # cookie_str[i.name] = i.value
    run(35*0, 35*260, False, cookie_str)
    # for i in url:
        # news_info = get_item_news(i, header)
        # print '--------------------------------------------------------------------'
    # for i in news_info:
        # print i[0], i[1]


