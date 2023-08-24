from django.db import models

class Order(models.Model):
    order_name = models.CharField(max_length=255)
    date_due = models.DateField()
    time_due = models.TimeField()
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_due', 'time_due', '-id']
