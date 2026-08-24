from django.db import models
from django_prose_editor.fields import ProseEditorField

from inform.models import Inform

# Create your models here.

PROSE_EXTENSIONS = {
    "Bold": True,
    "Italic": True,
    "Strike": True,
    "Underline": True,
    "HardBreak": True,
    "BulletList": True,
    "OrderedList": True,
    "ListItem": True,
    "Link": True,
    "History": True,
}


class Repair(models.Model):
    inform = models.ForeignKey(
        Inform, on_delete=models.CASCADE, related_name="inform_repair"
    )
    comment = ProseEditorField(
        extensions=PROSE_EXTENSIONS, sanitize=True, null=True, blank=True
    )
    cost = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inform.pk} - {self.inform.status}"
