from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class Options(forms.Form):
	opt1 = forms.BooleanField(required=False, label='Create staging tables?')
	opt2 = forms.BooleanField(required=False, label='Get ASX companies')
	opt3 = forms.BooleanField(required=False, label='Stage ASX companies')
	opt4 = forms.BooleanField(required=False, label='Stage changes in tickers')
	opt5 = forms.BooleanField(required=False, label='Get SAX Indicies History')
	opt6 = forms.BooleanField(required=False, label ='Stage indicies ')
	opt7 = forms.BooleanField(required=False, label='Get historical price data')
	opt8 = forms.BooleanField(required=False, label='Stage prices')
	opt9 = forms.BooleanField(required=False, label='Load production tables')
	opt10 = forms.BooleanField(required=False, label='Build calendar features')
	opt11 = forms.BooleanField(required=False, label='Run testing scripts')

	def clean_opt1(self):
		data = self.cleaned_data['opt1']
		return data

	def clean_opt2(self):
		data = self.cleaned_data['opt2']
		return data

	def clean_opt3(self):
		data = self.cleaned_data['opt3']
		return data

	def clean_opt4(self):
		data = self.cleaned_data['opt4']
		return data

	def clean_opt5(self):
		data = self.cleaned_data['opt5']
		return data

	def clean_opt6(self):
		data = self.cleaned_data['opt6']
		return data

	def clean_opt7(self):
		data = self.cleaned_data['opt7']
		return data

	def clean_opt8(self):
		data = self.cleaned_data['opt8']
		return data

	def clean_opt9(self):
		data = self.cleaned_data['opt9']
		return data

	def clean_opt10(self):
		data = self.cleaned_data['opt10']
		return data

	def clean_opt11(self):
		data = self.cleaned_data['opt11']
		return data


