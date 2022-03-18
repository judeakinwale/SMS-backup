# Generated by Django 3.2 on 2022-03-04 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0015_auto_20220125_2238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendedcourses',
            name='courses',
        ),
        migrations.AddField(
            model_name='recommendedcourses',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='academics.course'),
        ),
        migrations.AddField(
            model_name='recommendedcourses',
            name='is_compulsory',
            field=models.BooleanField(default=True),
        ),
    ]