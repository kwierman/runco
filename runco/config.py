# The configuration of runco uses yaml
import json
import os
import logging


class Config:
  logger = logging.getLogger('config')
  config_dir = '.config'
  config_name = 'runco.json'

  def __init__(self, filepath=None):
    if filepath is None:
      self.logger.info("Using default config")
      self.initialize_default()
    else:
      self.initialize_custom(filepath)

  @property
  def default_path(self):
    home = os.environ['HOME']
    config_path = os.path.join(home, self.config_dir)
    if not os.path.isdir(config_path):
      os.mkdir(config_path)
    return os.path.join(config_path, self.config_name)

  def initialize_default(self):
    path = self.default_path
    if os.path.exists(path):
      with open(path,'r') as input_file:
        try:
          self.data = json.loads(input_file.read())
          return
        except json.JSONDecodeError as e:
          self.logger.warning('Could not parse config: {}'.format(path))
          self.logger.warning(e)
    self.generate_config()
    self.initialize_default()

  def generate_config(self):
    self.logger.info("Generating new config")
    c = default_config()
    s = json.dumps(c)
    self.logger.info(s)
    output = open(self.default_path, 'w')
    output.write(s)
    output.close()
    os.chmod(self.default_path, 700)
    self.logger.info("Closed new config")
    self.logger.info("New config generated. Now please adjust values in: {}".format(self.default_path))

def default_config():
  return {'slowcontrols':{'url':'', 'user':'','pass':'','port':'', "db":"" },
          'ecl':{'url':'', 'user':'','pass':'' } }
