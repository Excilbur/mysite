from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django import forms
from django.contrib import auth
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum
from django.urls import reverse
from mysite.forms import RegisterForm, LoginForm
from .models import Expend, Income, Member

# Create your views here.
def Index(request):
    return render(request, 'index.html')

def Register(request):#注册
    context = {}

    if request.method == 'POST':
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

            today = timezone.now().date()
            dates = []
            expends_sum = []
            incomes_sum = []

            context['username'] = username
            contents_expend = Expend.objects.filter(username_id=username)
            contents_income = Income.objects.filter(username_id=username)

            for i in range(6, -1, -1):
                date = today - timedelta(days=i)
                tomorrow = date + timedelta(days=1)
                dates.append(date.strftime('%y/%m/%d'))

                expend_detail = Expend.objects.filter(username_id=username,
                                                      date__lt=tomorrow, date__gte=date)
                expend_result = expend_detail.aggregate(expend_money_num=Sum('money'))

                income_detail = Income.objects.filter(username_id=username,
                                                      date__lt=tomorrow, date__gte=date)
                income_result = income_detail.aggregate(income_money_num=Sum('money'))

                expends_sum.append(expend_result['expend_money_num'] or 0)
                incomes_sum.append(income_result['income_money_num'] or 0)

            context['contents_expend'] = contents_expend
            context['contents_income'] = contents_income
            context['contents_user'] = user
            context['dates'] = dates
            context['expends_sum'] = expends_sum
            context['incomes_sum'] = incomes_sum

            #return redirect(request.GET.get('from', reverse('login')))
            return render(request, 'personalcenter.html', context)
    else:
        reg_form = RegisterForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)

def Login(request):#登录
    context = {}

    if request.method == 'POST':  # POST方法请求页面
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            #user = login_form.cleaned_data['user']
            #auth.login(request, user)

            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('', reverse('index')))
            #return render(request, 'personalcenter.html', context)
    else:  # get方法请求页面
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def PersonalCeneter(request):
    context = {}

    referer = request.META.get('HTTP_REFERER', reverse('index'))

    today = timezone.now().date()
    dates = []
    expends_sum = []
    incomes_sum = []

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:

        auth.login(request, user)

        context['username'] = username
        contents_expend = Expend.objects.filter(username_id=username)
        contents_income = Income.objects.filter(username_id=username)
        contents_user = User.objects.get(username=username)


        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            yesterday = date - timedelta(days=1)
            tomorrow = date + timedelta(days=1)
            dates.append(date.strftime('%y/%m/%d'))

            expend_detail = Expend.objects.filter(username_id=username,
                                                  date__lt=tomorrow, date__gte=date)
            expend_result = expend_detail.aggregate(expend_money_num=Sum('money'))

            income_detail = Income.objects.filter(username_id=username,
                                                  date__lt=tomorrow, date__gte=date)
            income_result = income_detail.aggregate(income_money_num=Sum('money'))


            expends_sum.append(expend_result['expend_money_num'] or 0)
            incomes_sum.append(income_result['income_money_num'] or 0)

        context['contents_expend'] = contents_expend
        context['contents_income'] = contents_income
        context['contents_user'] = contents_user
        context['dates'] = dates
        context['expends_sum'] = expends_sum
        context['incomes_sum'] = incomes_sum

        return render(request, 'personalcenter.html', context)
    else:
        return render(request, 'error.html', {'message': '用户名或密码不正确', 'redirect_to': referer})

def PersonalCenterAgain(request, pk1, pk2):
    context = {}
    today = timezone.now().date()
    dates = []
    expend_sum = []
    income_sum = []
    user = User.objects.get(pk=pk1)

    username = user.username
    context['username'] = username
    contents_expend = Expend.objects.filter(username_id=username)
    contents_income = Income.objects.filter(username_id=username)
    contents_user = User.objects.get(username=username)

    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        yesterday = date - timedelta(days=1)
        tomorrow = date + timedelta(days=1)
        dates.append(date.strftime('%m/%d'))
        expend_detail = Expend.objects.filter(username_id=username,
                                              date__lt=tomorrow, date__gt=date)
        expend_result = expend_detail.aggregate(expend_money_num=Sum('money'))

        income_detail = Income.objects.filter(username_id=username,
                                              date__lt=tomorrow, date__gt=date)
        income_result = income_detail.aggregate(income_money_num=Sum('money'))


        expend_sum.append(expend_result['expend_money_num'] or 0)
        income_sum.append(income_result['income_money_num'] or 0)

    context['contents_expend'] = contents_expend
    context['contents_income'] = contents_income
    context['contents_user'] = contents_user

    context['dates'] = dates
    context['expends_sum'] = expend_sum
    context['incomes_sum'] = income_sum
    return render(request, 'personalcenter.html', context)

