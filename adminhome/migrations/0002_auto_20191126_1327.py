# Generated by Django 2.2.3 on 2019-11-26 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminhome', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='student',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminhome.School'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='school',
            name='school_admin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='principal',
            name='school',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='adminhome.School'),
        ),
        migrations.AddField(
            model_name='principal',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='parent',
            name='parent_of',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminhome.Student'),
        ),
        migrations.AddField(
            model_name='localadmin',
            name='school',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='adminhome.School'),
        ),
    ]
