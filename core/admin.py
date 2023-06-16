from django.contrib import admin
from core import models
from django.utils.html import format_html
from django.contrib.auth.models import User, Group

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(models.Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade')
    search_fields = ('nome',)
    list_per_page = 6
    list_max_show_all = 6
    fields = ('nome', 'idade')

    icon_name = 'airline_seat_flat'


@admin.register(models.Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'dosagem')
    search_fields = ('nome',)
    list_per_page = 6
    list_max_show_all = 6
    fields = ('nome', 'dosagem')

    icon_name = 'healing'


@admin.register(models.Tratamento)
class TratamentoAdmin(admin.ModelAdmin):
    #actions = None
    list_display = (
        'get_edit',
        'get_paciente',
        'get_medicamento',
        'get_data_tratamento',
        'get_horario',
        'get_duracao_dias',
        'get_quantidade_dia',
        'get_total',
        'get_restante',
        'get_status'
    )
    icon_name = 'receipt'
    #search_fields = ('paciente', 'medicamento',)
    list_filter = ('data_inicio',)
    autocomplete_fields = ('paciente', 'medicamento')
    list_per_page = 6
    list_max_show_all = 6

    fieldsets = (
        (None, {
            'fields': (
                ('paciente', 'medicamento'),
                ('quantidade_dia'),
                ('data_inicio', 'data_fim'),
                ('horario', 'status')
            )
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = None

    @admin.display(description='paciente')
    def get_paciente(self, objeto):

        return format_html(objeto.paciente.nome)

    @admin.display(description='Medicamento')
    def get_medicamento(self, objeto):
        retorno = (
            f'<div>'
            f'<p><b>Medicamento: </b><br>{objeto.medicamento.nome}</p>'
            f'<p><b>Dosagem: </b><br>{objeto.medicamento.dosagem}</p>'
            f'</div>'
        )

        return format_html(retorno)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.request = request
        return qs
