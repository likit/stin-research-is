# Generated by Django 2.1.7 on 2019-04-18 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0004_irbrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='budget',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='intro',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='method',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='objective',
            field=models.TextField(null=True),
        ),
    ]
