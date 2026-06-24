from django import forms
from .models import Service, Language


class OrderForm(forms.Form):
    client_name = forms.CharField(
        max_length=100,
        min_length=2,
        label="Ім'я",
        error_messages={
            "required": "Будь ласка, введіть ім'я.",
            "min_length": "Ім'я повинно містити щонайменше 2 символи.",
            "max_length": "Ім'я занадто довге.",
        }
    )
    email = forms.EmailField(
        label="Email",
        error_messages={
            "required": "Будь ласка, введіть email.",
            "invalid": "Введіть коректну email-адресу.",
        }
    )
    phone = forms.CharField(
        max_length=20,
        min_length=10,
        label="Телефон",
        error_messages={
            "required": "Будь ласка, введіть номер телефону.",
            "min_length": "Номер телефону повинен містити щонайменше 10 символів.",
            "max_length": "Номер телефону занадто довгий.",
        }
    )
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        label="Послуга",
        empty_label="Оберіть послугу",
        error_messages={
            "required": "Будь ласка, оберіть послугу.",
        }
    )
    source_language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        label="Мова оригіналу",
        empty_label="Оберіть мову оригіналу",
        error_messages={
            "required": "Будь ласка, оберіть мову оригіналу.",
        }
    )
    target_language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        label="Мова перекладу",
        empty_label="Оберіть мову перекладу",
        error_messages={
            "required": "Будь ласка, оберіть мову перекладу.",
        }
    )
    comment = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label="Коментар"
    )

    def clean(self):
        cleaned_data = super().clean()
        source_language = cleaned_data.get("source_language")
        target_language = cleaned_data.get("target_language")

        if source_language and target_language:
            if source_language.pk == target_language.pk:
                self.add_error(
                    "target_language",
                    "Мова оригіналу і мова перекладу не можуть бути однаковими."
                )

        return cleaned_data