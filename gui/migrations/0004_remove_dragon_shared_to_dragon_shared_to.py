# Generated by Django 4.1.4 on 2022-12-27 16:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gui', '0003_dragon_shared_to_alter_dragon_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dragon',
            name='shared_to',
        ),
        migrations.AddField(
            model_name='dragon',
            name='shared_to',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
