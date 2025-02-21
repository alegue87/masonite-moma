
#from Sched import scheduler
from apscheduler.schedulers.background import BackgroundScheduler

from multiprocessing import Process
from datetime import datetime as dt
import threading
import time

from app.models.Jobs import Jobs as JobsModel

import sys
from importlib import reload, import_module  # Python 3.4+
sys.path.insert(0, './app/jobs')

#s = scheduler(time.time, time.sleep)
aps = BackgroundScheduler()

from app.models.Time import Time
from datetime import datetime as dt


def log(app):

    old_time = ''
    if app.has('log_time'):
        old_time = app.make('log_time')
        if old_time == 0:
            app.bind('log_time', dt.timestamp(dt.now()))
            return
    else:
        app.bind('log_time', dt.timestamp(dt.now()))
        return

    # t_old = Time.builder.where('key_nation', 'zw').max('id').first()        

    now_time = dt.timestamp(dt.now())
    print('Current: ', now_time-old_time)

    try:
        Time.create({
            'key_nation': 'zw',
            'ms': float(now_time-old_time),
        })
        app.bind('log_time', dt.timestamp(dt.now()))
    except Exception as e:
        app.bind('log_time', 0)


class Dimport: 
    start_method = None
    def __init__(self, module_name, class_name, app, job_model): 
        #__import__ method used 
        # to fetch module 
        try:
            module = import_module(module_name)
            reload(module)
            # getting attribute by 
            # getattr() method 
            my_class = getattr(module, class_name) 
            #my_class.start(app, job_model) 
            self.start_method =  my_class.start
        except Exception as e:
            print(e)
    
    def get_start_method(self):
        return self.start_method

def run_pending(app):

    log(app)

    def runner(jobs):

        list_job = []
        for job_model in jobs:
            method = Dimport(
                    module_name=job_model.class_name, 
                    class_name =job_model.class_name, 
                    app=app, 
                    job_model=job_model \
                ).get_start_method()

            p = Process(target=method, kwargs={'app':app, 'job_model': job_model}, daemon=True)
            #s.enter(delay=.0, priority=-20, action=p )
            #list_job = s.run(blocking=False)
            p.start()
            list_job.append(p)

        # 0.5 / 10 = 0.05 join
        for j in list_job:
            j.join(1/len(list_job))
   
    t = dt.now()
    currentSec = int(t.strftime("%S"))

    job_model_list = JobsModel.where('run', True).where('start_second', currentSec).get()

    run_jobs = []
    for job_model in job_model_list:
        run_jobs.append(job_model)

    Process(target=runner, args=(run_jobs, )).start()

def runner(app):
    log(app)

    t = dt.now()
    currentSec = int(t.strftime("%S"))

    job_model_list = []
    if currentSec == 0:
        job_model_list = JobsModel.get()

    for job_model in job_model_list:
        #run_jobs.append(job_model)
       
        if job_model.run:
            try:
                aps._lookup_job(job_id=job_model.name, jobstore_alias='default')
            except Exception as e:  
                print('run ' + job_model.name)
                method = Dimport(
                    module_name=job_model.class_name, 
                    class_name =job_model.class_name, 
                    app=app, 
                    job_model=job_model \
                ).get_start_method()
                aps.add_job(method, 'interval', 
                    seconds=int(job_model.interval), 
                    jitter=int(job_model.start_second), 
                    id=job_model.name, 
                    args=(app, job_model), 
                    max_instances=3)
        else: 
            try:
                aps.remove_job(job_id=job_model.name, jobstore='default')
            except Exception as e:
                pass

def run_manager(app, interval=5):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):

            def run_threaded(app, job_model):
                method = Dimport(
                    module_name=job_model.class_name, 
                    class_name =job_model.class_name, 
                    app=app, 
                    job_model=job_model \
                ).get_start_method()

                job_thread = threading.Thread(target=method, kwargs={'app':app, 'job_model':job_model})
                job_thread.start()
            
            scheduler_hr = app.make('scheduler_hr')
            while not cease_continuous_run.is_set():
                print('run job manager')

                job_model_list = JobsModel.all()

                for job_model in job_model_list:

                    running_job_list = scheduler_hr.get_jobs(job_model.name)

                    if len(running_job_list) == 1:
                        #running_job = running_job_list[0]
                        if job_model.run == False:
                            scheduler_hr.clear(job_model.name)
                    else:
                        if job_model.run == True:
                            if job_model.start_second > 0:
                                sec = int(job_model.start_second)
                                if sec < 10:
                                    sec = ':0'+str(sec)
                                else:
                                    sec = ':'+str(sec)
                                scheduler_hr.every().minute \
                                    .at(sec)\
                                    .do(
                                        run_threaded, 
                                        app=app,
                                        job_model=job_model
                                    ) \
                                    .tag(job_model.name)
                            else:
                                scheduler_hr.every(float(job_model.interval)).seconds \
                                    .do(
                                        run_threaded, 
                                        app=app,
                                        job_model=job_model
                                    ) \
                                    .tag(job_model.name)
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return continuous_thread 

class SchedulerHighRate():
    def __init__(self, app, run_pending_interval=1, run_manager_interval=5) -> None:
        def monitor(manager_thread):
            while True:
                if not manager_thread.is_alive():
                    manager_thread = run_manager(app, interval=run_manager_interval)
                time.sleep(5)
       
        #app.singleton('scheduler_hr', schedule.Scheduler)
        
        #self.stop_run_pending = run_pending(app, interval=run_pending_interval)
        #manager_thread = run_manager(app, interval=run_manager_interval)

        #threading.Thread(target=monitor, args=(manager_thread,)).start()
        
        def scheduler(app, interval):
            print('Running scheduler')
            while True:
                run_pending(app)
                time.sleep(interval)

        #interval = 1
        #p = Process(target=scheduler, args=(app, interval )).start()
        aps.add_job(runner, 'interval', seconds=1, max_instances=5, jitter=0, args=(app,))

        aps.start()
    def stop(self):
        self.stop_run_pending.set()
        self.stop_run_manager.set()

   
