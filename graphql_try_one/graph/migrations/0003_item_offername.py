# Generated by Django 3.2.9 on 2021-11-15 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0002_item_partnerwarehouseid'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='offerName',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
