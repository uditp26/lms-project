# Generated by Django 2.2.3 on 2019-08-14 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0003_auto_20190813_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='class_upto',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
