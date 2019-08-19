# Generated by Django 2.2.3 on 2019-08-15 11:56

import adminhome.models
import adminhome.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0007_auto_20190815_0734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='principal',
            name='resume',
            field=models.FileField(upload_to=adminhome.models.get_upload_path, validators=[adminhome.validators.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='resume',
            field=models.FileField(upload_to=adminhome.models.get_upload_path, validators=[adminhome.validators.validate_file_extension]),
        ),
    ]