from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('email', 'cvcode', 'expirem', 'expirey', 'cardnumber')

    def clean_cardnumber(self):
        cardnumber = self.cleaned_data.get('cardnumber')
        cardnumber = cardnumber.replace(' ', '').replace('-', '')
        if not (11 < len(cardnumber) < 20):
            raise forms.ValidationError("Credit card number must be 12-19 digits.")
        return cardnumber

    def clean_cvcode(self):
        cvcode = self.cleaned_data.get('cvcode')
        if not (2 < len(str(cvcode)) < 5):
            raise forms.ValidationError("CV Code must be 4 digits for American Express and 3 digits for other card types.")
        return cvcode

    def clean_expirem(self):
        expirem = self.cleaned_data.get('expirem')
        if not (0 < expirem < 13):
            raise forms.ValidationError("Month must be between 1-12.")
        return expirem
