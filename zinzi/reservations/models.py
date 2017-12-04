from django.db import models

from members.models import User
from restaurants.models import ReservationInfo


# fixme
# class Reservation(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.PROTECT,
#     )
#     information = models.ForeignKey(
#         ReservationInfo,
#         on_delete=models.PROTECT,
#     )


class Payment(models.Model):
    # 고유번호
    imp_uid = models.CharField(max_length=50)
    merchant_uid = models.CharField(max_length=50)
    # 지불방법 및 pg사 정보
    pay_method = models.CharField(max_length=20)
    pg_provider = models.CharField(max_length=20)
    pg_tid = models.CharField(max_length=50)
    # 주문정보
    name = models.CharField(max_length=50)
    amount = models.IntegerField()
    cancel_amount = models.IntegerField()
    currency = models.CharField(max_length=5)
    status = models.CharField(max_length=10)
    paid_at = models.IntegerField()
    failed_at = models.IntegerField()
    cancelled_at = models.IntegerField()
    fail_reason = models.CharField(max_length=255, null=True, blank=True)
    cancel_reason = models.CharField(max_length=255, null=True, blank=True)
    # 주문자 정보
    buyer_name = models.CharField(max_length=10)
    buyer_email = models.CharField(max_length=30)
    buyer_tel = models.CharField(max_length=20)
