# Generated by Django 2.2.3 on 2019-08-14 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0005_teacher_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='principal',
            name='subject',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='has_principal',
            field=models.BooleanField(default=False),
        ),
    ]