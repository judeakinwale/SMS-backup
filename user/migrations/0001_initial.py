# Generated by Django 3.2.4 on 2021-08-11 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('academics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=250, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=250, null=True)),
                ('last_name', models.CharField(max_length=250, null=True)),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Biodata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marital_status', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Other', 'Other')], default='Other', max_length=250)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other', max_length=250)),
                ('religion', models.CharField(choices=[('Christianity', 'Christianity'), ('Islam', 'Islam'), ('Other', 'Other')], default='Other', max_length=250)),
                ('birthday', models.DateField(null=True)),
                ('nationality', models.CharField(blank=True, max_length=250, null=True)),
                ('state_of_origin', models.CharField(max_length=250, null=True)),
                ('local_govt', models.CharField(max_length=250, null=True)),
                ('permanent_address', models.CharField(max_length=250, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('phone_no_1', models.CharField(max_length=20, null=True)),
                ('phone_no_2', models.CharField(blank=True, max_length=20, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='images/profile_pictures/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='biodata', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Biodata',
                'verbose_name_plural': 'Biodata',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matric_no', models.CharField(blank=True, max_length=250, null=True)),
                ('student_id', models.CharField(max_length=250, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=250, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_lecturer', models.BooleanField(default=False)),
                ('is_bursar', models.BooleanField(default=False)),
                ('is_IT', models.BooleanField(default=False)),
                ('is_head_of_department', models.BooleanField(default=False)),
                ('is_dean_of_faculty', models.BooleanField(default=False)),
                ('programme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='academics.programme')),
                ('user', models.ForeignKey(limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Staff',
                'verbose_name_plural': 'Staff',
            },
        ),
        migrations.CreateModel(
            name='HealthData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.CharField(default='', max_length=300)),
                ('genotype', models.CharField(default='', max_length=300)),
                ('allergies', models.TextField(blank=True, null=True)),
                ('diabetes', models.BooleanField(default=False)),
                ('STIs', models.TextField(null=True)),
                ('heart_disease', models.TextField(blank=True, null=True)),
                ('disabilities', models.TextField(blank=True, null=True)),
                ('respiratory_problems', models.TextField(blank=True, null=True)),
                ('biodata', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='health_data', to='user.biodata')),
            ],
            options={
                'verbose_name': 'HealthData',
                'verbose_name_plural': 'HealthData',
            },
        ),
        migrations.CreateModel(
            name='FamilyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('next_of_kin_full_name', models.CharField(max_length=250, null=True)),
                ('next_of_kin_phone_no_1', models.CharField(max_length=250, null=True)),
                ('next_of_kin_phone_no_2', models.CharField(max_length=250, null=True)),
                ('next_of_kin_address', models.CharField(max_length=250, null=True)),
                ('guardian_full_name', models.CharField(max_length=250, null=True)),
                ('guardian_phone_no_1', models.CharField(max_length=250, null=True)),
                ('guardian_phone_no_2', models.CharField(max_length=250, null=True)),
                ('guardian_address', models.CharField(max_length=250, null=True)),
                ('biodata', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='family_data', to='user.biodata')),
            ],
            options={
                'verbose_name': 'FamilyData',
                'verbose_name_plural': 'FamilyData',
            },
        ),
        migrations.CreateModel(
            name='CourseRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(blank=True, max_length=250, null=True)),
                ('semester', models.CharField(blank=True, max_length=250, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_passed', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.student')),
            ],
            options={
                'verbose_name': 'AcademicData',
                'verbose_name_plural': 'AcademicData',
            },
        ),
        migrations.CreateModel(
            name='AcademicHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=250, null=True)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('qualification_earned', models.CharField(choices=[('Other', 'Other')], default='Other', max_length=250, null=True)),
                ('biodata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='academic_history', to='user.biodata')),
            ],
            options={
                'verbose_name': 'AcademicHistory',
                'verbose_name_plural': 'AcademicHistory',
            },
        ),
        migrations.CreateModel(
            name='AcademicData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.DateTimeField(null=True)),
                ('ended', models.DateTimeField(blank=True, null=True)),
                ('qualification', models.CharField(choices=[('Other', 'Other')], default='Other', max_length=250, null=True)),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.programme')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='academic_data', to='user.student')),
            ],
        ),
    ]
