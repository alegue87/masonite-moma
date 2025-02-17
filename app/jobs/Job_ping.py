
from app.models.IpRange import IpRange
from app.models.Nation import Nation
from app.models.Time import Time
import random
from ping3 import ping
#from multiprocess import Process

class Job_ping:
    def start(app, job_model):
        #print('Job_1, jobname ' + job_model.name)
        rangeList = IpRange.builder.where('key_nation', job_model.args['nation_key']).all()
        ipRange = rangeList[random.randrange(0, len(rangeList))]
        nation = Nation.builder.where('key', ipRange.key_nation).first()
        sstart = ipRange['start'].split('.')
        send = ipRange['end'].split('.')

        ips = [0,0,0,0]
        for i in range(0, 4):
            if sstart[i] != send[i]:
                ips[i] = [sstart[i], send[i]]
            else:
                ips[i] = sstart[i]

        ip = []
        for ott in ips:
            if type(ott) == str:
                ip.append(ott)
            else:
                ip.append(str(random.randrange(int(ott[0]), int(ott[1]))))


        ip = '.'.join(ip)
        ret = ping(ip, unit='s', timeout=1)
        if ret == None or ret == False:
            pass
            #print('Timeout or unreachable')
        else:
            try:
                print(nation.name+' :', ret)
                Time.create({
                    'key_nation': nation.key,
                    'ms': float(ret),
                })
            except Exception as e:
                from datetime import datetime as dt
                file = open('./storage/log/'+nation.key+'.log', 'a')
                now = dt.now()
                tm = now.strftime("%d/%m/%Y %H:%M:%S")
                file.write(tm)
                file.close()
        
