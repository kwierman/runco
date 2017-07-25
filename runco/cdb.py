
import psycopg2
import psycopg2.extras
import json


class ConfigDB(object):

  def __init__(self, config):
    raise NotImplementedError("ConfigDB Does not work outside of the DAQ area")
    self.conn = psycopg2.connect(host=config['host'],
                                 database=config['db'],
                                 user=config['user'],
                                 password=config['pass'])
    psycopg2.extras.register_hstore(__connection)
    self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

  def get_config_lookup(self):
    self.cursor.execute('SELECT subconfigtype, subconfigname from configlookup;')
    result = self.cursor.fetchall()
    cache = {}
    for i in result:
      cache[i[0]] = i[1]
      cache[i[1]] = i[0]
    return cache

  def get_subconfig(self, tablename, configid):
    query = 'select * from ' + tablename + ' where configid = %s;'
    self.cursor.execute(query)
    configrow = self.cursor.fetchone()
    res = configrow['parameters'].copy()
    paramsets = configrow['parametersets']
    for p in paramsets:
      subresult = self.get_subconfig(p, paramsets[p])
      res[p] = subresult
    return res

  def get_config(self,run):
    result={}

    try:
      self.cursor.execute('SELECT configid from mainrun where runnumber={}'.format(run))
      configid = self.cursor.fetchone()[0]
      self.cursor.execute('SELECT configname,subconfigtype,subconfigid from mainconfigtable where configid={}'.format(configid))
      subconfigs = self.cursor.fetchall()
      result['configname'] = subconfigs[0]['configname']
      result['configid']   = configid
      lookup = self.config_lookup()
      for subconfig in subconfigs:
          tablename = lookup[subconfig['subconfigtype']]
          result[tablename]=get_subconfig(tablename,subconfig['subconfigid'])
      return result
    except:
      return {}

  def has_asic(self, result):
    """Return true if the dictionary result has got asic info"""
    if not ("ASIC" in result): return False

    asic = result['ASIC']
    if(len(asic)<1): return False;

    for key, FT in asic.iteritems():
        if FT["reconfigure"] == "false": return False

    return True

  def get_asic_config(self, run):
    runnumber = int(run.run)
    arun = runnumber

    while(arun>0):
        result = self.get_config(arun)
        if(self.has_asic(result)): break
        arun = arun - 1

    if(arun==0):
        return False

    run.run_data['configdb_asic_run'] = arun
    run.run_data['configdb_asic_config'] = result
    return True

  def analyze(self, run):
    runnumber = int(run.run)
    result= self.get_config(runnumber)
    run.run_data['configdb'] = result
    self.get_asic_config(run)
