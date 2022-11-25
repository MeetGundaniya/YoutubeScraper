"""
Models for Storing data on sql
"""

# DJANGO LIBRARY
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _



def validate_upper_case(key_text):
  if not key_text.isupper():
    raise ValidationError(
      _(f'all character of "{key_text}" must be capital')
    )


class Setting(models.Model):
  """
  Store ScraperApp configuration on sql
  """
  __cache = {}

  key = models.CharField(unique=True, max_length=128, validators=[validate_upper_case])
  value = models.CharField(max_length=128)
  description = models.TextField()

  class Meta:
    verbose_name = 'Settings'
    ordering = ('key',)

  def __repr__(self):
    return f'<Setting: key={self.key}, value={self.value}>'

  def __str__(self):
    return f'Setting(key={self.key})'

  @classmethod
  def get_value(cls, key):
    try:
      value = cls.__cache[key]
    except KeyError:
      value = cls.objects.get(key).value
      cls.set_value(key, value)
    return value

  @classmethod
  def set_value(cls, key, value):
    cls.__cache[key] = value

  @classmethod
  def cache_values(cls, queryset=None):
    queryset = queryset or cls.objects
    cls.__cache.update({key:val for key,val in queryset.values_list('key', 'value')})
