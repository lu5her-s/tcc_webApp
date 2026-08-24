from typing import Any, Dict

from django.conf import settings
from django.template.loader import get_template
from weasyprint import HTML


def generate_pdf(data: Dict[str, Any], template_path: str) -> bytes:
    template = get_template(template_path)
    html = template.render(data)
    return HTML(string=html, base_url=str(settings.BASE_DIR)).write_pdf()
