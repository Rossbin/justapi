# Generated by Django 2.2.2 on 2021-03-31 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_auto_20210329_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(default='just@qq.com', max_length=64, verbose_name='导师联系方式'),
        ),
    ]
