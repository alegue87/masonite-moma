from datetime import datetime as dt
from time import sleep
class Job_1:
    def start(app, job_model):
        t = dt.now()
        print('Job_1, jobname ' + job_model.name + ' st1 ', t.strftime("%H:%M:%S.%fZ"))
        sleep(.9)
        #t = dt.now()
        #print('Job_1, jobname ' + job_model.name + ' st2', t.strftime("%H:%M:%S.%fZ"))
        # Usage of json args column
        #print(job_model.args['key'])
        
        #for job in app.make('scheduler_hr').get_jobs():
        #    print(job.tags)

        #app.make('scheduler_hr').clear('Job_B')