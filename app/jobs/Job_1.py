
class Job_1:
    def start(app, job_model):
        print('Job_1, jobname ' + job_model.name)

        # Usage of json args column
        #print(job_model.args['key'])
        
        #for job in app.make('scheduler_hr').get_jobs():
        #    print(job.tags)

        #app.make('scheduler_hr').clear('Job_B')