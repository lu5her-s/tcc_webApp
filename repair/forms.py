from django import forms

from repair.models import Repair


# repair form for save data to model
class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = (
            "comment",
            "cost",
        )
        labels = {
            "comment": "รายละเอียด",
            "cost": "ค่าใช้จ่าย",
        }
