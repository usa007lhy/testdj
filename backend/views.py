# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
import logging
import os
import time

#logger = logging.getLogger(__name__)
logger1 = logging.getLogger('views1')
logger2 = logging.getLogger('views2')

def required_login(func):
    def fun1(request,*args, **kwargs):
        start = time.time()
        res = func(request, *args, **kwargs)
        stop = time.time()
        logger1.info('required_login')
        return res
    return fun1

@required_login
def index(request):
    logger1.info('logger_index1')
    result = {'title':u'首页','content':'Hello World11'}
    #time.sleep(60)
    print request.GET
    #return HttpResponse('Hello World')
    return render_to_response('index.html',result)

