# Generated by Django 2.2.2 on 2021-03-24 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20210324_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pay_time',
            field=models.DateTimeField(null=True, verbose_name='支付时间'),
        ),
    ]