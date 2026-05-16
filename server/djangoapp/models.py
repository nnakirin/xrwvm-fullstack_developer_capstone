from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

# Модель для марки автомобіля


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country_of_origin = models.CharField(
        max_length=50,
        blank=True,
        null=True)  # Додаткове поле за бажанням

    def __str__(self):
        return self.name  # Повертає назву марки


# Модель для конкретної моделі автомобіля
class CarModel(models.Model):
    # Зв'язок Багато-до-Одного (Багато моделей до однієї марки)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    # Поле ID дилера, що посилається на базу Cloudant
    dealer_id = models.IntegerField()

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('HATCHBACK', 'Hatchback'),
    ]
    type = models.CharField(
        max_length=10,
        choices=CAR_TYPES,
        default='SUV'
    )

    # Рік випуску з обмеженнями від 2015 до 2023
    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )

    def __str__(self):
        # Виводить марку та модель разом
        return f"{self.car_make.name} {self.name}"
