from django.db import models


class Hospital(models.Model):
    class Meta:
        verbose_name = 'Больница'
        verbose_name_plural = 'Больницы'

    name = models.TextField('Название')
    address = models.TextField('Адрес')

    def __str__(self):
        return self.name


class HospitalUnit(models.Model):
    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отдел'

    name = models.TextField('Название')
    hospital = models.ForeignKey('Hospital', models.CASCADE, verbose_name='Больница')
    workers = models.ManyToManyField('users.User', verbose_name='Работники')

    def __str__(self):
        return self.name


class WorkerQueue(models.Model):
    class Meta:
        verbose_name = 'Очередь к работнику'
        verbose_name_plural = 'Очередь к работнику'

    worker = models.OneToOneField('users.User', models.CASCADE, verbose_name='Работник', related_name='queue')
    clients = models.ManyToManyField('users.User', verbose_name='Клиенты в очереди')

    def __str__(self):
        return self.worker.username
