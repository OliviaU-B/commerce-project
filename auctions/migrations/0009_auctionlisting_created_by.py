# Generated by Django 3.2 on 2021-05-17 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='created_by',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
