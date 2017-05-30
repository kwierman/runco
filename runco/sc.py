import psycopg2
import logging
import datetime


class SlowControls:
    logger = logging.getLogger("sc")
    def __init__(self):
        self.connection = psycopg2.connect(host="ifdbrep2.fnal.gov",
                                           user="smcreader",
                                           port=5438,
                                           database="slowmoncon_archive")
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT channel_id,name from channel;")
        rows = self.cur.fetchall()
        self.channel_name_by_id = d = dict( (int(r[0]),r[1]) for r in rows )
        self.channel_id_by_name = dict( (i[1],i[0]) for i in d.items() )
        self.channel_ids = d.keys()
        self.channel_ids.sort()
        self.nchannel = len(self.channel_ids)
        print self.channel_name_by_id

    def query_timebinned_data(self,channel_id, dt_s, tstart, tstop,
                              max_severity =3):

        if type(tstart) == int:
             tstart = datetime.datetime.fromtimestamp(tstart)
        if type(tstop) == int:
             tstop = datetime.datetime.fromtimestamp(tstop)
        query = """SELECT channel_id,                                                                                                                                                                               
floor(extract(epoch from smpl_time)/%s) as tbin,                                                                                                                                                                    
avg(float_val) FROM sample                                                                                                                                                                                          
WHERE smpl_time >= %s and smpl_time < %s and channel_id = %s                                                                                                                                                        
and severity_id <= %s                                                                                                                                                                                               
GROUP BY channel_id,tbin ORDER BY tbin;"""
        self.cur.execute(query, (dt_s, tstart, tstop, channel_id, max_severity))
