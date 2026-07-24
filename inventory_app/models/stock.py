from django.db import models
from inventory_app.models.product import Product


class StockEntry(models.Model):
    """
    ورود کالا به انبار (شارژ موجودی / خرید).
    با ثبت هر رکورد، موجودی محصول افزایش می‌یابد و بهای خرید نگهداری می‌شود
    تا در گزارش هزینه‌های حسابداری لحاظ شود.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_entries',
        verbose_name="کالا",
    )
    quantity = models.PositiveIntegerField(verbose_name="تعداد")
    unit_cost = models.BigIntegerField(verbose_name="بهای خرید هر واحد (تومان)")
    supplier = models.CharField(max_length=150, blank=True, null=True, verbose_name="تأمین‌کننده")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ورود کالا به انبار"
        verbose_name_plural = "ورودی‌های انبار"
        ordering = ['-created_at']

    @property
    def total_cost(self):
        return self.unit_cost * self.quantity

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"
