import time
import hashlib
import urllib2
import json
timestamp = int(time.time())
keyStr = '/api/report/dailyShare?ak=test_ak&date=2020-01-01&sk=kuaishou_test_sk&timestamp=%s'%(timestamp)
sign = hashlib.md5(keyStr).hexdigest()
#sign = hashlib.sha1(keyStr).hexdigest()
url = 'https://ssp-debug.test.gifshow.com/api/report/dailyShare?timestamp=%s&ak=test_ak&date=2020-01-01&sign=%s' % (timestamp, sign)
response = urllib2.urlopen(url)
res = response.read()
res_dict = json.loads(res)
print 'url=>',url
print 'result=>',res_dict['result']
print 'error_msg=>',res_dict['error_msg']
print 'Hello World'
