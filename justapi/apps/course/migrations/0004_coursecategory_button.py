# Generated by Django 2.2.2 on 2021-03-28 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20210324_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecategory',
            name='button',
            field=models.BooleanField(default=False, verbose_name='前端按钮遍历'),
        ),
    ]