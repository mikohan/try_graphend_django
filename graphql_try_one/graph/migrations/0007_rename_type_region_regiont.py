# Generated by Django 3.2.9 on 2021-11-15 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0006_rename_type_deliverymodel_t_attention'),
    ]

    operations = [
        migrations.RenameField(
            model_name='region',
            old_name='type',
            new_name='regionT',
        ),
    ]