"""
This module helps to manage environment settings.
"""

# STDLIB LIBRARY
import logging
from os.path import exists

# THIRDPARTY LIBRARY
import environ



logger = logging.getLogger(__name__)


# base directory of project
BASE_DIR = environ.Path(__file__) - 3


env = environ.Env()

# Take environment variables from .env file
if exists(BASE_DIR("envs", "Prod.env")):
  env.read_env(BASE_DIR("envs", "Prod.env"))

# overwrite production environment variables to development environment variables.
if exists(BASE_DIR("envs", "Dev.env")):
  env.read_env(BASE_DIR("envs", "Dev.env"), overwrite=True)


try:
  # LOCALFOLDER LIBRARY
  from ._base import *
  logger.info('base settings imported')

except  ImportError or ModuleNotFoundError as e:
  logger.error('base settings not available')


if DEBUG:
  try:
    # LOCALFOLDER LIBRARY
    from .local import *
    logger.info('development settings imported')

  except ImportError or ModuleNotFoundError as e:
    logger.warning('development settings not available')

    try:
      # LOCALFOLDER LIBRARY
      from .prod import *
      logger.info('production settings imported')

    except  ImportError or ModuleNotFoundError as e:
      logger.error('production settings not available')

else:
  try:
    # LOCALFOLDER LIBRARY
    from .prod import *
    logger.info('production settings imported')

  except  ImportError or ModuleNotFoundError as e:
    logger.error('production settings not available')
