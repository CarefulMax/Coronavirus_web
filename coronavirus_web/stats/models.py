from django.db import models


# Create your models here.
class Regions(models.Model):
    region = models.CharField(max_length=100, blank=False, verbose_name='Регион')

    def __str__(self):
        return self.region

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        db_table = 'regions'


class RegionalStats(models.Model):
    date = models.DateField(verbose_name='Дата')
    region = models.ForeignKey('Regions', on_delete=models.CASCADE, default=-1, verbose_name='id региона')
    new_cases = models.IntegerField(verbose_name='Новые случаи')
    hospitalised = models.IntegerField(verbose_name='Госпитализировано')
    recovered = models.IntegerField(verbose_name='Вылечились')
    died = models.IntegerField(verbose_name='Умерло')
    vaccinated_first_component_cumulative = models.IntegerField(verbose_name='Вакцинировано 1 комп.')
    vaccinated_fully_cumulative = models.IntegerField(verbose_name='Вакцинировано 2 комп.')
    collective_immunity = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Коллективный иммунитет')

    def __str__(self):
        return f'Дата: {self.date} ' \
               f'Регион: {self.region.region} ' \
               f'Новых случаев: {self.new_cases} ' \
               f'Госпитализировано: {self.hospitalised} ' \
               f'Вылечились: {self.recovered} ' \
               f'Умерло: {self.died} ' \
               f'Вакцинировано первым компонентом: {self.vaccinated_first_component_cumulative} ' \
               f'Вакцинировано полностью: {self.vaccinated_fully_cumulative} ' \
               f'Коллективный иммунитет: {self.collective_immunity}'

    class Meta:
        verbose_name = 'Региональная статистика'
        verbose_name_plural = 'Региональная статистика'
        db_table = 'regional_stats'
        ordering = ['-date', 'region']
        unique_together = ['date', 'region']


class Restrictions(models.Model):
    description = models.TextField(unique=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Ограничение'
        verbose_name_plural = 'Ограничения'


class RegionalRestrictions(models.Model):
    region = models.ForeignKey('Regions', on_delete=models.CASCADE, default=-1, verbose_name='id региона')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    restriction = models.ForeignKey('Restrictions', on_delete=models.CASCADE, default=-1, verbose_name='Ограничение')

    def __str__(self):
        return f'Регион: {self.region}' \
               f'Дата: {self.date}' \
               f'Ограничение: {self.restriction}'

    class Meta:
        verbose_name = 'Региональное ограничение'
        verbose_name_plural = 'Региональные ограничения'
        db_table = 'regional_restrictions'
        ordering = ['-date', 'region']
        unique_together = ['date', 'region', 'restriction']


class LastParsed(models.Model):
    parse_datetime = models.DateTimeField(auto_now=True, verbose_name='Время последней проверки')
    parsed_info_datetime = models.DateField(verbose_name='Время последних взятых данных')
    parse_success = models.BooleanField(verbose_name='Парсинг прошел успешно', default=False)

    def __str__(self):
        if self.parse_success:
            return f'Последний парсинг (успешный) - {self.parse_datetime}, последние данные - {self.parsed_info_datetime}'
        else:
            return f'Последний парсинг не прошел в {self.parse_datetime}, последние данные - {self.parsed_info_datetime}'

    class Meta:
        verbose_name = 'Последний парсинг'
        verbose_name_plural = 'Последний парсинг'
        db_table = 'last_parsed'
