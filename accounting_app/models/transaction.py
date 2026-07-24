from django.db import models


class TransactionKind(models.TextChoices):
    INCOME = ('income', 'درآمد')
    EXPENSE = ('expense', 'هزینه')


class PaymentMethod(models.TextChoices):
    CASH = ('cash', 'نقدی')
    CARD = ('card', 'کارت‌خوان / کارت به کارت')
    TRANSFER = ('transfer', 'انتقال بانکی')
    CHEQUE = ('cheque', 'چک')


class TransactionCategory(models.Model):
    """دسته‌بندی تراکنش‌های مالی (مثلاً حقوق، اجاره، خرید قطعه)."""
    name = models.CharField(max_length=100, verbose_name="عنوان دسته")
    kind = models.CharField(
        choices=TransactionKind.choices,
        max_length=10,
        verbose_name="نوع",
    )
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "دسته تراکنش"
        verbose_name_plural = "دسته‌های تراکنش"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'kind'],
                name='unique_category_name_per_kind',
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.get_kind_display()})"


class Transaction(models.Model):
    """یک تراکنش مالی دستی — درآمد یا هزینه."""
    kind = models.CharField(
        choices=TransactionKind.choices,
        max_length=10,
        verbose_name="نوع",
    )
    title = models.CharField(max_length=150, verbose_name="عنوان")
    amount = models.BigIntegerField(verbose_name="مبلغ (تومان)")
    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        verbose_name="دسته",
    )
    payment_method = models.CharField(
        choices=PaymentMethod.choices,
        max_length=20,
        default=PaymentMethod.CASH,
        verbose_name="روش پرداخت",
    )
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    occurred_at = models.DateField(verbose_name="تاریخ وقوع")
    visit = models.ForeignKey(
        "garage_app.Visit",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        verbose_name="ویزیت مرتبط",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"
        ordering = ['-occurred_at', '-created_at']

    def __str__(self):
        return f"{self.title} — {self.amount:,} تومان"
