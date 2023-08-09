from django.db import models

# Create your models here.


MEASUREMENT_UNITS = (
    ('литр', 'л'),
    ('миллилитр', 'мл'),
    ('грамм', 'г'),
    ('килограмм', 'кг'),
    ('штука', 'шт'),
)


class MeasurementUnit(models.Model):
    '''
    Saves units of measurments
    '''
    # TODO: add translation
    full_name = models.CharField(max_length=50, help_text='Наименоване')
    designation = models.CharField(max_length=10, help_text='Обозначение')

    def __str__(self):
        return '{}, {}'.format(self.full_name, self.designation)