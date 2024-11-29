
import schedule
import threading
import time

from app.models.Jobs import Jobs as JobsModel

from datetime import datetime as dt

import sys
from importlib import reload, import_module  # Python 3.4+
sys.path.insert(0, './app/jobs')

def run_pending(app, interval=.1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                print('pending run')
                app.make('scheduler_hr').run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

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
    def __init__(self, app, run_pending_interval=0.1, run_manager_interval=5) -> None:
        def monitor(manager_thread):
            while True:
                if not manager_thread.is_alive():
                    manager_thread = run_manager(app, interval=run_manager_interval)
                time.sleep(5)
       
        app.singleton('scheduler_hr', schedule.Scheduler)
        
        self.stop_run_pending = run_pending(app, interval=run_pending_interval)
        manager_thread = run_manager(app, interval=run_manager_interval)

        threading.Thread(target=monitor, args=(manager_thread,)).start()

    def stop(self):
        self.stop_run_pending.set()
        self.stop_run_manager.set()

   