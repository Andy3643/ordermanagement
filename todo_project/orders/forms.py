from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_name', 'date_due', 'time_due']
        widgets = {
            'date_due': forms.DateInput(attrs={'type': 'date'}),
            'time_due': forms.Select(choices=[(f'{i:02d}:{j:02d}', f'{i:02d}:{j:02d}') for i in range(24) for j in range(0, 60, 30)]),
        }
