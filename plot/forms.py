import pandas as pd
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file1 = forms.FileField()
    file2 = forms.FileField()
    file3 = forms.FileField()

class UploadFileForm2(forms.Form):
    choice_list = []
    choices = ['open_1','open_base','open_2','close_1','close_base','close_2','base_vs_d1','base_vs_d2','cbase_vs_cd1','cbase_vs_cd2','time','year']
    for i in choices:
        choice_list.append((i,i))
    year_choice = []
    for i in range(2019,2025):
        year_choice.append((i,i))
    year = forms.ChoiceField(choices = year_choice)
    x_axis = forms.ChoiceField(choices = choice_list)
    y_axis = forms.ChoiceField(choices = choice_list)