from django import forms

from main.models import Mailing, Client, Letter


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('email', 'first_sent', 'periodicity', 'letter')
        widgets = {
            'first_sent': forms.TextInput(attrs={'type': 'datetime-local'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'fullname', 'comment')


class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ('title', 'body')