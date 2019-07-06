from django import forms


class HabitatSearchForm(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()
    division = forms.IntegerField()
    persons = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(HabitatSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = 'پر کردن این فیلد اجباری است.'

    def clean_division(self):
        if self.cleaned_data['division'] == -1:
            self.add_error('شهر وارد شده در پایگاه داده موجود نیست.', 'division')
            return None
