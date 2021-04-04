# Generated by Django 2.2.2 on 2021-04-04 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_generalcategory_show'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.SmallIntegerField(choices=[(0, '零基础'), (1, '进阶'), (2, '高级')], default=0, verbose_name='难度等级'),
        ),
    ]
