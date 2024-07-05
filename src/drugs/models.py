from django.db import models
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from loguru import logger


class Shipment(models.Model):
    drug = models.ForeignKey('drugs.Drug', on_delete=models.PROTECT)
    provider = models.ForeignKey('drugs.Firm', on_delete=models.PROTECT, related_name='provided_shipment')
    producer = models.ForeignKey('drugs.Firm', on_delete=models.PROTECT, related_name='produced_shipment')
    document = models.CharField(max_length=100)
    date_of_comming = models.DateField()
    date_of_run_out = models.DateField(blank=True, null=True)
    use_by_date = models.DateField()
    serial_number = models.CharField(max_length=100)
    initial_amount = models.IntegerField()
    current_amount = models.IntegerField(blank=True, null=True)# TODO delete blsnk/null
    undistributed_amount = models.IntegerField(blank=True, null=True)# TODO delete blsnk/null
    prise_for_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.drug.name

    @property
    def editable(self):
        if self.initial_amount == self.undistributed_amount:
            return True
        else:
            return False

    @property
    def total_price(self):
        return Decimal(self.current_amount) * Decimal(self.prise_for_unit)

    @property
    def is_expired(self):
        if self.use_by_date < (timezone.now().date() - timedelta(days=30)):
            return "True"
        elif self.use_by_date < timezone.now().date():
            return "Soon"
        else:
            return "False"

    # TODO make saving initial current amount in the same way
    def save(self, *args, **kwargs):
        if self.undistributed_amount is None:
            self.undistributed_amount = self.initial_amount
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'

    @staticmethod
    def get_shipments(mode=None):
        queryset = Shipment.objects.all().select_related('drug', 'drug__unit', 'producer', 'provider')
        if mode is None:
            queryset = queryset.filter(current_amount__gt=0)
        elif mode == 'show_run_out':
            queryset = queryset.filter(current_amount=0)
        return queryset


class Drug(models.Model):
    name = models.CharField(max_length=100)
    unit = models.ForeignKey('drugs.DrugUnit', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Препарат'
        verbose_name_plural = 'Препараты'


class Firm(models.Model):
    name = models.CharField(max_length=100)
    FIRM_TYPES = (
        ('producer', 'producer'),
        ('provider', 'provider'),
    )
    firm_type = models.CharField(
        max_length=8,
        choices=FIRM_TYPES
        )
    
    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Фирма'
        verbose_name_plural = 'Фирмы'


class DrugUnit(models.Model):
    name  = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


class Movement(models.Model):
    shipment = models.ForeignKey('drugs.Shipment', on_delete=models.PROTECT)
    department = models.ForeignKey('drugs.Department', on_delete=models.PROTECT)
    amount = models.IntegerField()
    date = models.DateField()
    employee = models.ForeignKey('profiles.Employee', on_delete=models.PROTECT)
    direction = models.ForeignKey('Direction', on_delete=models.PROTECT)

    @property
    def total_price(self):
        return Decimal(self.shipment.prise_for_unit) * Decimal(self.amount)

    class Meta:
        verbose_name = 'Движение'
        verbose_name_plural = 'Движения'


class Distribution(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.PROTECT)
    department = models.ForeignKey('Department', on_delete=models.PROTECT)
    initial_amount = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.initial_amount is None:
            self.initial_amount = self.amount
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Распределение'
        verbose_name_plural = 'Распределения'


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отделение'
        verbose_name_plural = 'Отделения'


class Direction(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'


class WriteOff(models.Model):
    shipment = models.ForeignKey('Shipment', on_delete=models.PROTECT)
    date = models.DateField()
    amount = models.PositiveIntegerField()
    reason = models.CharField(max_length=250)

    @property
    def total_price(self):
        return Decimal(self.shipment.prise_for_unit) * Decimal(self.amount)

    class Meta:
        verbose_name = 'Списание'
        verbose_name_plural = 'Списания'
