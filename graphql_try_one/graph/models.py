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

    class Status(models.TextChoices):
        CANCELLED = "CANCELLED", _("CANCELLED")
        DELIVERED = "DELIVERED", _("DELIVERED")
        DELIVERY = "DELIVERY", _("DELIVERY")
        PICKUP = "PICKUP", _("PICKUP")
        PROCESSING = "PROCESSING", _("PROCESSING")
        PENDING = "PENDING", _("PENDING")
        UNPAID = "UNPAID", _("UNPAID")

    class SubStatus(models.TextChoices):
        STARTED = "STARTED", _("STARTED")
        ANTIFRAUD = "ANTIFRAUD", _("ANTIFRAUD")
        DELIVERY_SERVICE_UNDELIVERED = "DELIVERY_SERVICE_UNDELIVERED", _(
            "DELIVERY_SERVICE_UNDELIVERED"
        )
        PENDING_EXPIRED = "PENDING_EXPIRED", _("PENDING_EXPIRED")
        PROCESSING_EXPIRED = "PROCESSING_EXPIRED", _("PROCESSING_EXPIRED")
        REPLACING_ORDER = "REPLACING_ORDER", _("REPLACING_ORDER")
        RESERVATION_EXPIRED = "RESERVATION_EXPIRED", _("RESERVATION_EXPIRED")
        RESERVATION_FAILED = "RESERVATION_FAILED", _("RESERVATION_FAILED")
        SHOP_FAILED = "SHOP_FAILED", _("SHOP_FAILED")
        SHOP_PENDING_CANCELLED = "SHOP_PENDING_CANCELLED", _("SHOP_PENDING_CANCELLED")
        WAREHOUSE_FAILED_TO_SHIP = "WAREHOUSE_FAILED_TO_SHIP", _(
            "WAREHOUSE_FAILED_TO_SHIP"
        )
        USER_CHANGED_MIND = "USER_CHANGED_MIND", _("USER_CHANGED_MIND")
        USER_NOT_PAID = "USER_NOT_PAID", _("USER_NOT_PAID")
        USER_REFUSED_DELIVERY = "USER_REFUSED_DELIVERY", _("USER_REFUSED_DELIVERY")
        USER_REFUSED_PRODUCT = "USER_REFUSED_PRODUCT", _("USER_REFUSED_PRODUCT")
        USER_REFUSED_QUALITY = "USER_REFUSED_QUALITY", _("USER_REFUSED_QUALITY")
        USER_UNREACHABLE = "USER_UNREACHABLE", _("USER_UNREACHABLE")
        PICKUP_SERVICE_RECEIVED = "PICKUP_SERVICE_RECEIVED", _(
            "PICKUP_SERVICE_RECEIVED"
        )
        PICKUP_USER_RECEIVED = "PICKUP_USER_RECEIVED", _("PICKUP_USER_RECEIVED")

    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.RUR
    )
    # delivery = models.OneToOneField(
    #     "DeliveryModel",
    #     on_delete=models.CASCADE,
    #     related_name="delivery",
    #     null=True,
    #     blank=True,
    # )

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

    status = models.CharField(max_length=50, choices=Status.choices, default=None)
    substatus = models.CharField(max_length=50, choices=SubStatus.choices, default=None)

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
    buyerPrice = models.FloatField(null=True, blank=True)
    subsidy = models.FloatField(null=True, blank=True)
    count = models.IntegerField()
    delivery = models.BooleanField()
    params = models.CharField(max_length=255, blank=True, null=True)
    vat = models.CharField(
        max_length=255, choices=Vat.choices, default=None, blank=True, null=True
    )
    fulfilmentShopId = models.PositiveBigIntegerField(blank=True, null=True)
    sku = models.CharField(max_length=255)
    shopSku = models.CharField(max_length=255)
    warehouseId = models.PositiveBigIntegerField(blank=True, null=True)
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


class DeliveryModel(models.Model):
    class DeliveryPartner(models.TextChoices):
        YANDEX_MARKET = "YANDEX_MARKET", _("YANDEX_MARKET")
        # Divider

    class DevType(models.TextChoices):
        DELIVERY = "DELIVERY", _("DELIVERY")
        PICKUP = "PICKUP", _("PICKUP")
        POST = "POST", _("POST")

    deliveryPartnerType = models.CharField(
        max_length=100,
        choices=DeliveryPartner.choices,
        default=DeliveryPartner.YANDEX_MARKET,
    )
    deliveryServiceId = models.PositiveBigIntegerField(null=True, blank=True)
    serviceName = models.CharField(max_length=255, null=True, blank=True)
    t_attention = models.CharField(
        max_length=255, choices=DevType.choices, blank=True, null=True, default=None
    )
    region = models.ForeignKey("Region", on_delete=models.CASCADE)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="delivery"
    )

    def __str__(self):
        return str(self.region)


class Shipment(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    shipmentDate = models.DateField(blank=True, null=True)
    delivery = models.ForeignKey(
        DeliveryModel, on_delete=models.CASCADE, related_name="shipments"
    )

    def __str__(self):
        return str(self.id)


class Region(models.Model):
    class RegionModelType(models.TextChoices):
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
    regionT = models.CharField(
        max_length=200, choices=RegionModelType.choices, blank=True, null=True
    )
    parent = models.ForeignKey(
        "self", on_delete=models.DO_NOTHING, null=True, blank=True
    )

    def __str__(self):
        return str(self.name)
