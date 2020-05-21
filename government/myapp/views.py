from django.shortcuts import render
from django.http import JsonResponse
from .models import Cateory, Content, GetNum, Wage, UserIC
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.utils.six import BytesIO
import json
import time
import os
import psutil
# import face_recognition
import hashlib
from PIL import Image, ImageDraw
import base64


# Create your views here.


# /apis/get_info
def get_info(request):
    """
    用于提供数据
    :param request: HttpRequest
    :return: Json
    """

    if request.method == "GET":
        # 如果是要获取分类列表则加上这个参数  需要提供的内容为: 1ds2ppJu2I9dl1
        user_id = request.GET.get("user_id")
        cateory_list = request.GET.get("cateory")
        user_list = request.GET.get("users")
        get_page_arr = request.GET.get("page")
        get_access_num = request.GET.get("num")
        get_blog_list = request.GET.get("blog_list")
        get_mp3 = request.GET.get("mp3")
        get_status = request.GET.get("status")
        get_wage = request.GET.get("wage")
        get_date = request.GET.get("date")
        get_user_detail = request.GET.get("user_detail")
        get_username = request.GET.get("username")



        # 页码
        if get_page_arr is not None:
            get_page = int(get_page_arr)
        else:
            get_page = 1
        pagesize = 5
        start = (get_page - 1) * pagesize
        end = get_page * pagesize

        # 获取分类列表
        if cateory_list is not None and cateory_list == "1ds2ppJu2I9dl1":
            return JsonResponse({
                "status_code": 0,
                "data": [i[0] for i in list(Cateory.objects.values_list("cateory_name"))]
            })

        if user_list is not None and user_list == "2ds2ppJu2I9dl1":
            return JsonResponse({
                "status_code": 0,
                "data": [i[0] for i in list(User.objects.values_list("username"))]
            })

        if get_access_num is not None and get_access_num == "true":
            db = GetNum.objects.get(date=time.strftime("%Y-%m-%d"))
            return JsonResponse({
                "status_code": 0,
                "num": int(db.number)
            })

        # 获取公告列表
        if get_blog_list is not None and get_blog_list == "true":
            db = Content.objects.all()
            data = [
                {
                    "title": i.title,
                    "content": i.content,
                    "cateory": i.cateory.cateory_name,
                    "user": i.user.username,
                    "time": i.time
                }
                for i in db[start:end]]

            return JsonResponse({
                "status_code": 0,
                "total": len(db),
                "data": data
            })

        # 查询工资
        if get_wage is not None and get_wage == "true" and user_id is not None:
            user_ic = UserIC.objects.get(user_id=user_id)
            if get_date is not None:
                db_data = Wage.objects.filter(IC_num=user_ic.IC_num, date=get_date)
            else:
                db_data = Wage.objects.filter(IC_num=user_ic.IC_num).order_by("date").reverse()[:6]
            data = [
                {
                    "id": i.id,
                    "date": i.date,
                    "pf": i.pf,
                    "ss": i.ss,
                }
                for i in db_data]

            return JsonResponse({
                "status_code": 0,
                "data": data
            })

        # 获取用户详细信息
        if get_user_detail is not None and get_user_detail == "true":
            if get_username is not None:
                db_data = User.objects.filter(is_superuser=0).filter(username__contains=get_username)
            else:
                db_data = User.objects.filter(is_superuser=0)
            data = [
                {
                    "id": i.id,
                    "username": i.username,
                    "is_staff": i.is_staff,
                    "is_active": i.is_active,
                    "email": i.email,
                    "date_joined": i.date_joined,
                    "last_login": i.last_login,
                    "IC_num": UserIC.objects.get(user_id=i.id).IC_num
                }
                for i in db_data[start:end]]
            return JsonResponse({
                "status_code": 0,
                "total": len(db_data),
                "data": data
            })

        if get_mp3 is not None:
            data = []
            for i in os.listdir("static/mp3"):
                data.append({"url": f"/apis/static/mp3/{i}",
                             "name": i})

            return JsonResponse({
                "status_code": 0,
                "data": data
            })

        def getMemorystate():
            phymem = psutil.virtual_memory()
            line = "Memory: %5s%% %6s/%s" % (
                phymem.percent,
                str(int(phymem.used / 1024 / 1024)) + "M",
                str(int(phymem.total / 1024 / 1024)) + "M"
            )
            return line

        if get_status is not None:
            data = {}
            data["status_code"] = 0
            # data["cpu_status"] = int(math.fsum(psutil.cpu_percent(interval=1, percpu=True)) // 4)  # 获得cpu当前使用率
            data["cpu_status"] = max(psutil.cpu_percent(interval=1, percpu=True))  # 获得cpu当前使用率
            data["memory_status"] = int(psutil.virtual_memory().percent)  # 获取当前内存使用情况
            data["disk_status"] = int(psutil.disk_usage("/").percent)

            return JsonResponse(data)

        # =====================================================================================
        return JsonResponse({
            "status_code": 1,
            "error": "not data"
        })


#
def change_data(request):
    if request.method == "GET":
        change_active = request.GET.get("change_active")
        user_id = request.GET.get("user_id")
        certification = request.GET.get("certification")
        IC_num = request.GET.get("IC_num")
        # 更改锁定状态
        if change_active is not None and change_active == "true" and user_id is not None:
            db_data = User.objects.get(id=user_id)
            if db_data.is_active == 1:
                db_data.is_active = 0
            else:
                db_data.is_active = 1
            db_data.save()
            return JsonResponse({
                "status_code": 0,
            })

        # 认证，身份证绑定
        if certification is not None and certification == "true" and user_id is not None and IC_num is not None:
            db_data = UserIC.objects.get(user_id=user_id)
            db_data.IC_num = IC_num
            db_data.save()
            return JsonResponse({
                "status_code": 0,
            })


