from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from .models import Orcamento
from django.urls import reverse_lazy

from .analysis import Analise

# Create your data analise


# Create your views here.
class OrcamentoIndexView(TemplateView):
    template_name = 'orcamento/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        data_entries = Orcamento.objects.all()
        values = [entry for entry in data_entries.values()]

        analise = Analise(values=values)

        # -----------
        context['DESPESA_FIXA'] = analise.DESPESA_FIXA()
        context['RENDA_EXTRA'] = analise.RENDA_EXTRA()
        context['PERC_INVESTIMENTO'] = analise.PERC_INVESTIMENTO()
        context['CAIXA'] = analise.CAIXA()
        context['FIG_recebidos'] = analise.FIG_recebidos().to_html(
            full_html=False, default_height=250, default_width=175)
        context['FIG_acumulo'] = analise.FIG_acumulo().to_html(full_html=False, default_height=250, default_width=675)
        context['FIG_meta'] = analise.FIG_meta().to_html(full_html=False, default_height=250, default_width=425)
        context['FIG_despesas'] = analise.FIG_despesas().to_html(full_html=False, default_height=250, default_width=175)
        context['FIG_receita_despesa'] = analise.FIG_receita_despesa().to_html(
            full_html=False, default_height=250, default_width=675)
        context['FIG_despesas_mes'] = analise.FIG_despesas_mes().to_html(
            full_html=False, default_height=250, default_width=425)

        return context


class OrcamentoCreate(CreateView):
    model = Orcamento
    fields = ['ordem', 'descricao', 'valor', 'categoria', 'periodo', 'fixo', 'credito']
    template_name = 'orcamento/form.html'
    success_url = reverse_lazy('registrar-orcamento')


class OrcamentoList(ListView):
    model = Orcamento
    queryset = Orcamento.objects.order_by("-periodo")
    template_name = 'orcamento/lista.html'


class OrcamentoUpdate(UpdateView):
    model = Orcamento
    fields = ['ordem', 'descricao', 'valor', 'categoria', 'periodo', 'fixo', 'credito']
    template_name = 'orcamento/form.html'
    success_url = reverse_lazy('listar-orcamento')


class OrcamentoDelete(DeleteView):
    model = Orcamento
    template_name = 'orcamento/form-excluir.html'
    success_url = reverse_lazy('listar-orcamento')
