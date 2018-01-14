from django.db import models
from django.core.validators import EmailValidator, RegexValidator


class TeamMember(models.Model):

    ADMIN = "admin"
    REGULAR = "regular"

    role_choices = (
        (ADMIN, "Admin"),
        (REGULAR, "Regular"),
    )

    first_name = models.TextField()
    last_name = models.TextField()
    phone_number = models.TextField(validators=[RegexValidator(regex=r"^\d{10}$", message="Invalid phone number")])
    email = models.TextField(validators=[EmailValidator(message="Invalid email address")])
    role = models.TextField(choices=role_choices)
