# Generated by Django 2.2.2 on 2021-04-03 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_auto_20210403_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecategory',
            name='general_category',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.GeneralCategory', verbose_name='总目录分类'),
        ),
    ]
