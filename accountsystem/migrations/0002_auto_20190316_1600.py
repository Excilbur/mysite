# Generated by Django 2.1.7 on 2019-03-16 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountsystem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expend',
            name='username',
            field=models.CharField(max_length=6),
        ),
    ]