from django.contrib.gis.db import models


class Module(models.Model):
    module_id = models.CharField("Device ID", max_length=255, unique=True)

    def __str__(self):
        return self.module_id


class ModuleLocation(models.Model):
    module = models.ForeignKey(Module, related_name='locations', blank=True, null=True)
    geom = models.PointField("Location", srid=4326)
    created_on = models.DateTimeField("Created On")
    expired_on = models.DateTimeField("Expired On")

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

    def __str__(self):
        return self.name
