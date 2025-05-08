from django.core.exceptions import ValidationError


class ContainsLetterValidator:
    """
    Validator that checks whether the password contains at least one letter.
    """
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                "Le mot de passe doit contenir une lettre.",
                code='password_no_letter',
            )

    def get_help_text(self) -> str:
        return "Le mot de passe doit contenir au moins une lettre majuscule ou minuscule."
