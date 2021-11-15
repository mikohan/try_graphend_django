# Generated by Django 3.2.9 on 2021-11-14 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('RUR', 'RUR'), ('USD', 'USD')], default='RUR', max_length=3)),
                ('fake', models.BooleanField(blank=True, default=False, null=True)),
                ('order_id', models.PositiveBigIntegerField()),
                ('paymentType', models.CharField(choices=[('PREPAID', 'PREPAID'), ('POSTPAID', 'POSTPAID')], default='POSTPAID', max_length=50)),
                ('paymentMethod', models.CharField(choices=[('YANDEX', 'YANDEX'), ('APPLE_PAY', 'APPLE_PAY'), ('GOOGLE_PAY', 'GOOGLE_PAY'), ('CREDIT', 'CREDIT'), ('TINKOFF_CREDIT', 'TINKOFF_CREDIT'), ('EXTERNAL_CERTIFICATE', 'EXTERNAL_CERTIFICATE'), ('CARD_ON_DELIVERY', 'CARD_ON_DELIVERY'), ('CASH_ON_DELIVERY', 'CASH_ON_DELIVERY')], default='CASH_ON_DELIVERY', max_length=50)),
            ],
        ),
    ]
