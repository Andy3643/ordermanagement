from django import forms
from .models import Order
import re
from datetime import datetime

class RawOrderForm(forms.Form):
    raw_order_input = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Paste full order (e.g., FIN4424 Task 8 DUE 2/22 1PM EST)'})
    )

    def clean_raw_order_input(self):
        raw_order = self.cleaned_data.get("raw_order_input")

        match = re.search(r'(.+?)\sDUE\s(\d{1,2}/\d{1,2})\s(\d{1,2}(?::\d{2})?\s?[APap][Mm])\s?EST?', raw_order)
        if match:
            order_name = match.group(1).strip()
            due_date = match.group(2)
            due_time = match.group(3)

            # Convert date format to YYYY-MM-DD
            current_year = datetime.now().year
            month, day = map(int, due_date.split('/'))
            due_date = datetime(year=current_year, month=month, day=day).date()

            # Convert time to 24-hour format
            due_time = datetime.strptime(due_time, "%I%p" if ":" not in due_time else "%I:%M%p").time()

            return {"order_name": order_name, "date_due": due_date, "time_due": due_time}
        else:
            raise forms.ValidationError("Invalid format. Use: FIN4424 Task 8 DUE 2/22 1PM EST")

class ManualOrderForm(forms.ModelForm):
    # Generate 24-hour time choices (00:00 - 23:00)
    TIME_CHOICES = [(f"{hour:02d}:00", f"{hour:02d}:00") for hour in range(24)]

    time_due = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select())

    class Meta:
        model = Order
        fields = ['order_name', 'date_due', 'time_due']
        widgets = {
            'date_due': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_time_due(self):
        selected_time = self.cleaned_data['time_due']
        return datetime.strptime(selected_time, "%H:%M").time()  # Convert to Python `time` object
