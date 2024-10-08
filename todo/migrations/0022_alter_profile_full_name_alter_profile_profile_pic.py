# Generated by Django 5.1 on 2024-08-14 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0021_alter_profile_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='profile_pics/'),
        ),
    ]
