# Generated by Django 3.2.4 on 2021-08-11 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('information', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='informationimage',
            name='information',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='information.information'),
        ),
        migrations.AddField(
            model_name='information',
            name='scope',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='information.scope'),
        ),
        migrations.AddField(
            model_name='information',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
