from django.db import models
from django.contrib.auth.models import User
from asset.models import StockItem

# Create your models here.

from django.db import models

class RelayStockBill(models.Model):
    """
    Represents a stock bill for relay devices.
    Each instance of this class corresponds to a bill for purchasing or selling relay devices.

    Attributes:
        bill_number (CharField): The unique identifier for the stock bill.
        date_created (DateTimeField): The date and time when the bill was created.
        items (ManyToManyField): The relay devices associated with this bill.
        is_purchase (BooleanField): Indicates whether the bill is for a purchase (True) or a sale (False).
        total_amount (DecimalField): The total amount of the bill in currency.
    """

    bill_number = models.CharField(max_length=20, unique=True, help_text="Unique identifier for the stock bill.")
    date_created = models.DateTimeField(auto_now_add=True, help_text="Date and time when the bill was created.")
    items = models.ManyToManyField('RelayDevice', through='BillItem', help_text="Relay devices associated with the bill.")
    is_purchase = models.BooleanField(default=True, help_text="True if the bill is for a purchase, False if for a sale.")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total amount of the bill.")

    class Meta:
        verbose_name = "Relay Stock Bill"
        verbose_name_plural = "Relay Stock Bills"

    def __str__(self):
        return f"{self.bill_number} - {'Purchase' if self.is_purchase else 'Sale'} Bill"


class RelayDevice(models.Model):
    """
    Represents a relay device that can be included in stock bills.

    Attributes:
        serial_number (CharField): The unique serial number of the relay device.
        name (CharField): The name or description of the relay device.
        price (DecimalField): The price of the relay device.
    """

    serial_number = models.CharField(max_length=30, unique=True, help_text="Unique serial number of the relay device.")
    name = models.CharField(max_length=100, help_text="Name or description of the relay device.")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the relay device.")

    class Meta:
        verbose_name = "Relay Device"
        verbose_name_plural = "Relay Devices"

    def __str__(self):
        return self.name


class BillItem(models.Model):
    """
    Represents an individual item on a stock bill.

    Attributes:
        bill (ForeignKey): The stock bill this item belongs to.
        relay_device (ForeignKey): The relay device associated with this item.
        quantity (PositiveIntegerField): The quantity of relay devices in this item.
    """

    bill = models.ForeignKey(RelayStockBill, on_delete=models.CASCADE, help_text="Stock bill this item belongs to.")
    relay_device = models.ForeignKey(RelayDevice, on_delete=models.CASCADE, help_text="Relay device for this item.")
    quantity = models.PositiveIntegerField(help_text="Quantity of relay devices in this item.")

    class Meta:
        verbose_name = "Bill Item"
        verbose_name_plural = "Bill Items"

    def __str__(self):
        return f"{self.quantity} x {self.relay_device.name} ({self.bill.bill_number})"

