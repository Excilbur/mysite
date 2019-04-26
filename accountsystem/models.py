from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expend(models.Model):#支出数据库表

    account_choice = (('现金', '现金'), ('银行卡', '银行卡'), ('支付宝', '支付宝'))
    outcome_choice = (('服饰', '服饰'), ('食品酒水', '食品酒水'), ('居家物业', '居家物业'),
                      ('行车交通', '行车交通'), ('文化教育', '文化教育'), ('休闲娱乐', '休闲娱乐'))
    people_choice = (('自己', '自己'), ('家人', '家人'), ('其他人', '其他人'))

    username = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                 to_field='username', default='lyj')
    date = models.DateTimeField(auto_now_add=False)  # 日期
    account = models.CharField(max_length=4, choices=account_choice)  # 账户
    outcometype = models.CharField(max_length=4, choices=outcome_choice)  # 支出类型
    people = models.CharField(max_length=4, choices=people_choice, default='自己')
    money = models.FloatField(max_length=20)#金额
    description = models.TextField(null=True)#说明

    def __str__(self):
        return '%s'%self.username

    class Meta:
        ordering = ['date']

class Income(models.Model):#收入数据库表
    account_choice = (('现金', '现金'), ('银行卡', '银行卡'), ('支付宝', '支付宝'))
    income_choice = (('工资', '工资'), ('奖金补贴', '奖金补贴'), ('投资分红', '投资分红'), ('其他', '其他'))
    people_choice = (('自己', '自己'), ('家人', '家人'), ('其他人', '其他人'))

    username = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                 to_field='username', default='lyj')
    date = models.DateTimeField(auto_now_add=False)  # 日期
    account = models.CharField(max_length=4, choices=account_choice)  # 账户
    incometype = models.CharField(max_length=4, choices=income_choice) #收入类别
    people = models.CharField(max_length=4, choices=people_choice, default='自己')
    money = models.FloatField(max_length=20)  # 金额
    description = models.TextField(null=True)  # 说明

    def __str__(self):
        return '%s'%self.username

    class Meta:
        ordering = ['date']


class Member(models.Model):
    relation_choice = (('夫妻', '夫妻'), ('父子', '父子'), ('父女', '父女'), ('母子', '母子'),
                       ('母女', '母女'), ('兄弟姐妹', '兄弟姐妹'), ('其他', '其他'))

    username = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                 to_field='username', default='lyj')#一家之主
    member_name = models.CharField(max_length=8, default='try')#成员姓名
    member_relation = models.CharField(max_length=4, choices=relation_choice)#关系
    member_password = models.CharField(max_length=20, default='111111',
                                       help_text='成员密码，默认为111111')#密码
    description = models.TextField(null=True)  # 说明

    class Meta:
        ordering = ['id']
