from django.db import models


class Order(models.Model):
    email = models.EmailField()
    transaction_id = models.CharField("Transaction ID", max_length=120)
    price = models.DecimalField("Price", max_digits=5, decimal_places=2)
    card_type = models.CharField("Card Type", max_length=120)
    last_4 = models.CharField("Last 4 Digits", max_length=4, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email
