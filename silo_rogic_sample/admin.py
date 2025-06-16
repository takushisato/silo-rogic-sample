from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from .models import SiloMaster, SiloFormula


class SiloFormulaInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            silo_master = form.instance.silo if form.instance.pk else self.instance
            if silo_master.should_calculate and form.cleaned_data.get('DELETE', False):
                raise ValidationError("should_calculate=True の場合、SiloFormula を削除できません。")
        if self.instance.should_calculate and not any(form.cleaned_data and not form.cleaned_data.get('DELETE', False) for form in self.forms):
            raise ValidationError("should_calculate=True の場合、SiloFormula を1つ登録してください。")


class SiloFormulaInline(admin.StackedInline):
    model = SiloFormula
    formset = SiloFormulaInlineFormSet
    extra = 0
    max_num = 1



@admin.register(SiloMaster)
class SiloMasterAdmin(admin.ModelAdmin):
    list_display = ("silo_name", "should_calculate", "disabled", "max_weight")
    inlines = [SiloFormulaInline]
