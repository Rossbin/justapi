# Generated by Django 2.2.2 on 2021-04-20 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20210419_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_user', to='user.User', verbose_name='下单用户'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='course',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_orders', to='course.Course', verbose_name='课程'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='order_courses', to='order.Order', verbose_name='订单'),
        ),
    ]