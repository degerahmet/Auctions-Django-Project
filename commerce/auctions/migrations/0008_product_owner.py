# Generated by Django 3.1 on 2020-08-22 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_comment_commenttitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
