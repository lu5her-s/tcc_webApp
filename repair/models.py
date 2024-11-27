from ckeditor.fields import RichTextField
from django.db import models
from inform.models import Inform

# Create your models here.


class Repair(models.Model):
    inform = models.ForeignKey(
        Inform, on_delete=models.CASCADE, related_name="inform_repair"
    )
    comment = RichTextField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inform.pk} - {self.inform.status}"
