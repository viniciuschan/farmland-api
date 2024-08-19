from decimal import Decimal

from django.db import models
from django.db.models import CharField, Count, F, Func, Sum
from django.db.models.functions import Cast


class FarmManager(models.Manager):
    def total_farms_data(self) -> dict:
        return self.aggregate(
            total_farms_count=Count("id"),
            total_farms_area=Cast(
                Sum(
                    F("total_area_hectares"),
                    default=Decimal("0.00"),
                ),
                output_field=CharField(),
            ),
            total_vegetation_area=Cast(
                Sum(
                    F("vegetation_area_hectares"),
                    default=Decimal("0.00"),
                ),
                output_field=CharField(),
            ),
            total_cultivable_area=Cast(
                Sum(
                    F("cultivable_area_hectares"),
                    default=Decimal("0.00"),
                ),
                output_field=CharField(),
            ),
        )

    def farms_per_state(self) -> dict:
        qs = self.values(state=F("location__state")).annotate(
            count=Count("id"),
            area=Cast(
                Sum(
                    F("total_area_hectares"),
                    default=Decimal("0.00"),
                ),
                output_field=CharField(),
            ),
        )
        return {
            item["state"]: {
                "total_count": item["count"],
                "total_area": item["area"],
            }
            for item in qs
        }

    def total_farms_per_cultivation(self) -> dict:
        class Unnest(Func):
            function = "unnest"
            template = "%(function)s(%(expressions)s)"

        total_cultivable_area = self.aggregate(
            total_cultivable_area=Sum(
                "cultivable_area_hectares",
                default=Decimal("0.00"),
            )
        )["total_cultivable_area"]

        qs = (
            self.annotate(cultivation=Unnest("cultivations"))
            .values("cultivation")
            .annotate(
                total_farms=Count("id"),
                area=Sum(F("cultivable_area_hectares"), default=Decimal("0.00")),
            )
        )

        return {
            item["cultivation"]: {
                "total_farms": item["total_farms"],
                "percentage_area": str(item["area"] / total_cultivable_area),
            }
            for item in qs
        }
