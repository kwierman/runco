import pytz
from datetime import datetime
import json

# Hack to get datetime objects to serialize into json                                                                                                                                                               
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        # change to UTC, then print. Keeps it portable.                                                                                                                                                             
        serial = obj.astimezone(pytz.utc).isoformat()
        return serial
    raise TypeError ("Type not serializable")

def parse_iso(s,the_tzinfo =pytz.utc):
    # strip Z:                                                                                                                                                                                                      
    s = re.sub('Z$','', s)
    # strip tz if UTC                                                                                                                                                                                               
    s = re.sub('\+00:00$','', s)
    # If non-utc, this will throw an error below                                                                                                                                                                    
    ss = re.split('\.',s)
    s = ss[0] # first part                                                                                                                                                                                          
    t = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")  # assumes NO timezone info                                                                                                                                       
    if(len(ss)>1):
        frac = '0.' + ss[1]
        t = t + timedelta(seconds=float(frac))

    return the_tzinfo.localize(t)

kvalid_start = datetime(2015,1,1,tzinfo=pytz.utc);
kvalid_stop  = datetime(2050,1,1,tzinfo=pytz.utc);

def time_is_valid(t):
    return (t > kvalid_start) and (t < kvalid_stop)


class Run(object):
    def __init__(self,inrun):
        self.run = int(inrun)
        self.start = pytz.utc.localize(datetime.max)
        self.stop  = pytz.utc.localize(datetime.min)
        self.num_events = 0
        self.run_data  = {}
        self.subrun_data  = {}


    def expand_stop_time(self,t,tzinfo=pytz.utc):
        print "Examining stop time " + str(t)
        if(not isinstance(t,datetime)): t = parse_iso(t,tzinfo)
        t = t.astimezone(pytz.utc)
        if(time_is_valid(t) and t > self.stop):
            print "New stop time estimate: " + str(t)
            self.stop = t

    def expand_start_time(self,t,tzinfo=pytz.utc):
        print "Examining start time " + str(t)
        print t
        if(not isinstance(t,datetime)): t = parse_iso(t,tzinfo)
        t = t.astimezone(pytz.utc)
        if(time_is_valid(t) and  t < self.start):
            print "New start time estimate: " + str(t)
            self.start = t;

    def expand_time(self,t):
        self.expand_start_time(t)
        self.expand_stop_time(t)


    def subrunData(self,index):
        if not(index in self.subrun_data):
            self.subrun_data[index] ={}
        return self.subrun_data[index]

    def last_subrun(self):
        """ Return the number of the last subrun that we have data for"""
        subruns = self.subrun_data.keys()
        subruns.sort(key=int)
        return int(subruns[-1])

    def filename(self):
        return config.data_directory + "/run_"+str(self.run).zfill(8)+".json";

    def __str__(self):
        s = ""
        s += " run:        %s\n" % self.run
        s += " start:      %s\n" % self.start
        s += " stop:       %s\n" % self.stop
        s += " num+events: %s\n" % self.num_events
        subruns = self.subrun_data.keys() # list of subruns I have data for                                                                                                                                         
        subruns.sort(key=int)
        s += " subruns:    %s\n" % ' '.join(str(sr) for sr in subruns) # convert to string list of string ints                                                                                                      
        s += " main data:  \n"
        s +=json.dumps( self.run_data, indent=4, default=json_serial )

        for sr in subruns:
            s += "\nSubrun %s:\n" % sr
            s += json.dumps( self.subrunData(sr), indent=4 , default=json_serial)
        # s += "\nFirst subrun data:\n"                                                                                                                                                                             
        # s += json.dumps( self.subrunData(0), indent=4 )                                                                                                                                                           
        # last = self.last_subrun()                                                                                                                                                                                 
        # s += "\nLast subrun data: %s\n" % last                                                                                                                                                                    
        # s += json.dumps( self.subrunData(self.last_subrun()), indent=4 )     

    def save(self):
        data ={
            'header' : {
              'run':   self.run,
              'start': self.start,
              'stop' : self.stop,
              'num_events' :    self.num_events,
            },
            'run_data': self.run_data,
            'subrun_data': self.subrun_data
        }

        file = open( self.filename(), "w+")
        json.dump(data, file,  default=json_serial)
        file.close()


    def load(self):
        data = None
        try:
            file = open( self.filename(), "r+")
            data = json.load(file)
        except:
            print "No file " + self.filename() + " exists yet"
            return

        file.close()

        self.start              = parse_iso(data['header']['start'])
        self.stop               = parse_iso(data['header']['stop'] )
        self.num_events         = data['header']['num_events']
        print "Read file for run " + str(self.run)
        print "            start " + str(self.start)
        print "             stop " + str(self.stop)

        self.run_data = data['run_data']
        self.subrun_data = data['subrun_data']

