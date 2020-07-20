# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

def login_required(func):
    def new_func(request, *args, **kwargs):
        user_id = request.session.get("session_username")
        if not user_id:
            return HttpResponseRedirect("/login")
        res=func(request, *args, **kwargs)
        return res
    return new_func

def login(request):
    result = {}
    if request.POST:
        username=request.POST.get("username")
        password=request.POST.get("password")
        redirect_to = "/welcome"
        if username == "root" and password == "123456":
            request.session['session_username'] = username
            request.session.set_expiry(3600*6)
            return HttpResponseRedirect(redirect_to)
        elif username == "liuhuayong" and password == "123456":
            request.session['session_username'] = username
            request.session.set_expiry(3600*6)
            return HttpResponseRedirect(redirect_to)
        else:
            result['message'] = u'用户名或密码错误'
    print request.COOKIES
    return render(request, 'login.html', result)

@login_required
def welcome(request):
    if request.user.is_authenticated():
        print 'ddddddddd'
    else:
        print 'ttttttttttt'

    print request.user.username
    result = {"username":request.session.get('session_username')}
    response = render(request, 'welcome.html', result)
    response.set_cookie("color", "red")
    print request.COOKIES
    return response


def logout(request):
    request.session["session_username"] = ""
    result = {"username":request.session.get('session_username')}
    return render(request, 'login.html', result)

@login_required
def wel(request):
    if request.user.is_authenticated():
        print 'ddddddddd'
    else:
        print 'ttttttttttt'

    print request.user.username
    result = {"session_username":request.session["session_username"]}
    return render(request, 'wel.html', result)