from django.db import models
from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    middle_name = models.CharField('Отчество', max_length=50,
                                   blank=True, null=True)
    speciality = models.CharField('Специальность', max_length=50,
                                  blank=True, null=True)
    department = models.ManyToManyField('drugs.department', blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
