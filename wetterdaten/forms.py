import logging
from datetime import datetime, timedelta

from django import forms

from common.models import *
from blauen.settings.common import TZ

logger = logging.getLogger(__name__)


class SelectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SelectForm, self).__init__(*args, **kwargs)
        self.fields['dauer'] = forms.ChoiceField(choices=PERIODS)
        self.fields['beginn'] = forms.DateField(label='von', required=True,
                                                input_formats=['%d.%m.%Y', ],
                                                widget=forms.DateInput(attrs={'class': 'datePicker'},
                                                                       format='%d.%m.%Y'))
        self.fields['ende'] = forms.DateField(label='bis', required=True,
                                              input_formats=['%d.%m.%Y', ],
                                              widget=forms.DateInput(attrs={'class': 'datePicker'},
                                                                     format='%d.%m.%Y'))

    def clean(self):
        cleaned_data = super(SelectForm, self).clean()
        dauer = cleaned_data['dauer']
        beginn = cleaned_data['beginn']
        ende = cleaned_data['ende']
        if dauer == DAUER_SELECT:
            if beginn is not None and ende is not None:
                if beginn < ende:
                    return cleaned_data
                else:
                    logger.warning('Ungültige Selektion, Beginn kann nicht nach dem Ende sein.')
                    raise forms.ValidationError(
                        'Ungültige Selektion, Beginn kann nicht nach dem Ende sein.',
                        code='invalid selection'
                    )
            else:
                logger.warning('Ungültige Selektion, Beginn und Ende sind einzugeben')
                raise forms.ValidationError(
                    'Ungültige Selektion, Beginn und Ende sind einzugeben',
                    code='invalid selection'
                )
        else:
            # aufgrund der Selektion sind Beginn und Ende bestimmt.
            dt = datetime.now()
            dte = datetime(dt.year, dt.month, dt.day, 23, 59, 59, 999999, tzinfo=TZ)
            dt0 = datetime(dte.year, dte.month, dte.day, tzinfo=TZ)
            cleaned_data['ende'] = dte
            if dauer == DAUER_TAG:
                cleaned_data['beginn'] = dt0 - timedelta(days=1)
            elif dauer == DAUER_WOCHE:
                cleaned_data['beginn'] = dt0 - timedelta(days=7)
            elif dauer == DAUER_MONAT:
                cleaned_data['beginn'] = dt0 - timedelta(days=31)
            elif dauer == DAUER_VIERTELJAHR:
                cleaned_data['beginn'] = dt0 - timedelta(days=92)
            elif dauer == DAUER_HALBES_JAHR:
                cleaned_data['beginn'] = dt0 - timedelta(days=183)
            elif dauer == DAUER_JAHR:
                cleaned_data['beginn'] = dt0 - timedelta(days=365)

        return cleaned_data


class SelectDateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['datum'] = forms.DateField(label='Datum', required=True,
                                               input_formats=['%d.%m.%Y', ],
                                               widget=forms.DateInput(attrs={'class': 'datePicker'},
                                                                      format='%d.%m.%Y'))
