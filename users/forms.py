from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class CustomUserChangeForm(UserChangeForm):

    password = None

    class Meta:
        model = CustomUser
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'city',
                  'phone',
                  'gender')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True
        self.fields['username'].label = "Ім'я користувача"
        self.fields['email'].label = "Пошта"
        self.fields['first_name'].label = "Ім'я"
        self.fields['last_name'].label = "Прізвище"
        self.fields['phone'].label = "Телефон"
        self.fields['gender'].label = "Стать"
        self.fields['city'].label = "Місто"


class CustomUserAdminChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = '__all__'
