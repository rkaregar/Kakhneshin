from django import forms


class PlaceSearchForm(forms.Form):
    name = forms.SlugField(allow_unicode=True, required=False)
    division = forms.IntegerField(required=False)

    def clean_division(self):
        data = self.cleaned_data['division']
        if data == -1:
            self.add_error('division', 'شهر وارد شده در پایگاه داده موجود نیست.')
            return None
        return data
