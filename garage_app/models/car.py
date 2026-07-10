from django.db import models
from auth_app.models import User
from django.core.validators import MaxValueValidator

class CarModel(models.Model):
    class TransmissionTypeChoices(models.TextChoices):
        AUTO = ('auto', 'اتومات')
        MANUAL = ('man', 'دستی')

    make = models.CharField(null=True, blank=True, max_length=50)
    model = models.CharField(max_length=50)
    model_year = models.IntegerField(null=True, blank=True)
    transmission_type = models.CharField(choices=TransmissionTypeChoices.choices, max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.model}'

class Car(models.Model):
    PLATE_LETTERS = [
        ("الف", "الف"),
        ("ب", "ب"),
        ("پ", "پ"),
        ("ت", "ت"),
        ("ث", "ث"),
        ("ج", "ج"),
        ("د", "د"),
        ("س", "س"),
        ("ص", "ص"),
        ("ط", "ط"),
        ("ع", "ع"),
        ("ق", "ق"),
        ("ل", "ل"),
        ("م", "م"),
        ("ن", "ن"),
        ("و", "و"),
        ("ه", "ه"),
        ("ی", "ی"),
    ]
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True, blank=True)
    manufacturing_year = models.IntegerField(null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_visit_date = models.DateTimeField(null=True, blank=True)
    last_mileage = models.IntegerField(null=True, blank=True)

    plate_first = models.PositiveIntegerField(validators=[MaxValueValidator(99)])
    plate_letter = models.CharField(choices=PLATE_LETTERS, max_length=4)
    plate_second = models.PositiveIntegerField(validators=[MaxValueValidator(999)])
    plate_region = models.PositiveIntegerField(validators=[MaxValueValidator(99)])

    @property
    def plate_number(self):
        return f'{self.plate_first:02d}{self.plate_letter}{self.plate_second:03d}{self.plate_region:02d}'

    def is_in_garage(self):
        return self.visits.exclude(status__in=['cancelled', 'delivered']).exists()
        
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'plate_first',
                    'plate_letter',
                    'plate_second',
                    'plate_region',
                ],
                name='unique_plate_number'
            )
        ]