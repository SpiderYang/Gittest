import urllib2
import urlparse
import hashlib

def md5(input_str):
    m = hashlib.md5()
    m.update(input_str)
    return m.hexdigest()

def make_request(url,refer=None):
    all = urlparse.urlparse(url)
    hdr = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'Host': all.netloc,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.45 Safari/537.36'
    }
    if refer:
        hdr['Referer'] = refer
    return urllib2.Request(url,headers=hdr)

def get_url_length(url,retry_times=1,refer=None):
    for i in range(0,retry_times):
        try:
            return get_source_size(url,refer)
        except:
            print "Get source Size fail."
    raise Exception("Get source Size fail.")

def get_source_size(url,refer=None):
    req = make_request(url,refer)
    try:
        res = urllib2.urlopen(req)
        size = res.info().getheader('Content-Length')
    except:
        print "cat't get the source size"
    if size:
        return int(size)

def readable_size(size):
    if size < 1000:
        return '%d b',size
    kb = size /1024.0
    if kb < 1000:
        return '%.3f kb',kb
    mb = kb / 1024.0
    if mb < 1000:
        return '%.3f mb',mb
    gb = mb /1024.0
    if gb < 1000:
        return '%.3f gb',gb

def download_chunk(url,start,end,retry_times=1,refer=None):
    for i in range(0,retry_times):
        try:
            return download(urlm,start,end,refer=None)
        except:
            print "download Error from %s-%s" % (start,end)
    raise Exception("download Error from %s-%s" % (start,end))

def download(url,start,end,refer=None):
    req = make_request(url,refer)
    req.headers['Range'] = 'byte=%s-%s' % (start,end)
    try:
        res = urllib2.urlopen(req)
    except:
        print 'download Error'
    return res.read()
