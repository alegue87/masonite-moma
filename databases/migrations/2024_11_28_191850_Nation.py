"""Nation Migration."""

from masoniteorm.migrations import Migration
from app.models import Time

class Nation(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("nations") as table:
            #table.increments("id")
            table.string('key').primary()
            table.string('name')
            table.big_integer('ping_ok').nullable()
            table.small_integer('min').nullable()
            table.small_integer('max').nullable()
            table.small_integer('avg').nullable()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("nations")
