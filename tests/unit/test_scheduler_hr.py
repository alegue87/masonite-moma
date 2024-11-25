from tests import TestCase
from SchedulerHighRate import SchedulerHighRate
from time import sleep

from app.models.Jobs import Jobs

RUN_PENDING_INTERVAL = 0.1
RUN_MANAGER_INTERVAL = 0.1

class SchedulerHrTestCase(TestCase):
    def test_scheduler_hr_is_empty(self):
        hr = SchedulerHighRate(self.application, RUN_PENDING_INTERVAL, RUN_MANAGER_INTERVAL)

        app = self.application

        sleep(1)
        job_list = app.make('scheduler_hr').get_jobs()
        hr.stop()
        self.assertEqual(len(job_list), 0)

    def test_scheduler_hr_Job_A_run_and_stop(self):
        hr = SchedulerHighRate(self.application, RUN_PENDING_INTERVAL, RUN_MANAGER_INTERVAL)

        app = self.application
        ja = Jobs.where('name', 'Job_A').first()

        ja.run = True
        ja.save()

        sleep(0.5)

        job_list = app.make('scheduler_hr').get_jobs()
        self.assertEqual(len(job_list), 1)

        sleep(0.5)
        
        ja.run = False
        ja.save()

        sleep(0.5)

        job_list = app.make('scheduler_hr').get_jobs()
        self.assertEqual(len(job_list), 0)

        hr.stop()



