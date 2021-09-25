# Generated by Django 3.2.4 on 2021-09-25 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0014_remove_quiz_score'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['id'], 'verbose_name': 'Answer', 'verbose_name_plural': 'Answers'},
        ),
        migrations.AlterModelOptions(
            name='grade',
            options={'ordering': ['id'], 'verbose_name': 'Grade', 'verbose_name_plural': 'Grades'},
        ),
        migrations.AlterModelOptions(
            name='quiztaker',
            options={'ordering': ['id'], 'verbose_name': 'QuizTaker', 'verbose_name_plural': 'QuizTakers'},
        ),
        migrations.AlterModelOptions(
            name='response',
            options={'ordering': ['id'], 'verbose_name': 'Response', 'verbose_name_plural': 'Responses'},
        ),
        migrations.AddField(
            model_name='grade',
            name='update_reason',
            field=models.TextField(default='None'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grade',
            name='update_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='grade',
            name='updated',
            field=models.BooleanField(default=False),
        ),
    ]
