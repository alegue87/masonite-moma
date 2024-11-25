"""MigrationForJobsTable Migration."""

from masoniteorm.migrations import Migration


class CreateForJobsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("jobs") as table:
            table.increments("id")
            table.string('name')
            table.decimal('interval').default(1)      # 1 second
            table.boolean('run').default(False)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("jobs")