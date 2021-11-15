from django.db import models
import graphene
from django.utils.translation import gettext_lazy as _


class TestModel(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    class Currency(models.TextChoices):
        RUR = "RUR", _("RUR")
        USD = "USD", _("USD")

    class PaymentType(models.TextChoices):
        PREPAID = "PREPAID", _("PREPAID")
        POSTPAID = "POSTPAID", _("POSTPAID")

    class PaymentMethod(models.TextChoices):
        YANDEX = "YANDEX", _("YANDEX")
        APPLE_PAY = "APPLE_PAY", _("APPLE_PAY")
        GOOGLE_PAY = "GOOGLE_PAY", _("GOOGLE_PAY")
        CREDIT = "CREDIT", _("CREDIT")
        TINKOFF_CREDIT = "TINKOFF_CREDIT", _("TINKOFF_CREDIT")
        EXTERNAL_CERTIFICATE = "EXTERNAL_CERTIFICATE", _("EXTERNAL_CERTIFICATE")
        CARD_ON_DELIVERY = "CARD_ON_DELIVERY", _("CARD_ON_DELIVERY")
        CASH_ON_DELIVERY = "CASH_ON_DELIVERY", _("CASH_ON_DELIVERY")

    class TaxSystem(models.TextChoices):
        ECHN = "ECHN", _("ECHN")
        ENVD = "ENVD", _("ENVD")
        OSN = "OSN", _("OSN")
        PSN = "PSN", _("PSN")
        USN = "USN", _("USN")
        USN_MINUS_COST = "USN_MINUS_COST", _("USN_MINUS_COST")

    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.RUR
    )

    id = models.PositiveBigIntegerField(primary_key=True)
    fake = models.BooleanField(default=False, null=True, blank=True)
    paymentType = models.CharField(
        max_length=50, choices=PaymentType.choices, default=PaymentType.POSTPAID
    )
    paymentMethod = models.CharField(
        max_length=50,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH_ON_DELIVERY,
    )
    taxSystem = models.CharField(
        max_length=200, choices=TaxSystem.choices, default=None
    )

    notes = models.TextField()

    class Meta:
        verbose_name = "Order"

    def __str__(self):
        return str(self.id)


class Item(models.Model):
    class Vat(models.TextChoices):
        NO_VAT = "NO_VAT", _("NO_VAT")
        VAT_0 = "VAT_0", _("VAT_0")
        VAT_10 = "VAT_10", _("VAT_10")
        VAT_10_110 = "VAT_10_110", _("VAT_10_110")
        VAT_18 = "VAT_18", _("VAT_18")
        VAT_18_118 = "VAT_18_118", _("VAT_18_118")
        VAT_20 = "VAT_20", _("VAT_20")
        VAT_20_120 = "VAT_20_120", _("VAT_20_120")

    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="items")
    id = models.PositiveBigIntegerField(primary_key=True)
    feedId = models.PositiveBigIntegerField()
    offerId = models.CharField(max_length=255)
    offerName = models.CharField(max_length=255)
    price = models.FloatField()
    buyerPrice = models.FloatField()
    subsidy = models.FloatField()
    count = models.IntegerField()
    delivery = models.BooleanField()
    params = models.CharField(max_length=255)
    vat = models.CharField(max_length=255, choices=Vat.choices, default=None)
    fulfilmentShopId = models.PositiveBigIntegerField()
    sku = models.CharField(max_length=255)
    shopSku = models.CharField(max_length=255)
    warehouseId = models.PositiveBigIntegerField()
    partnerWarehouseId = models.CharField(
        max_length=255, blank=True, null=True, default=None
    )

    def __str__(self):
        return str(self.offerName)


class Promo(models.Model):
    class PromoType(models.TextChoices):
        MARKET_COUPON = "MARKET_COUPON", _("MARKET_COUPON")
        MARKET_DEAL = "MARKET_DEAL", _("MARKET_DEAL")
        MARKET_COIN = "MARKET_COIN", _("MARKET_COIN")

    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="promos")
    marketPromoId = models.CharField(max_length=255)
    subsidy = models.FloatField()
    type = models.CharField(max_length=200, choices=PromoType.choices, default=None)


class Delivery(models.Model):
    class DeliveryPartner(models.TextChoices):
        YANDEX_MARKET = "YANDEX_MARKET", _("YANDEX_MARKET")
        # Divider

    class DevType(models.TextChoices):
        DELIVERY = "DELIVERY", _("DELIVERY")
        PICKUP = "PICKUP", _("PICKUP")
        POST = "POST", _("POST")

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="delivery"
    )
    deliveryPartnerType = models.CharField(
        max_length=100,
        choices=DeliveryPartner.choices,
        default=DeliveryPartner.YANDEX_MARKET,
    )
    deliveryServiceId = models.PositiveBigIntegerField(null=True, blank=True)
    serviceName = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(
        max_length=255, choices=DevType.choices, blank=True, null=True, default=None
    )
    region = models.ForeignKey("Region", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.order)


class Shipment(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    shipmentDate = models.DateField(blank=True, null=True)
    delivery = models.ForeignKey(
        Delivery, on_delete=models.CASCADE, related_name="shipments"
    )

    def __str__(self):
        return str(self.id)


class Region(models.Model):
    class RegionType(models.TextChoices):
        CITY = "CITY", _("CITY")
        CITY_DISTRICT = "CITY_DISTRICT", _("CITY_DISTRICT")
        CONTINENT = "CONTINENT", _("CONTINENT")
        COUNTRY = "COUNTRY", _("COUNTRY")
        COUNTRY_DISTRICT = "COUNTRY_DISTRICT", _("COUNTRY_DISTRICT")
        METRO_STATION = "METRO_STATION", _("METRO_STATION")
        MONORAIL_STATION = "MONORAIL_STATION", _("MONORAIL_STATION")
        OTHERS_UNIVERSAL = "OTHERS_UNIVERSAL", _("OTHERS_UNIVERSAL")
        OVERSEAS_TERRITORY = "OVERSEAS_TERRITORY", _("OVERSEAS_TERRITORY")
        REGION = "REGION", _("REGION")
        SECONDARY_DISTRICT = "SECONDARY_DISTRICT", _("SECONDARY_DISTRICT")
        SETTLEMENT = "SETTLEMENT", _("SETTLEMENT")
        SUBJECT_FEDERATION = "SUBJECT_FEDERATION", _("SUBJECT_FEDERATION")
        SUBJECT_FEDERATION_DISTRICT = "SUBJECT_FEDERATION_DISTRICT", _(
            "SUBJECT_FEDERATION_DISTRICT"
        )
        SUBURB = "SUBURB", _("SUBURB")
        VILLAGE = "VILLAGE", _("VILLAGE")

    id = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=200, choices=RegionType.choices, blank=True, null=True
    )
    parent = models.ForeignKey(
        "self", on_delete=models.DO_NOTHING, null=True, blank=True
    )

    def __str__(self):
        return str(self.name)
