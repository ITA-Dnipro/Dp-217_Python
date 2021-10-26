from django import forms
from .services import (
    RegionService as Regions,
    CityService as Cities,
    UniversityService as Unies,
    HousingService as Housings,
    )


class HousingForm(forms.Form):
    region = forms.ModelChoiceField(
        queryset=Regions.all(),
        label='Регіон',
        required=False,
        empty_label='Будь-яка область',
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
        )
    region_filter = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Шукати області...',
            }),
        )
    city = forms.ModelChoiceField(
        queryset=Cities.all(),
        label='Місто',
        required=False,
        empty_label='Будь-яке місто',
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
        )
    city_filter = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Шукати міста...',
            }),
        )
    uni = forms.ModelChoiceField(
        queryset=Unies.all(),
        label='Університет',
        required=False,
        empty_label='Будь-який ВУЗ',
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
        )
    uni_filter = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Шукати ВУЗи...',
            }),
        )

    def __init__(self, form_data, *args, **kwargs):
        self.qs = {'regions': None, 'cities': None, 'unies': None}
        self.data = self.__format_data(form_data)
        self.__set_initials()
        super().__init__(self.data, *args, **kwargs)
        self.__set_querysets()

    def __format_data(self, form_data):
        """Switch data to mutable a format type and construct querysets
        if possible."""
        self.data = dict(form_data)
        self.data['region_filter'] = form_data.get('region_filter', '')
        self.data['city_filter'] = form_data.get('city_filter', '')
        self.data['uni_filter'] = form_data.get('uni_filter', '')
        self.__create_querysets(form_data)
        return self.data

    def __create_querysets(self, form_data):
        """Create querysets based on filters and chosen ids from form data."""
        prompt = self.data['region_filter']
        if len(prompt) > 2:
            self.qs['regions'] = Regions.by_name(prompt)
        region_id = form_data.get('region')
        prompt = self.data['city_filter']
        if len(prompt) > 2 or region_id:
            self.qs['cities'] = Cities.by_region_or_name(region_id, prompt)
        city_id = form_data.get('city')
        prompt = self.data['uni_filter']
        if len(prompt) > 2 or city_id:
            self.qs['unies'] = Unies.by_city_or_name(city_id, prompt)
        return self.qs

    def __set_initials(self):
        """Set initial values for the choice fields (dropdown elements)."""
        if self.qs['regions']:
            self.data['region'] = self.qs['regions'][0].id
        if self.qs['cities']:
            self.data['cities'] = self.qs['cities'][0].id
        if self.qs['unies']:
            self.data['unies'] = self.qs['unies'][0].id

    def __set_querysets(self):
        """Set option lists for the choice fields (dropdown elements)."""
        if self.qs['regions'] is not None:
            self.fields['region'].queryset = self.qs['regions']
        if self.qs['cities'] is not None:
            self.fields['city'].queryset = self.qs['cities']
        if self.qs['unies'] is not None:
            self.fields['uni'].queryset = self.qs['unies']

    def get_housings(self):
        """Get the list of all housings if the university is chosen."""
        if uni_id := self.data.get('uni')[0]:
            if uni := Unies.get(uni_id):
                return Housings.all_for_uni(uni)
        return tuple()
