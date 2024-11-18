#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : utils.py
# Author            : lu5her <lu5her@mail>
# Date              : Wed Sep, 20 2023, 10:18 263
# Last Modified Date: Wed Sep, 20 2023, 10:30 263
# Last Modified By  : lu5her <lu5her@mail>
import os
from io import BytesIO
from typing import Any, Dict, List

from django.template.loader import get_template
from xhtml2pdf import pisa


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL  # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL  # Typically /media/
    mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception("media URI must start with %s or %s" % (sUrl, mUrl))
    return path


def generate_pdf(data: Dict[str, Any], template_path: str) -> bytes:
    template = get_template(template_path)
    html = template.render(data)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result, encoding="utf-8")
    if not pdf.err:
        return result.getvalue()

    result.close()
    return None
