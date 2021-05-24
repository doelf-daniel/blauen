from datetime import datetime

from django import forms

from config.settings.common import TZ

PROD_PERIOD_1 = '1-2 Tage'
PROD_PERIOD_2 = '3-4 Tage'
PROD_PERIOD_3 = '1 Woche'

PROD_PERIODS = (
    (PROD_PERIOD_1, PROD_PERIOD_1),
    (PROD_PERIOD_2, PROD_PERIOD_2),
    (PROD_PERIOD_3, PROD_PERIOD_3)
)


TABLE_PERIOD_DAYS = "Tagesdaten"
TABLE_PERIOD_WEEKS = "Wochendaten"
TABLE_PERIOD_MONTHS = "Monatsdaten"
TABLE_PERIOD_ACTUAL_YEAR = "aktuelles Jahr"
TABLE_PERIOD_UNDEFINED = "undefined"
TABLE_PERIODS = (
    (TABLE_PERIOD_DAYS, TABLE_PERIOD_DAYS),
    (TABLE_PERIOD_WEEKS, TABLE_PERIOD_WEEKS),
    (TABLE_PERIOD_MONTHS, TABLE_PERIOD_MONTHS),
    (TABLE_PERIOD_ACTUAL_YEAR, TABLE_PERIOD_ACTUAL_YEAR),
    (TABLE_PERIOD_UNDEFINED, TABLE_PERIOD_UNDEFINED)
)


class SelectFormEnergieChart(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dauer'] = forms.ChoiceField(choices=PROD_PERIODS)
        self.fields['ende'] = forms.DateField(label='Enddatum', required=True,
                                              input_formats=['%d.%m.%Y', ],
                                              widget=forms.DateInput(attrs={'class': 'datePicker'},
                                                                     format='%d.%m.%Y'))

    def clean(self):
        cleaned_data = super().clean()
        temp_date = cleaned_data['ende']
        if not isinstance(temp_date, datetime.date):
            raise forms.ValidationError("ende is not a valid date or datetime", code='invalid')
        ende = datetime(temp_date.year, temp_date.month, temp_date.day, tzinfo=TZ)
        cleaned_data['ende'] = ende
        return cleaned_data


class SelectFormEnergieTables(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['period'] = forms.ChoiceField(choices=TABLE_PERIODS)
        self.fields['begin'] = forms.DateField(label='von', required=True,
                                               input_formats=['%d.%m.%Y', ],
                                               widget=forms.DateInput(attrs={'class': 'datePicker'},
                                                                      format='%d.%m.%Y'))
        self.fields['end'] = forms.DateField(label='bis', required=True,
                                             input_formats=['%d.%m.%Y', ],
                                             widget=forms.DateInput(attrs={'class': 'datePicker'},
                                                                    format='%d.%m.%Y'))

    def clean(self):
        cleaned_data = super().clean()
        temp_date_end = cleaned_data['end']
        temp_date_begin = cleaned_data['begin']
        if temp_date_begin > temp_date_end:
            raise forms.ValidationError("Beginn muss vor dem Ende sein!", code='invalid')
        return cleaned_data


class SelectFormMesswerte(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['begin'] = forms.DateField(label='Datum', required=True,
                                               input_formats=['%d.%m.%Y', ],
                                               widget=forms.DateInput(attrs={'class': 'datePicker'},
                                                                      format='%d.%m.%Y'))


class DtForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['datumZeit'] = forms.DateTimeField(input_formats=['%d.%m.%Y %H:%M', ],
                                                       required=True)
