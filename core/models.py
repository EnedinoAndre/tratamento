from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from core import choices
from datetime import date, timedelta


####################################
############ PACIENTE ##############
####################################
class Paciente(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome', help_text='Digite o nome do paciente')
    idade = models.IntegerField(verbose_name='Idade', null=True, help_text='Digite a idade')

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return self.nome


####################################
########### MEDICAMENTO ############
####################################
class Medicamento(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome', help_text='Digite o nome do medicamento')
    dosagem = models.CharField(max_length=100, verbose_name='Dosagem', help_text='Ex. 40MG/mL AMP/2mL')

    class Meta:
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'

    def __str__(self):
        return f"{self.nome} - Dosagem: {self.dosagem}"


####################################
############ TRATAMENTO ############
####################################
class Tratamento(models.Model):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        verbose_name='Paciente',
        related_name='pacientes',
        help_text='Selecione um paciente ou cadastre um novo paciente'
    )

    medicamento = models.ForeignKey(
        Medicamento,
        on_delete=models.CASCADE,
        verbose_name='Medicamento',
        related_name='medicamentos',
        help_text='Selecione o medicamento ou cadastre um novo medicamento'
    )

    data_inicio = models.DateField(verbose_name='Inicio do tratamento')
    data_fim = models.DateField(verbose_name='Fim do tratamento')
    quantidade_dia = models.IntegerField(
        verbose_name='Quantidade(Dia)',
        null=True,
        blank=True,
        help_text='Quantidade a ser tomada por dia'
    )
    horario = models.CharField(max_length=10, verbose_name="Horário", help_text='Ex. 8/8, 6/6')
    status = models.CharField(
        max_length=20,
        choices=choices.StatusTratamento.choices,
        default=choices.StatusTratamento.EM_TRATAMENTO,
    )

    class Meta:
        verbose_name = 'Tratamento'
        verbose_name_plural = 'Tratamentos'

    def __str__(self):
        return f"Prescrição para {self.paciente}"

    @admin.display(description='##')
    def get_edit(self):
        url = (
            f"<i title='Editar' class='tiny material-icons'>edit</i>"
        )
        return format_html(url)

    @admin.display(description='Tratamento', ordering='data_inicio')
    def get_data_tratamento(self):
        inicio = self.data_inicio.strftime('%d/%m/%Y')
        fim = self.data_fim.strftime('%d/%m/%Y')
        retorno = (
            f'<div class="left-align">'
            f'<p style="padding:0px;"><b>Início:</b><br>{inicio}</p>'
            f'<p style="padding:0px;"><b>Fim:</b><br>{fim}</p></div>'
        )
        return format_html(retorno)

    @admin.display(description=format_html(
        f'<div div class="center-align" style="font-weight: bold; background-color: #8bc649; padding: 3px;'
        f'border: 2px solid #eeeeee;border-radius: 3px; color:#FFFFFF;">Horário</div>'
    ))
    def get_horario(self):
        retorno = (
            f'<div div class="center-align" style="font-weight: bold; background-color: #DCDCDC; padding: 3px;'
            f'border: 2px solid #eeeeee;border-radius: 3px;">{self.horario}</div>'
        )
        return format_html(f'{retorno}')

    @admin.display(description=format_html(
        f'<div div class="center-align" style="font-weight: bold; background-color: #8bc649; padding: 3px;'
        f'border: 2px solid #eeeeee;border-radius: 3px; color:#FFFFFF;">Duração(dias)</div>'
    ))
    def get_duracao_dias(self):
        resultado = self.calculo_duracao_tratamento()
        retorno = (
            f'<div div class="center-align" style="font-weight: bold; background-color: #DCDCDC; padding: 3px;'
            f'border: 2px solid #eeeeee;border-radius: 3px;">{resultado}</div>'
        )
        return format_html(f'{retorno}')

    @admin.display(description=format_html(
        f'<div div class="center-align" style="font-weight: bold; background-color: #8bc649; padding: 3px;'
        f'border: 2px solid #eeeeee;border-radius: 3px; color:#FFFFFF;">Quantidade(dia)</div>'
    ))
    def get_quantidade_dia(self):
        retorno = (
            f'<div div class="center-align" style="font-weight: bold; background-color: #DCDCDC; padding: 3px;'
            f'border: 2px solid #eeeeee;border-radius: 3px;">{self.quantidade_dia}</div>'
        )
        return format_html(f'{retorno}')

    @admin.display(description=format_html(
        f'<div div class="center-align" style="font-weight: bold; background-color: #8bc649; padding: 3px;'
        f'border: 2px solid #eeeeee;border-radius: 3px; color:#FFFFFF;">Total</div>'
    ))
    def get_total(self):
        resultado = self.calculo_duracao_tratamento() * self.quantidade_dia
        retorno = (
            f'<div div class="center-align" style="font-weight: bold; background-color: #DCDCDC; padding: 3px;'
            f'border: 2px solid #eeeeee;border-radius: 3px;">{resultado}</div>'
        )
        return format_html(f'{retorno}')

    @admin.display(description=format_html(
        f'<div div class="center-align" style="font-weight: bold; background-color: #8bc649; padding: 3px;'
        f'border: 2px solid #eeeeee;border-radius: 3px; color:#FFFFFF;">Restante</div>'
    ))
    def get_restante(self):
        calculo_total = self.calculo_duracao_tratamento() * self.quantidade_dia
        if date.today() <= self.data_fim:
            dif_hoje_fim = abs((date.today() - self.data_inicio).days)
            quantidade_tomada = self.quantidade_dia * (dif_hoje_fim)
            retorno = (
                f'<div div class="center-align" style="font-weight: bold; background-color: #DCDCDC; padding: 3px;'
                f'border: 2px solid #eeeeee;border-radius: 3px;">{calculo_total - quantidade_tomada}</div>'
            )
            return format_html(f'{retorno}')
        else:
            self.status = choices.StatusTratamento.ENCERRADO
            self.save()
            return "Acabou"

    @admin.display(description=format_html(
        f'<div div class="center-align" style="font-weight: bold; background-color: #8bc649; padding: 3px;'
        f'border: 2px solid #eeeeee;border-radius: 3px; color:#FFFFFF;">Status</div>'
    ))
    def get_status(self):
        if self.status == choices.StatusTratamento.EM_TRATAMENTO:
            retorno = (
                f'<div class="center-align"  style="font-weight: bold; background-color: #1E90FF; padding: 3px; '
                f'border: 2px solid #eeeeee;border-radius: 3px; color: #FFFFFF;">{self.status}</div>'
            )

        elif self.status == choices.StatusTratamento.ENCERRADO:
            retorno = (
                f'<div class="center-align"  style="font-weight: bold; background-color: #B22222; padding: 3px; '
                f'border: 2px solid #eeeeee;border-radius: 3px;color: #FFFFFF;">{self.status}</div>'
            )

        return format_html(f'{retorno}')

    ########################################################################
    ######################## MÉTODOS ALTERNATIVOS ##########################
    ########################################################################
    def calculo_duracao_tratamento(self):
        duracao_tratamento_dias = abs((self.data_fim - self.data_inicio).days)
        resultado = duracao_tratamento_dias + 1
        return resultado




