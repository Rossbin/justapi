# Generated by Django 2.2.2 on 2021-04-01 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_auto_20210331_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='brief_text',
            field=models.TextField(blank=True, max_length=2048, null=True, verbose_name='章节介绍'),
        ),
    ]
