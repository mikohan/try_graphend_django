# Generated by Django 3.2.9 on 2021-11-15 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0003_auto_20211115_1034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery',
        ),
        migrations.AddField(
            model_name='delivery',
            name='order',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='graph.order'),
            preserve_default=False,
        ),
    ]