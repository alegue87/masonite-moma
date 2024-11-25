
class Job_A:
    def start(app, job_model):
        print('jobname ' + job_model.name)

        #for job in app.make('scheduler_hr').get_jobs():
        #    print(job.tags)

        #app.make('scheduler_hr').clear('Job_B')