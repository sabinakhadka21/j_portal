# Generated by Django 4.2.4 on 2023-11-28 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_createjob_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createjob',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='createjob',
            name='modified_at',
            field=models.DateField(auto_now=True),
        ),
    ]
