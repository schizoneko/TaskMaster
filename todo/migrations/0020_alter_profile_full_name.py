# Generated by Django 5.1 on 2024-08-14 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0019_message_reply_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.CharField(default='None', max_length=100),
        ),
    ]
