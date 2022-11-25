"""
ModelAdmin for Admin interface
"""

# STDLIB LIBRARY
import logging

# DJANGO LIBRARY
from django.contrib import admin

# FIRSTPARTY LIBRARY
from core.models import Setting

# LOCALFOLDER LIBRARY
from ._actions import force_to_apply_config



logger = logging.getLogger(__name__)


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
  """
  Admin interface for Setting model on sql
  """

  logger = logging.LoggerAdapter(logger)

  list_display = ('key', 'value', 'description')
  search_fields = ('key', 'value', 'description')

  actions = [force_to_apply_config]

  def has_add_permission(self, request):
    return False

  def has_delete_permission(self, request, obj=None):
    return False

  def save_model(self, request, obj, form, change):
    if form.has_changed():
      if 'value' in form.changed_data:
        self.model.set_value(obj.key, obj.value)
        self.logger.debug('UPDATE "{}" from {} to {}', obj.key, form.initial['value'], obj.value)
      return super().save_model(request, obj, form, change)
