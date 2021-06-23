from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import User, KP, Battledetail
from django.core.files.storage import default_storage
from .pokegetmatch_module import getpoke
from django.template import loader
from PIL import Image
import numpy, urllib, csv
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
# from django.urls import reverse


from mysite.settings import BASE_DIR

import random, string

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

with open('/home/wagou/djangoconf/twitkeys.txt') as f:
    consumer_key = f.readline().strip()
    consumer_secret = f.readline().strip()

# Create your views here.
def view(request):
    skps = KP.objects.all().order_by('-count').filter(count__gt=0)
    dkps = KP.objects.all().order_by('-count2').filter(count2__gt=0)
    sbattle = Battledetail.objects.all().filter(battletype='single').filter(memory='yes').count()
    dbattle = Battledetail.objects.all().filter(battletype='double').filter(memory='yes').count()
    battle = sbattle + dbattle
    context = {
        'skps': skps,
        'dkps': dkps,
        'battle': battle,
        'sbattle': sbattle,
        'dbattle': dbattle,
    }
    template = loader.get_template('upload/view.html')
    return HttpResponse(template.render(context, request))

def user(request):
    user_id_str = request.GET.get('user_id')
    if user_id_str == None:
        return HttpResponse("AuthError")
    # 登録済みの場合オブジェクト参照
    if User.objects.filter(key=user_id_str).exists():
        user = User.objects.get(key=user_id_str)
    # 未登録の場合エラーを返す
    else:
        return HttpResponse("LoginError")
    # ユーザの対戦数
    userbattle = Battledetail.objects.filter(key=user.key).count()
    # ユーザの対戦データ
    details = Battledetail.objects.filter(key=user.key).order_by('-date')
    context = {
        'user': user,
        'userbattle': userbattle,
        'details' : details,
    }
    template = loader.get_template('upload/user.html')
    return HttpResponse(template.render(context, request))

@require_POST
@csrf_exempt
def upload(request,mode):
    """/upload で呼び出される。"""
    # POSTを受けた時
    if request.method == 'POST':
        importkey = request.FILES['key'].read()
        importkey = importkey.decode()
        print(importkey)
        # key認証
        if User.objects.filter(key=importkey).exists():
            try:
                img_moto = Image.open(request.FILES['image'])
                # img_moto = Image.open(BASE_DIR+"/apps/upload/"+"test3.png")
                # img = numpy.asarray(numpy.array(img_moto))
                img = numpy.asarray(img_moto)
                line = getpoke(img,importkey,mode)
                return HttpResponse(line)
            except Exception as e:
                return HttpResponse("Error")
        # 認証失敗
        else:
            return HttpResponse("Incorrect key")
    else:
        return HttpResponse("Not Uploaded")

@require_POST
def csvdownload(request):
    key = request.POST.get("key", None)
    print(key)
    if (key == None):
        return HttpResponse("KeyError")
    response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    filename = urllib.parse.quote((u'battledata.csv').encode("utf8"))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)
    writer = csv.writer(response)
    header = ['Date', '#1', '#2', '#3', '#4', '#5', '#6', 'My#1', 'My#2', 'My#3', 'My#4', 'My#5', 'My#6', 'Type', 'Issent']
    writer.writerow(header)
    for battledetail in Battledetail.objects.filter(key=key):
        writer.writerow([battledetail.date, battledetail.poke1, battledetail.poke2, battledetail.poke3, battledetail.poke4, battledetail.poke5, battledetail.poke6, battledetail.mypoke1, battledetail.mypoke2, battledetail.mypoke3, battledetail.mypoke4, battledetail.mypoke5, battledetail.mypoke6,battledetail.battletype,battledetail.memory])
    return response

def agreement(request):
    return render(request, 'upload/agreement.html',{})

def howto(request):
    return render(request, 'upload/howto.html',{})

def logintw(request):
    oauth_callback = "https://app.roishi.com/pokeapp/back"
    twitter = OAuth1Session(consumer_key, consumer_secret)
    response = twitter.post(
        'https://api.twitter.com/oauth/request_token',
        params={'oauth_callback': oauth_callback}
    )
    request_token = dict(parse_qsl(response.content.decode("utf-8")))
    authenticate_url = "https://api.twitter.com/oauth/authenticate"
    authenticate_endpoint = '%s?oauth_token=%s' \
        % (authenticate_url, request_token['oauth_token'])

    return redirect(authenticate_endpoint)

def back(request):
    oauth_token = request.GET.get("oauth_token", None)
    oauth_verifier = request.GET.get("oauth_verifier", None)
    if oauth_token == None or oauth_verifier == None:
        return HttpResponse("Login Error")
    twitter = OAuth1Session(
        consumer_key,
        consumer_secret,
        oauth_token,
        oauth_verifier,
    )
    response = twitter.post(
        'https://api.twitter.com/oauth/access_token',
        params={'oauth_verifier': oauth_verifier}
    )
    access_token = dict(parse_qsl(response.content.decode("utf-8")))
    # 新規登録の場合オブジェクト参照
    if User.objects.filter(twid=str(access_token['user_id'])).exists():
        user = User.objects.get(twid=str(access_token['user_id']))
    # 新規登録の場合オブジェクト作成
    else:
        user = User(twid=str(access_token['user_id']),key=randomname(20))
        user.save()
    return redirect('https://app.roishi.com/pokeapp/user?user_id='+user.key)
