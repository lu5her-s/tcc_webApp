from django.db import models
from django.contrib.auth.models import User
from asset.models import StockItem

# Create your models here.


class RelayBill(models.Model):
    """
    Model representing a relay bill.
    """

    CASE = (
        ('basic', 'basic'),
        ('replace', 'replace'),
        ('rent', 'rent'),
    )

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requester',
        help_text="The user who requested the bill."
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver',
        null=True,
        blank=True,
        help_text="The user who receives the bill."
    )

    request_case = models.CharField(
        max_length=10,
        choices=CASE,
        help_text="The case of the request."
    )

    money_category = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="The category of money."
    )

    job_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="The job number."
    )

    for_req = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="The request information."
    )

    check_comment = models.TextField(
        null=True,
        blank=True,
        help_text="Comments for checking the bill."
    )

    check_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='check_person',
        null=True,
        blank=True,
        help_text="The user who checks the bill."
    )

    approve_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='approve_person',
        null=True,
        blank=True,
        help_text="The user who approves the bill."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the bill was created."
    )


class SatelliteBill(models.Model):
    """
    Represents a satellite bill entry in the system.
    """
    CASE_CHOICES = [
        ('basic', 'Basic'),
        ('replace', 'Replace'),
        ('rent', 'Rent'),
    ]

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requested_bills',
        help_text='The user who requested the bill.'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_bills',
        null=True,
        blank=True,
        help_text='The user who received the bill (optional).'
    )
    request_case = models.CharField(
        max_length=10,
        choices=CASE_CHOICES,
        help_text='The type of request case for the bill.'
    )
    money_category = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text='The category of money associated with the bill.'
    )
    job_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text='The job number associated with the bill.'
    )
    for_req = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text='The purpose for which the bill is requested.'
    )
    check_comment = models.TextField(
        null=True,
        blank=True,
        help_text='Comments related to the bill check.'
    )
    check_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='bills_checked',
        null=True,
        blank=True,
        help_text='The user responsible for checking the bill.'
    )
    approve_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='bills_approved',
        null=True,
        blank=True,
        help_text='The user responsible for approving the bill.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='The timestamp when the bill entry was created.'
    )


class FiberBill(models.Model):
    """
    Model representing a FiberBill.

    FiberBill contains information about the requester, receiver, request case, money category,
    job number, requester for, check comment, check person, approve person, and creation date.

    Attributes:
        CASE (tuple): Choices for the request case field.
        requester (ForeignKey): Reference to the User who made the request.
        receiver (ForeignKey): Reference to the User who received the request.
        request_case (CharField): Indicates the type of request.
        money_category (CharField): Category of the money associated with the request.
        job_no (CharField): Job number associated with the request.
        for_req (CharField): Requester for whom the request is made.
        check_comment (TextField): Additional comments provided during the check.
        check_person (ForeignKey): Reference to the User who performed the check.
        approve_person (ForeignKey): Reference to the User who approved the request.
        created_at (DateTimeField): Date and time when the request was created.
    """

    CASE = [
        ('basic', 'basic'),
        ('replace', 'replace'),
        ('rent', 'rent'),
    ]

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requester',
        help_text="The user who made the request."
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver',
        null=True,
        blank=True,
        help_text="The user who received the request."
    )

    request_case = models.CharField(
        max_length=10,
        choices=CASE,
        help_text="The type of request."
    )

    money_category = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="The category of money associated with the request."
    )

    job_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="The job number associated with the request."
    )

    for_req = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="The requester for whom the request is made."
    )

    check_comment = models.TextField(
        null=True,
        blank=True,
        help_text="Additional comments provided during the check."
    )

    check_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='check_person',
        null=True,
        blank=True,
        help_text="The user who performed the check."
    )

    approve_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='approve_person',
        null=True,
        blank=True,
        help_text="The user who approved the request."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the request was created."
    )


class AirBill(models.Model):
    """
    Model to represent an air bill.

    Attributes:
        requester (User): The user who requested the air bill.
        receiver (User, optional): The user who will receive the air bill.
        request_case (str): The type of request case for the air bill.
        money_category (str, optional): The category of money for the air bill.
        job_no (str, optional): The job number associated with the air bill.
        for_req (str, optional): Additional details for the air bill.
        check_comment (str, optional): Comments for checking the air bill.
        check_person (User, optional): The user responsible for checking the air bill.
        approve_person (User, optional): The user responsible for approving the air bill.
        created_at (datetime): The date and time when the air bill was created.
    """
    CASE = (
        ('basic', 'basic'),
        ('replace', 'replace'),
        ('rent', 'rent'),
    )

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requester'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver',
        null=True,
        blank=True
    )
    request_case = models.CharField(
        max_length=10,
        choices=CASE
    )
    money_category = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    job_no = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    for_req = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    check_comment = models.TextField(
        null=True,
        blank=True
    )
    check_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='check_person',
        null=True,
        blank=True
    )
    approve_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='approve_person',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )


