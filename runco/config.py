# The configuration of runco uses yaml
import yaml
import os
import logging


class Config:
  logger = logging.getLogger('config')
  config_dir = '.config'
  config_name = 'runco.yaml'

  def __init__(filepath):
    if filepath is None:
      self.logger.info("Using default config")
      self.initialize_default()
    else:
      self.initialize_custom(filepath)

  @property
  def default_path(self):
    home = os.environ['HOME']
    config_path = os.path.join(home,config_dir)
    return os.path.join(config_path, config_name)

  def initialize_default(self):
    path = self.default_path
    if os.path.exists(path):
      with open(path) as input_file:
        try:
          self.data = yaml.load(input_file.read())
          return
        except yaml.YAMLError:
          self.logger.warning('Could not parse config: {}'.format(path))
    self.generate_config()
    self.initialize_default()


def default_config():
  return {'slowcontrols':{'url':'', 'username':'','pass':'','port':'' },
          'ecl':{'url':'', 'username':'','pass':'' } }
