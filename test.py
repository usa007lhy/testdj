#-*- coding:utf-8 -*-
import datetime
import random
import traceback

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.httputil
import config
import time

class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		try:
			import time
			import hashlib

			timestamp = int(time.time())
			keyStr = '/api/report/dailyShare?ak=test_ak&date=2019-09-01&sk=kuaishou_test_sk&timestamp=%s' % (timestamp)
			sign = hashlib.sha1(keyStr).hexdigest()
			url = 'http://ssp1-debug.test.gifshow.com/api/report/dailyShare?timestamp=%s&ak=test_ak&date=2019-09-01&sign=%s' % (timestamp, sign)
			http_client = tornado.httpclient.AsyncHTTPClient()
			http_client.fetch(tornado.httpclient.HTTPRequest(url.encode('utf8', 'ignore'), connect_timeout=0.2, request_timeout=0.4),callback=self.on_complete, request_timeout=0.5)
		except Exception, e:
			print e
			self.write("程序执行异常")
			self.finish()

	def on_complete(self, response):
		try:
			print response
			# self.write(content)
			# self.finish()
		except Exception, e:
			print e
			self.write('complete执行异常')
			self.finish()

def signature_gen(secure_key, timestamp, nonce):
	'''生成秘钥，请求头条接口获取收入数据时候使用'''
	keys = [secure_key, str(timestamp), nonce]
	keys.sort()
	keyStr = ''.join(keys)
	import hashlib
	signature = hashlib.sha1(keyStr).hexdigest()
	return signature

class AdIncomeHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		import json
		self.set_header('Content-Type', 'application/x-javascript')
		result_dict={'code':config.income_toutiao_request_exception,'message':u'程序发生异常'}
		result = json.dumps(result_dict)
		try:
			yesterday = (datetime.date.today()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
			twodayago = (datetime.date.today()+datetime.timedelta(days=-2)).strftime("%Y-%m-%d")
			start_date = self.get_argument('start_date', twodayago)
			end_date = self.get_argument('end_date', yesterday)
			app2adslot = self.get_argument('app2adslot','')
			app2adslot_dict = json.loads(app2adslot)
			user_id = config.income_toutiao_user_id
			timestamp = int(time.time())
			nonce = '58%s%s'%(timestamp, random.randint(1000,10000))
			sign = signature_gen(config.income_toutiao_secure_key, timestamp, nonce)
			url = u'http://partner.oceanengine.com/union/media/open/api/report/slot?user_id=%(user_id)s&sign=%(sign)s&nonce=%(nonce)s&timestamp=%(timestamp)s&start_date=%(start_date)s&end_date=%(end_date)s' % locals()
			print url
			http_client = tornado.httpclient.AsyncHTTPClient()
			http_client.fetch(tornado.httpclient.HTTPRequest(url.encode('utf8', 'ignore'), connect_timeout=2, request_timeout=4),callback=self.on_complete, request_timeout=5)

			# response = urllib2.urlopen(url)
			# res = response.read()
			# res_dict = json.loads(res)
			# if res_dict['code'] != config.income_toutiao_request_success:
			# 	self.write(res)
			# 	self.finish()
			# data_list = []
			# for data_one in res_dict['data']:
			# 	ad_slot_id = str(data_one["ad_slot_id"])
			# 	appid = str(data_one["appid"])
			# 	if appid in app2adslot_dict.keys() and ad_slot_id in app2adslot_dict[appid]:
			# 		data_list.append(data_one)
			# if not data_list:
			# 	res_dict['code'] = config.income_toutiao_request_no_suitable
			# 	res_dict['message'] = u'没有符合appid和ad_slot_id的数据'
			# res_dict['data'] = data_list
			# result = json.dumps(res_dict)
			# print result
		except Exception, e:
			traceback.print_exc()
			self.write(result)
			self.finish()



	def on_complete(self, response):
		self.set_header('Content-Type', 'application/x-javascript')
		try:
			if not response:
				print u'返回为空'
				self.write('null')
			elif  response.error:
				print response.error
				self.write(response.error)
			else:
				print 'success'
				print response.body
				self.write(response.body)
		except Exception,e:
			print e
			self.write(u'complete执行异常')
		self.finish()


application = tornado.web.Application([
	(r"/test", MainHandler),
	(r"/", AdIncomeHandler),
])

def start(port):
	port = int(port)
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(port)
	print 'server start on port %s...'%port
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    start(8000)
