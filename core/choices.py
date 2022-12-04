from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class StatusTratamento(TextChoices):
    EM_TRATAMENTO = "Em Tratamento", _('Em Tratamento')
    ENCERRADO = "Encerrado", _('Encerrado')