# Generated by Django 5.1.7 on 2025-03-28 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('seeker', 'Job Seeker'), ('recruiter', 'Recruiter'), ('admin', 'Admin')], default='seeker', max_length=20),
        ),
    ]
