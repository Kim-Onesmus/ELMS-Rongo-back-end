# Generated by Django 4.2 on 2023-05-24 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_worker_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.department'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='job_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.jobgroup'),
        ),
    ]