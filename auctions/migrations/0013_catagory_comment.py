# Generated by Django 4.1.7 on 2023-05-31 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_bids_bidsa_alter_comments_list_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='catagory',
            name='comment',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