def UserLogout(request):#注销
    auth.logout(request)
    if request.method == 'POST':  # POST方法请求页面
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('', reverse('index')))
    else:  # get方法请求页面
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def UpdateInformation(request, user_pk):
    context = {}

    user = User.objects.get(pk=user_pk)
    context['user'] = user

    return render(request, 'UpdateInformation.html', context)

def Update(request, user_pk):
    referer = request.META.get('HTTP_REFERER', reverse('index'))
    context = {}

    user = User.objects.get(pk=user_pk)
    username = user.username

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password_again = request.POST['password_again']

        if len(password) < 6:
            message = "密码长度最少为6位"
            context['message'] = message
            context['redirect_to'] = referer
            return render(request, 'error.html', context)

        if password != password_again:
            message = "两次输入的密码不一致"
            context['message'] = message
            context['redirect_to'] = referer
            return render(request, 'error.html', context)

        if User.objects.filter(email=email).count() > 1:
            message = "邮箱已存在"
            context['message'] = message
            context['redirect_to'] = referer
            return render(request, 'error.html', context)

        user.username = username
        user.email = email
        user.set_password(password)
        user.save()

    login_form = LoginForm()
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def MemberList(request, user_pk):
    context = {}

    user = User.objects.get(pk=user_pk)
    username = user.username
    user_members = Member.objects.filter(username_id=username)

    context['user_members'] = user_members
    context['user'] = user
    return render(request, 'member-list.html', context)

def AddMember(request, user_pk):
    context = {}

    user = User.objects.get(pk=user_pk)
    context['user'] = user
    return render(request, 'add-member.html', context)

def SaveMember(request, user_pk):
    context = {}

    user = User.objects.get(pk=user_pk)
    username = user.username
    user_member = Member.objects.filter(username_id=username)

    if request.method == 'POST':
        member_name = request.POST.get('member_name')
        member_relation = request.POST.get('member_relation')
        member_description = request.POST.get('member_description')
        member_password = request.POST.get('member_password')

        if member_name.strip() == '':
            message = '成员姓名不能为空'
            context['message'] = message
            return render(request, 'error.html', context)

        if Member.objects.filter(member_name=member_name).count() > 0:
            message = '成员已存在'
            context['message'] = message
            return render(request, 'error.html', context)

        if member_password.strip() == '':
            member_password = '111111'

        Member.objects.create(username_id=username, member_name=member_name, member_relation=member_relation,
                              member_password=member_password, description=member_description)

    context['user'] = user
    context['user_members'] = user_member
    return render(request, 'member-list.html', context)

def MemberDetail(request, pk):
    context = {}

    member_detail = Member.objects.get(pk=pk)
    username = member_detail.username
    user = User.objects.get(username=username)

    context['member_detail'] = member_detail
    context['user'] = user

    return render(request, 'member-detail.html', context)

def UpdateMember(request, pk):
    context = {}

    member_detail = Member.objects.get(pk=pk)
    member_first_name = member_detail.member_name
    username = member_detail.username
    user = User.objects.get(username=username)
    user_member = Member.objects.filter(username_id=username)

    if request.method == 'POST':
        member_name = request.POST.get('member_name')
        member_relation = request.POST.get('member_relation')
        member_password = request.POST.get('member_password')
        member_description = request.POST.get('member_description')

        if member_first_name != member_name:
            if Member.objects.filter(member_name=member_name).count() >= 1:
                message = '成员已存在'
                context['message'] = message
                return render(request, 'error.html', context)

        if member_name.strip() == '':
            message = '成员姓名不能为空'
            context['message'] = message
            return render(request, 'error.html', context)

        if member_password.strip() == '':
            member_password = '111111'

        member_detail.member_name = member_name
        member_detail.member_password = member_password
        member_detail.member_relation = member_relation
        member_detail.description = member_description
        member_detail.save()

    context['user'] = user
    context['user_members'] = user_member
    return render(request, 'member-list.html', context)

def DeleteMember(request, pk):
    context = {}

    member_detail = Member.objects.get(pk=pk)
    username = member_detail.username
    user = User.objects.get(username=username)
    user_members = Member.objects.filter(username_id=username)
    Member.objects.get(pk=pk).delete()
    context['user'] = user
    context['user_members'] = user_members
    return render(request, 'member-list.html', context)
