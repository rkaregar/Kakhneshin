from django import forms


class HabitatSearchForm(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()
    division = forms.IntegerField(required=True)
    persons = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(HabitatSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = 'پر کردن این فیلد اجباری است.'

    def clean_division(self):
        data = self.cleaned_data['division']
        if data == -1:
            self.add_error('division', 'شهر وارد شده در پایگاه داده موجود نیست.')
            return None
        return data
