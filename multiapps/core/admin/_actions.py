"""
Admin actions to perform database queries in bulk at once
"""

# STDLIB LIBRARY
import logging

# DJANGO LIBRARY
from django.contrib import admin



logger = logging.getLogger(__name__)


@admin.action()
def force_to_apply_config(modeladmin, request, queryset):
  """
  Force to apply config immediately
  """
  modeladmin.model.cache_values(queryset)
