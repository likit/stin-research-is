# Generated by Django 2.1.7 on 2019-05-02 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_researcher',
            field=models.BooleanField(default=True),
        ),
    ]