# /apis/add
def add_data(request):
    if request.method == "POST":
        add_blog = request.GET.get("add_data")
        add_access = request.GET.get("access")
        # 添加blog
        if add_blog is not None and add_blog == "1bs2ppJu2I9dl1":
            # 将json转换为python dict格式
            data = json.loads(request.body)
            if data.get("title") is not None and data.get("content") is not None and data.get(
                    "cateory") is not None and data.get("author") is not None:

                # try:
                cateory = Cateory.objects.get(cateory_name=data["cateory"])
                user = User.objects.get(username=data["author"])
                db = Content(title=data["title"], content=data["content"], cateory=cateory, user=user)
                db.save()
                # except:
                #     return JsonResponse({
                #         "status_code": 1,
                #         "error": "save define"
                #     })

                return JsonResponse({
                    "status_code": 0,
                    "data": "success"
                })
            else:
                return JsonResponse({
                    "status_code": 1,
                    "error": "data is vaild"
                })
        # 添加访问数
        if add_access is not None and add_access == "add_access":
            try:
                db = GetNum.objects.get(date=time.strftime("%Y-%m-%d"))
                db.number += 1
                db.save()
                return JsonResponse({
                    "status_code": 0,
                    "data": "first user access"
                })
            except:
                db = GetNum()
                db.number = 1
                db.save()
                return JsonResponse({
                    "status_code": 0,
                    "data": "access success!"
                })

        return JsonResponse({
            "status_code": 1,
            "error": "not done"
        })


# /apis/face  0d62f4e0ccdf47c235e34ba512a882c388f667eae540169c7bfd9a415de303494eea5076f90f21cb2ca0299de4cb3bb2
def checkface(request):
    try:
        files = request.FILES.get("file")
        type_image = files.name.split('.')[-1]
        filename = "./upload/" + hashlib.sha3_384(files.name.encode()).hexdigest() + f".{type_image}"
        with open(filename, "ab+") as fp:
            fp.write(files.read())
        img = BytesIO()
        image = face_recognition.load_image_file(filename)
        locations = face_recognition.face_locations(img=image)
        result_image = Image.fromarray(image)
        for pos in locations:
            d = ImageDraw.Draw(result_image, 'RGBA')
            d.rectangle((pos[3], pos[0], pos[1], pos[2]))
        result_image.save(img, 'png')

        return JsonResponse({
            "status": 0,
            "filename": files.name,
            "face_count": len(locations),
            "resultImg_base": str(base64.b64encode(img.getvalue()).decode())
        })
    except:
        return JsonResponse({
            "status": 1,
            "message": "重试一下吧. 你的照片有问题哦."
        })


class Users:
    @staticmethod
    def get_status(request):
        if request.user.is_authenticated:
            user_ic = UserIC.objects.get(user_id=request.user.id)
            if user_ic.IC_num == "":
                return JsonResponse({
                    "status": 2,  # 登陆未认证
                    "id": str(request.user.id),
                    "is_superuser": User.objects.get(id=request.user.id).is_superuser,
                    "is_staff": User.objects.get(id=request.user.id).is_staff,
                    "username": str(request.user),
                    "email": str(request.user.email)
                })
            else:
                return JsonResponse({
                    "status": 0,  # 登陆且认证
                    "id": str(request.user.id),
                    "is_superuser": User.objects.get(id=request.user.id).is_superuser,
                    "is_staff": User.objects.get(id=request.user.id).is_staff,
                    "username": str(request.user),
                    "email": str(request.user.email)
                })
        else:
            return JsonResponse({
                "status": 1  # 未登陆
            })

    @staticmethod
    def login_user(request):
        if request.method == "POST":
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            if username is not None and password is not None:
                islogin = authenticate(request, username=username, password=password)
                if islogin:
                    login(request, islogin)
                    return JsonResponse({
                        "status": 0,
                        "message": "Login Success",
                        "username": username
                    })
                else:
                    return JsonResponse({
                        "status": 1,
                        "message": "登录失败, 请检查用户名或者密码是否输入正确."
                    })
            else:
                return JsonResponse({
                    "status": 2,
                    "message": "参数错误"
                })

    @staticmethod
    def logout_user(request):
        logout(request)
        return JsonResponse({
            "status": 0
        })

    @staticmethod
    def register(request):
        if request.method == "POST":
            data = json.loads(request.body)

            if request.GET.get("select") is not None:
                select_username = data.get("select_username")
                print(select_username)
                try:
                    User.objects.get(username=select_username)
                    return JsonResponse({
                        "status": 0,
                        "is_indb": 1
                    })
                except:
                    return JsonResponse({
                        'status': 0,
                        "is_indb": 0
                    })
            username = data.get("username")
            password = data.get("password")
            email = data.get("email")
            if username is not None and password is not None and email is not None:
                try:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    user_ic = UserIC(user_id=user.id)
                    user_ic.save()
                    login_user = authenticate(request, username=username, password=password)
                    if login_user:
                        login(request, login_user)
                        return JsonResponse({
                            "status": 0,
                            "message": "Register and Login Success"
                        })

                except:
                    return JsonResponse({
                        "status": 2,
                        "message": "注册失败, 该用户名已经存在."
                    })

        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })
