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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.should_calculate and not hasattr(self, "formula"):
            raise ValidationError("should_calculate=True の場合、SiloFormula を作成してください。")


class SiloFormula(models.Model):
    """
    SiloMasterに対応した計算式の情報（should_calculate=Trueのときのみ存在）
    """
    silo = models.OneToOneField(SiloMaster, on_delete=models.CASCADE, related_name="formula")
    formula_text = models.TextField("計算式の内容", blank=True, null=True)
    description = models.CharField("説明", max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Formula for {self.silo.silo_name}"

    class Meta:
        verbose_name = "サイロ計算式"
        verbose_name_plural = "サイロ計算式"
        db_table = "silo_formula"