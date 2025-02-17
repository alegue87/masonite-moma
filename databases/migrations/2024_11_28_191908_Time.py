"""Time Migration."""

from masoniteorm.migrations import Migration
from app.models import Nation

class Time(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("times") as table:
            table.increments("id")
            table.string('key_nation')
            table.foreign('key_nation').references('key').on('nations')
            table.decimal('ms').nullable()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("times")
