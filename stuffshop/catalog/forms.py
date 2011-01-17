# -*- coding: utf-8 -*-
from django import forms

class PhoneForm(forms.Form):
    NUM_OF_SIM = (('','Без разницы'),(1,'1'),(2,'2'),(3,'3'))
    num_of_sim = forms.ChoiceField(choices=NUM_OF_SIM,label='Количество сим-карт')
    HAS_SOMETHING = (('','Без разницы'),(1,'Есть'),(2,'Нет'))
    has_wifi = forms.ChoiceField(label='Наличие wi-fi',choices=HAS_SOMETHING)
    has_bluetooth = forms.ChoiceField(label='Наличие bluetooth',choices=HAS_SOMETHING)
    has_touchscreen = forms.ChoiceField(label='Наличие Touchscreen',choices=HAS_SOMETHING)
    has_gps = forms.ChoiceField(label='Наличие GPS',choices=HAS_SOMETHING)
    has_tv = forms.ChoiceField(choices=HAS_SOMETHING)
