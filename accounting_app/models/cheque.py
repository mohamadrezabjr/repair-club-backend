from django.db import models
from django.utils import timezone


class ChequeDirection(models.TextChoices):
    RECEIVED = ('received', 'دریافتی')   # چکی که از مشتری گرفته‌ایم
    ISSUED = ('issued', 'پرداختی')       # چکی که ما صادر کرده‌ایم


class ChequeStatus(models.TextChoices):
    PENDING = ('pending', 'در جریان')
    CLEARED = ('cleared', 'پاس شده')
    BOUNCED = ('bounced', 'برگشت خورده')
    CANCELLED = ('cancelled', 'باطل شده')


class Cheque(models.Model):
    """چک دریافتی یا پرداختی با تاریخ سررسید و وضعیت پاس شدن."""
    direction = models.CharField(
        choices=ChequeDirection.choices,
        max_length=10,
        verbose_name="نوع چک",
    )
    status = models.CharField(
        choices=ChequeStatus.choices,
        max_length=10,
        default=ChequeStatus.PENDING,
        verbose_name="وضعیت",
    )
    amount = models.BigIntegerField(verbose_name="مبلغ (تومان)")
    cheque_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="شماره چک")
    bank_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="بانک")
    counterparty = models.CharField(max_length=150, blank=True, null=True, verbose_name="طرف حساب")
    issue_date = models.DateField(null=True, blank=True, verbose_name="تاریخ صدور")
    due_date = models.DateField(verbose_name="تاریخ سررسید")
    cleared_at = models.DateField(null=True, blank=True, verbose_name="تاریخ پاس شدن")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "چک"
        verbose_name_plural = "چک‌ها"
        ordering = ['due_date']

    def __str__(self):
        return f"چک {self.amount:,} تومان — {self.get_status_display()}"

    @property
    def is_overdue(self):
        """چک در جریانی که تاریخ سررسیدش گذشته است."""
        return self.status == ChequeStatus.PENDING and self.due_date < timezone.localdate()
