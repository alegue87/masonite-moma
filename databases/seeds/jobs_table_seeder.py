"""JobsTableSeeder Seeder."""

from masoniteorm.seeds import Seeder
from app.models.Jobs import Jobs

class JobsTableSeeder(Seeder):
    def run(self):
        """Run the database seeds."""
        Jobs.builder.new().bulk_create([
            {'name': 'Job_A', 'interval': 0.1, 'run': True},
            {'name': 'Job_B', 'interval': 0.1, 'run': False},
            {'name': 'Job_C', 'interval': 0.1, 'run': False},
            {'name': 'Job_D', 'interval': 0.1, 'run': False},
            {'name': 'Job_E', 'interval': 0.1, 'run': False},
            {'name': 'Job_F', 'interval': 0.1, 'run': False},
            {'name': 'Job_G', 'interval': 0.1, 'run': False},
        ])
        
