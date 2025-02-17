""" Nation Model """

from masoniteorm.relationships import has_many
from masoniteorm.models import Model


class Nation(Model):
    """Nation Model"""

    @has_many('key', 'key_nation')
    def times(self):
       from app.models.Time import Time
       return Time
    
    @has_many('key', 'key_nation')
    def ipRange(self):
       from app.models.IpRange import IpRange
       return IpRange
