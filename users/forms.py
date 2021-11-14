from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'Паролі не співпадають',
    }

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        error_messages = {
            'username': {
                'unique': "Ім'я вже зайняте",
                'required': "Заповнення обов'язкове"
            },
            'email': {
                'unique': "Пошта вже зайнята",
                'invalid': "Некоректна адреса",
                'required': "Заповнення обов'язкове"
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = "Ім'я користувача"
        self.fields['username'].help_text = 'До 150 символів. Букви, цифри та @ . + - _'

        self.fields['email'].label = "Пошта"
        self.fields['email'].help_text = 'Ваша електронна пошта'

        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].help_text = 'Від 8 символів, не повністю з цифр'

        self.fields['password2'].label = 'Підтвердження пароля'
        self.fields['password2'].help_text = 'Введіть пароль ще раз'


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
