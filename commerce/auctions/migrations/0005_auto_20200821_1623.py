# Generated by Django 3.1 on 2020-08-21 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_user_earnings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='Bid',
        ),
        migrations.RemoveField(
            model_name='product',
            name='startingBid',
        ),
        migrations.AlterField(
            model_name='product',
            name='ImageUrl',
            field=models.CharField(max_length=500),
        ),
    ]