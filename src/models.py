import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from src.constants import BrazilianState, CultivationType, DocumentType
from src.validators import DocumentValidator


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        abstract = True


class Farmer(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100)
    document_type = models.CharField(max_length=4, choices=[(item.name, item.value) for item in DocumentType])
    document_value = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        validator = DocumentValidator(self.document_type)
        self.document_value = validator.clean_punctuations(self.document_value)
        return super().save(*args, **kwargs)


class Location(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=[(item.name, item.value) for item in BrazilianState])

    def __str__(self):
        return f"{self.state} - {self.city}"


class Farm(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    total_area_hectares = models.DecimalField(max_digits=10, decimal_places=2)
    cultivable_area_hectares = models.DecimalField(max_digits=10, decimal_places=2)
    vegetation_area_hectares = models.DecimalField(max_digits=10, decimal_places=2)
    cultivations = ArrayField(
        models.CharField(max_length=100, choices=[(item.name, item.value) for item in CultivationType]),
        default=list,
    )

    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
