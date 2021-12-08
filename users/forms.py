from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _('Паролі не співпадають'),
    }

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        error_messages = {
            'username': {
                'unique': _("Ім'я вже зайняте"),
                'required': _("Заповнення обов'язкове")
            },
            'email': {
                'unique': _("Пошта вже зайнята"),
                'invalid': _("Некоректна адреса"),
                'required': _("Заповнення обов'язкове")
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = _("Ім'я користувача")
        self.fields['username'].help_text = _('До 150 символів. Букви, цифри та @ . + - _')

        self.fields['email'].label = _("Пошта")
        self.fields['email'].help_text = _('Ваша електронна пошта')

        self.fields['password1'].label = _('Пароль')
        self.fields['password1'].help_text = _('Від 8 символів, не повністю з цифр')

        self.fields['password2'].label = _('Підтвердження пароля')
        self.fields['password2'].help_text = _('Введіть пароль ще раз')


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
                  'gender',
                  'is_relocating')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True
        self.fields['username'].label = _("Ім'я користувача")
        self.fields['email'].label = _("Пошта")
        self.fields['first_name'].label = _("Ім'я")
        self.fields['last_name'].label = _("Прізвище")
        self.fields['phone'].label = _("Телефон")
        self.fields['gender'].label = _("Стать")
        self.fields['city'].label = _("Місто")
        self.fields['is_relocating'].label = _("Отримувати нагадування щодо релокації")


class CustomUserAdminChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = '__all__'
