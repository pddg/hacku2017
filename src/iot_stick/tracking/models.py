import enum
from django.contrib.gis.db import models


class BaseChoices(enum.Enum):
    @classmethod
    def choices(cls):
        return ((m.value, m.name) for m in cls)


class StateChoices(BaseChoices):
    IN = 0
    OUT = 1


class IsKnockedDownChoice(BaseChoices):
    UP = 0
    DOWN = 1


class Module(models.Model):
    name = models.CharField("Device User", max_length=255, default="Test User")
    module_id = models.CharField("Device ID", max_length=255, unique=True)

    def __str__(self):
        return self.module_id


class ModuleLocation(models.Model):
    module = models.ForeignKey(Module, related_name='locations', blank=True, null=True)
    geom = models.PointField("Location", srid=4326)
    expired = models.BooleanField("Expired", default=False)
    state = models.IntegerField("State", choices=StateChoices.choices(), default=0)
    is_knocked_down = models.IntegerField("Is knocked down", choices=IsKnockedDownChoice.choices(), default=0)
    created_on = models.DateTimeField("Created On")
    expired_on = models.DateTimeField("Expired On", blank=True, null=True)

    def __str__(self):
        return self.created_on.strftime("%Y-%m-%d %H:%M:%S.%f")


class ModulePostLog(models.Model):
    module = models.ForeignKey(Module, related_name='logs', blank=True, null=True)
    type = models.CharField("Type", max_length=255)
    datetime = models.DateTimeField("Created On")
    associated = models.BooleanField("Associated", default=False)

    def __str__(self):
        return "{}-{}".format(self.type,
                              self.datetime.strftime("%Y-%m-%d %H:%M:%S.%f"))


class ChannelLog(models.Model):
    channel = models.IntegerField("Channel")
    type = models.CharField("Type", max_length=255)
    value = models.FloatField("Value")
    datetime = models.DateTimeField("Acquired On")
    module_log = models.ForeignKey(ModulePostLog, related_name='payload')

    def __str__(self):
        return "{}-{}-{}".format(self.module_log.module.module_id,
                                 self.channel,
                                 self.datetime.strftime("%Y-%m-%d %H:%M:%S.%f"))


class Home(models.Model):
    name = models.CharField("Home", max_length=255)
    geom = models.PointField("Location", srid=4326)
    radius = models.IntegerField("Radius")
    module = models.ForeignKey(Module, related_name='home', blank=True, null=True)

    def __str__(self):
        return self.name


class NotificationLog(models.Model):
    class HttpStatusChoice(BaseChoices):
        SUCCESS = 0
        FAIL = 1
        RUNNING = 2
    module = models.ForeignKey(Module, related_name='notifications')
    state = models.IntegerField("State", choices=StateChoices.choices(), default=2)
    status_code = models.IntegerField("HTTP Status", blank=True, null=True)
    status = models.IntegerField("is Success", choices=HttpStatusChoice.choices(), default=2)
    home = models.CharField("Home", max_length=255)
    created_on = models.DateTimeField("Notified at", auto_now_add=True)

    def __str__(self):
        return "{} {} {} {}".format(self.created_on.strftime('%Y/%m/%d %H:%M:%S'),
                                    self.module.name,
                                    StateChoices(self.state),
                                    self.home)
