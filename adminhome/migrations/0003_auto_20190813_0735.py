# Generated by Django 2.2.3 on 2019-08-13 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0002_auto_20190813_0442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='pincode',
            field=models.PositiveIntegerField(null=True),
        ),
    ]