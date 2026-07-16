from django.db import models


class StaffRole(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="عنوان نقش")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "نقش"
        verbose_name_plural = "نقش‌ها"

    def __str__(self):
        return self.name


class Staff(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="نام خانوادگی")
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="شماره تماس")
    role = models.ForeignKey(StaffRole, on_delete=models.SET_NULL, null=True, blank=True, related_name="staff_members", verbose_name="نقش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "سرویس‌کار"
        verbose_name_plural = "سرویس کاران"

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}".strip()
