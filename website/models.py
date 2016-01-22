from django.db import models


class Order(models.Model):
    email = models.EmailField()
    cvcode = models.IntegerField("CV Code")
    expirem = models.IntegerField("Expire Month")
    expirey = models.IntegerField("Expire Year")
    cardnumber = models.CharField("Card Number", max_length=50)
    price = models.DecimalField("Price", max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email
