# Generated by Django 3.2.9 on 2021-11-15 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0004_alter_item_offername'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Delivery',
            new_name='DeliveryModel',
        ),
    ]