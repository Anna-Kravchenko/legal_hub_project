from django.db import models
from .telegram_utils import send_order_notification
import logging

logger = logging.getLogger("bureau")

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services'
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    completion_time = models.CharField(
        max_length=100,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Review(models.Model):
    client_name = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_name


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    # source_language = models.ForeignKey(
    #     Language,
    #     on_delete=models.CASCADE,
    #     related_name='source_orders'
    # )
    # target_language = models.ForeignKey(
    #     Language,
    #     on_delete=models.CASCADE,
    #     related_name='target_orders'
    # )
    is_urgent = models.BooleanField(
        default=False,
        verbose_name="Термінове замовлення"
    )
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
        upload_to='orders/',
        blank=True,
        null=True
    )
    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            try:
                send_order_notification(self)
                logger.info("Telegram notification sent for order %s", self.id)
            except Exception as e:
                # print("Telegram error:", e)
                logger.error("Telegram notification error for order %s: %s", self.id, e)


    def __str__(self):
        return f'Order #{self.id} - {self.client.name}'