class DataBill(models.Model):
    """
    Represents a data bill entry in the system.

    Attributes:
        requester (User): The user who requested the bill.
        receiver (User, optional): The user who received the bill (if applicable).
        request_case (str): The type of request case, chosen from predefined options.
        money_category (str, optional): The category of money involved in the bill.
        job_no (str, optional): The job number associated with the bill.
        for_req (str, optional): The purpose of the request.
        check_comment (str, optional): Comments provided during checking.
        check_person (User, optional): The user responsible for checking the bill.
        approve_person (User, optional): The user responsible for approving the bill.
        created_at (datetime): The timestamp when the entry was created.
    """

    CASE = (
        ('basic', 'basic'),
        ('replace', 'replace'),
        ('rent', 'rent'),
    )

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requester',
        help_text='The user who requested the bill.'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver',
        null=True,
        blank=True,
        help_text='The user who received the bill (if applicable).'
    )
    request_case = models.CharField(
        max_length=10,
        choices=CASE,
        help_text='The type of request case, chosen from predefined options.'
    )
    money_category = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text='The category of money involved in the bill.'
    )
    job_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text='The job number associated with the bill.'
    )
    for_req = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text='The purpose of the request.'
    )
    check_comment = models.TextField(
        null=True,
        blank=True,
        help_text='Comments provided during checking.'
    )
    check_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='check_person',
        null=True,
        blank=True,
        help_text='The user responsible for checking the bill.'
    )
    approve_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='approve_person',
        null=True,
        blank=True,
        help_text='The user responsible for approving the bill.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='The timestamp when the entry was created.'
    )


class RelayBillItem(models.Model):
    """
    Represents an item within a relay bill, associating an asset with a bill and its quantity.
    """

    STATUS = (
        ('on_hand', 'on_hand',)
        ('replace', 'replace'),
        ('installed', 'installed'),
    )
    bill = models.ForeignKey(
        RelayBill,
        on_delete=models.CASCADE,
        related_name='bill_items',
        verbose_name='Bill',
        help_text='The relay bill associated with this item.'
    )
    asset = models.ForeignKey(
        StockItem,
        on_delete=models.CASCADE,
        related_name='bill_items',
        verbose_name='StockItem',
        help_text='The asset related to this bill item.'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Quantity',
        help_text='The quantity of the asset included in this bill item.'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS,
    )

    class Meta:
        verbose_name = 'Relay Bill Item'
        verbose_name_plural = 'Relay Bill Items'

    def __str__(self):
        return f'{self.quantity} x {self.asset.name} - Bill {self.bill.id}'


class SatelliteBillItem(models.Model):
    """
    Represents an item in a satellite bill.

    Each SatelliteBillItem is associated with a SatelliteBill and an StockItem.
    It also includes the quantity of the asset in the bill.
    """

    STATUS = (
        ('on_hand', 'on_hand',)
        ('replace', 'replace'),
        ('installed', 'installed'),
    )
    bill = models.ForeignKey(
        'SatelliteBill',
        on_delete=models.CASCADE,
        related_name='bill_items',
        help_text='The satellite bill this item belongs to.'
    )
    asset = models.ForeignKey(
        'StockItem',
        on_delete=models.CASCADE,
        related_name='bill_items',
        help_text='The asset associated with this item in the bill.'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text='The quantity of the asset in the bill item.'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS,
    )
    
    class Meta:
        verbose_name = 'Satellite Bill Item'
        verbose_name_plural = 'Satellite Bill Items'

    def __str__(self):
        return f'{self.quantity} x {self.asset.name} - Bill {self.bill.id}'


class FiberBillItem(models.Model):
    """
    Represents a single item in the FiberBill model.
    """

    STATUS = (
        ('on_hand', 'on_hand',)
        ('replace', 'replace'),
        ('installed', 'installed'),
    )
    bill = models.ForeignKey(
        'FiberBill',
        on_delete=models.CASCADE,
        related_name='bill_items',
        help_text='The bill to which this item belongs.'
    )

    asset = models.ForeignKey(
        'StockItem',
        on_delete=models.CASCADE,
        related_name='bill_items',
        help_text='The asset associated with this item.'
    )

    quantity = models.PositiveIntegerField(
        default=1,
        help_text='The quantity of the asset in this bill item.'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS,
    )

    class Meta:
        verbose_name = 'Fiber Bill Item'
        verbose_name_plural = 'Fiber Bill Items'

    def __str__(self):
        return f'{self.quantity} x {self.asset.name} - Bill {self.bill.id}'


class AirBillItem(models.Model):
    """
    Represents an item in an air bill.
    """

    STATUS = (
        ('on_hand', 'on_hand',)
        ('replace', 'replace'),
        ('installed', 'installed'),
    )
    bill = models.ForeignKey(
        AirBill,
        on_delete=models.CASCADE,
        related_name='bill_items',
        help_text="The air bill to which this item belongs."
    )
    asset = models.ForeignKey(
        StockItem,
        on_delete=models.CASCADE,
        related_name='bill_items',
        help_text="The asset associated with this item."
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="The quantity of the asset in this item."
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS,
    )

    class Meta:
        verbose_name = 'Air Bill Item'
        verbose_name_plural = 'Air Bill Items'

    def __str__(self):
        return f'{self.quantity} x {self.asset.name} - Bill {self.bill.id}'


class DataBillItem(models.Model):
    """
    Represents an item within a DataBill.

    Each DataBillItem corresponds to a specific asset included in a DataBill.
    """

    STATUS = (
        ('on_hand', 'on_hand',)
        ('replace', 'replace'),
        ('installed', 'installed'),
    )
    bill = models.ForeignKey(
        DataBill,
        on_delete=models.CASCADE,
        related_name='bill_items',
        help_text="The DataBill associated with this item."
    )
    asset = models.ForeignKey(
        StockItem,
        on_delete=models.CASCADE,
        related_name='bill_items',
        help_text="The asset associated with this item."
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="The quantity of the asset included in this item."
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS,
    )

    class Meta:
        verbose_name = 'Data Bill Item'
        verbose_name_plural = 'Data Bill Items'

    def __str__(self):
        return f'{self.quantity} x {self.asset.name} - Bill {self.bill.id}'
