# Generated by Django 3.2.4 on 2021-09-25 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0009_auto_20210925_0946'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
            ],
            options={
                'verbose_name': 'Session',
                'verbose_name_plural': 'Sessions',
            },
        ),
    ]
