import psycopg2
import psycopg2.extras
import json, sys
from datetime import datetime


class BeamDB:
    _cursor = None
    _connection = None
    _cached_config_lookup = None

    def __init__(self,config):
        self.conn = psycopg2.connect(host=config['host'],
                                    database=config['db'],
                                    user=config['user'],
                                    password=config['pass'])
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)        

    def get_beamdata(self, run):
        runnumber = int(run.run)
        self.cursor.execute("select smpl_time from sample where float_val = {} and channel_id = (select channel_id from channel where name={}) order by smpl_time limit 1;".format(run,"uB_DAQStatus_DAQX_runcontrol/current_run"))
        runtime = self.cursor.fetchone()[0]
        self.cursor.execute("select smpl_time from sample where float_val = {} and channel_id = (select channel_id from channel where name={}) order by smpl_time limit 1;".format(run+1,"uB_DAQStatus_DAQX_runcontrol/current_run"))
        nextruntime = self.cursor.fetchone()[0]
        result = {}
        for name in config.slomon['devices']:
            self.cursor.execute('select channel_id,descr from channel where name = %s',(name,))
            row = self.cursor.fetchone()
            channel_id = row['channel_id']
            descr      = row['descr']

            self.cursor.execute('select prec,unit from num_metadata where channel_id = %s',(channel_id,))
            row = self.cursor.fetchone()
            prec = None
            unit = None
            if(row):
                prec = row['prec']
                unit = row['unit']

            query = ("select "
                " count(float_val) as cnt, "
                " max(float_val) as max, "
                " min(float_val) as min, "
                " avg(float_val) as mean, "
                " stddev(float_val) as rms "
                " from sample where channel_id = %s and smpl_time > %s and smpl_time < %s;")
            self.cursor.execute(query,(channel_id,run.start,run.stop))
            data = self.cursor.fetchone()
            item = {
                'name': name,
                'desc': descr,
                'channel_id' : channel_id,
                'count': data['cnt'],
                'mean': data['mean'],
                'min': data['min'],
                'max': data['max'],
                'rms': data['rms']
            }
            if(prec is not None) : item['prec'] = prec
            if(unit is not None) : item['unit'] = unit
            print json.dumps(item)
            result[name] = item

        run.run_data['slomon'] = result
