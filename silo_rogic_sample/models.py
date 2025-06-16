from django.db import models

class SiloMaster(models.Model):
    """
    should_calculate: 計算対象になるかを判定するフラグ
    """
    silo_name = models.CharField("サイロNo", max_length=50)
    disabled = models.BooleanField("直接入庫対象外", default=False)
    inbound_max_weight = models.IntegerField("最大入庫量")
    max_weight = models.IntegerField("最大容量")
    should_calculate = models.BooleanField("計算対象", default=False)

    def __str__(self):
        return self.silo_name

    class Meta:
        ordering = ["silo_name"]
        verbose_name = "サイロマスタ"
        verbose_name_plural = "サイロマスタ"
        db_table = "silo_master"