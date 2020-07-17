# -- coding: utf-8 --
#from _future_ import unicode_literals

from django.shortcuts import render

from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.contrib.auth.models import User, Group
from .models import Venda
from .models import Recebimento
from .models import Relatorio
from .models import ExcessoBagagem
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class VendaDetail(DetailView):
    model = Venda

    def get_template_names(self):
        pk = self.kwargs['pk']
        obj = Venda.objects.get(pk=pk)
        #return 'encom/qualquer.html'
        return 'encom/teste.html'


class ExcessoBagagemDetail(DetailView):
    model = ExcessoBagagem

    def get_template_names(self):
        pk = self.kwargs['pk']
        obj = ExcessoBagagem.objects.get(pk=pk)
        return 'encom/bagagem_data_list.html'



class RelatorioDetail(DetailView):
    model = Relatorio
    

    def get_template_names(self):
        pk = self.kwargs['pk']
        obj = Relatorio.objects.get(pk=pk)
        return 'encom/venda_data_list.html'
    
    def get_context_data(self, **kwargs):
        inicio = self.object.data_inicial
        fim = self.object.data_final
        grupo = self.object.agencia
        #usuario = self.object.usuario
        #usuario = self.object.usuario
        #eturn self.model.filter(user=request.user)
    	
        return dict(
            super(RelatorioDetail, self).get_context_data(**kwargs),
            venda_list = Venda.objects.filter(data_venda__range=[inicio, fim]).filter(agencia=grupo),
            recebimento_list = Recebimento.objects.filter(data_recebimento__range=[inicio, fim]).filter(usuario=self.request.user),
            geral_list = Venda.objects.filter(data_venda__range=[inicio, fim]),
            #recebimento_list = Recebimento.objects.filter(data_recebimento__range=[inicio, fim]).filter(usuario=self.request.user), filtro buscando usuario logado

        )


    
    


#class RelatorioListView(ListView):

#    model = Venda
#    paginate_by = 100  # if pagination is desired
#
#    def dispatch(self, request, *args, **kwargs):
#        return super(RelatorioListView, self).dispatch(request, *args, **kwargs)
