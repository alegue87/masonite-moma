"""JobsTableSeeder Seeder."""

from masoniteorm.seeds import Seeder
from app.models.Jobs import Jobs

class JobsTableSeeder(Seeder):
    def run(self):
        """Run the database seeds."""
        Jobs.builder.new().bulk_create([
            {'name': 'Job_A', 'class_name': 'Job_1', 'interval': 0.1, 'run': False},
            {'name': 'Job_B', 'class_name': 'Job_2', 'interval': 0.1, 'run': False},
            {'name': 'Job_C', 'class_name': 'Job_2', 'interval': 0.1, 'run': False},
            {'name': 'Job_D', 'class_name': 'Job_2', 'interval': 0.1, 'run': False},
            {'name': 'Job_E', 'class_name': '', 'interval': 0.1, 'run': False},
            {'name': 'Job_F', 'class_name': '', 'interval': 0.1, 'run': False},
            {'name': 'Job_G', 'class_name': '', 'interval': 0.1, 'run': False},
        ])
        
