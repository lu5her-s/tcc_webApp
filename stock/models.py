from django.db import models
from asset.models import StockItem
from inform.models import Inform

# Create your models here.

class RelayStockBill(models.Model):
    """
    Represents a relay stock bill entry in the database.

    A RelayStockBill records the movement of a stock item within the system, including details such as the item itself,
    quantity, creation timestamp, and whether an information request has been made.

    Parameters:
        item (StockItem): The stock item associated with this bill.
        qty (int, optional): The quantity of the stock item being moved. Defaults to 1.
        created_at (datetime): The timestamp when this bill was created.
        inform_request (bool, optional): A flag indicating whether an information request has been made. Defaults to False.
        inform (Inform, optional): An optional link to an Inform object for additional information.

    Attributes:
        id (int): The unique identifier for this RelayStockBill.

    Note:
        - When creating a new RelayStockBill, the 'item' and 'created_at' parameters are required.
        - If 'qty' is not provided, it defaults to 1.
        - 'inform_request' is a boolean flag that can be set to True if additional information is requested.
        - 'inform' can be linked to an Inform object for more detailed information.

    Examples:
        Creating a new RelayStockBill:
        ```
        bill = RelayStockBill(item=my_stock_item, created_at=timezone.now())
        bill.save()
        ```

    """
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    inform_request = models.BooleanField(default=False)
    inform = models.ForeignKey(Inform, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{pk} - {self.item.item_name} - {self.qty}'


class DataStockBill(models.Model):
    """
    Represents a data stock bill entry in the database.
    """
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    inform_request = models.BooleanField(default=False)
    inform = models.ForeignKey(Inform, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{pk} - {self.item.item_name} - {self.qty}'


class SatteliteStockBill(models.Model):
    """
    Represents a sattelite stock bill entry in the database.
    """
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    inform_request = models.BooleanField(default=False)
    inform = models.ForeignKey(Inform, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{pk} - {self.item.item_name} - {self.qty}'


class AirStockBill(models.Model):
    """
    Represents an air stock bill entry in the database.
    """
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    inform_request = models.BooleanField(default=False)
    inform = models.ForeignKey(Inform, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{pk} - {self.item.item_name} - {self.qty}'
