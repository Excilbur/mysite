# Generated by Django 2.1.7 on 2019-04-22 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountsystem', '0007_auto_20190419_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member_relation',
            field=models.CharField(choices=[('夫妻', '夫妻'), ('父子', '父子'), ('父女', '父女'), ('母子', '母子'), ('母女', '母女'), ('兄弟姐妹', '兄弟姐妹'), ('其他', '其他')], max_length=4),
        ),
    ]
