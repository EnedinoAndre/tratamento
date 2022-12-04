from django.contrib import admin
from core import models


# Register your models here.
@admin.register(models.Tratamento)
class TratamentoAdmin(admin.ModelAdmin):
    #actions = None
    list_display = (
        'get_edit',
        'paciente',
        'medicamento',
        'get_data_tratamento',
        'get_horario',
        'get_duracao_dias',
        'get_quantidade_dia',
        'get_total',
        'get_restante',
        'get_status'
    )
    icon_name = 'enhanced_encryption'
    search_fields = ('paciente', 'medicamento',)
    list_filter = ('data_inicio',)
    list_per_page = 6
    list_max_show_all = 6

    fieldsets = (
        (None, {
            'fields': (
                ('paciente'),
                ('medicamento', 'quantidade_dia'),
                ('data_inicio', 'data_fim'),
                ('horario', 'status')
            )
        }),
    )


