# Generated by Django 4.2.7 on 2023-11-16 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_coresetting_time_to_execute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coresetting',
            name='twitter',
            field=models.TextField(null=True),
        ),
    ]
