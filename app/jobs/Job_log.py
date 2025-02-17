
from app.models.Time import Time
from datetime import datetime as dt

class Job_log:
    def start(app, job_model):
        
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
            
