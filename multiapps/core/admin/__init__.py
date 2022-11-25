"""
Admin package of CoreAPP
"""

# LOCALFOLDER LIBRARY
from ._actions import force_to_apply_config
from ._admin import SettingAdmin



__all__ = [
  'SettingAdmin',
  'force_to_apply_config',
]
