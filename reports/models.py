from django.db import models


class Reports(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Reports"

class Dashboard_Report(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"