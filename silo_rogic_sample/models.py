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
    should_compare_with_others = models.BooleanField("他サイロとの比較対象", default=False)

    def __str__(self):
        return self.silo_name

    class Meta:
        ordering = ["silo_name"]
        verbose_name = "サイロマスタ"
        verbose_name_plural = "サイロマスタ"
        db_table = "silo_master"

    def clean(self):
        if self.should_calculate and not hasattr(self, "formula"):
            raise ValidationError("should_calculate=True の場合、SiloFormula を作成してください。")
        if self.should_compare_with_others and not self.compare_with_silo.exists():
            raise ValidationError("should_compare_with_others=True の場合、SiloCompare を作成してください。")



class SiloFormula(models.Model):
    """
    SiloMasterに対応した計算式の情報（should_calculate=Trueの場合のみ存在）

    サイロに対して何か計算式がある場合、こちらに登録する
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


class SiloCompare(models.Model):
    """
    他サイロとの比較対象の情報

    比較するサイロがある場合、こちらに登録しておく
    """
    source_silo = models.ForeignKey(SiloMaster, verbose_name="比較元サイロ", on_delete=models.CASCADE, related_name="comparisons_as_source")
    target_silo = models.ForeignKey(SiloMaster, verbose_name="比較先サイロ", on_delete=models.CASCADE, related_name="comparisons_as_target")


    def __str__(self):
        return f"Compare {self.silo.silo_name} with {self.compare_with_silo.silo_name}"

    class Meta:
        verbose_name = "サイロ比較"
        verbose_name_plural = "サイロ比較"
        db_table = "silo_compare"