# Generated by Django 2.2.3 on 2019-08-13 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='pincode',
            field=models.PositiveIntegerField(),
        ),
    ]