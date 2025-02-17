"""IpRange Migration."""

from masoniteorm.migrations import Migration


class IpRange(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("ip_ranges") as table:
            table.increments("id")
            table.string('key_nation')
            table.foreign('key_nation').references('key').on('nations')
            table.string('start')
            table.string('end')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("ip_ranges")
