# Generated by Django 4.2.1 on 2024-10-25 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.CharField(default='work', max_length=50),
            preserve_default=False,
        ),
    ]
