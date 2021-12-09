from django.urls import path
from django.conf.urls import include, url 
from django.views.generic.base import TemplateView
from django.views.generic.base import RedirectView


from . import views
from .views import VendaDetail
#from .views import RelatorioListView
from .views import RelatorioDetail
from .views import ExcessoBagagemDetail
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #path('', views.index, name='index'),
    #url(r'^venda/(?P<pk>\d+)/$', VendaDetail.as_view(), name='venda_detail'),
    #path(r'^venda/(?P<pk>\d+)/$', VendaDetail.as_view(), name='venda_detail'),
    path('venda/<int:pk>', login_required(views.VendaDetail.as_view(template_name='encom/testerionorte.html')), name='venda_detail'),
	#url(r'^lista/(?P<pk>\d+)/$', RelatorioListView.as_view(), name='venda_list'),
	#url(r'^relatorio/(?P<pk>\d+)/$', RelatorioDetail.as_view(), name='venda_data_list'),
	path('relatorio/<int:pk>', login_required(views.RelatorioDetail.as_view(template_name='encom/venda_data_list_rionorte.html')), name='venda_data_list'),
	
	#url(r'^excessobagagem/(?P<pk>\d+)/$', ExcessoBagagemDetail.as_view(), name='bagagem_data_list'),
	path('excessobagagem/<int:pk>', login_required(views.ExcessoBagagemDetail.as_view(template_name='encom/recibo_excesso_bagagem.html')), name='excessobagagem_detail'),
	path('manifesto/<int:pk>', login_required(views.ManifestoDetail.as_view(template_name='encom/manifesto_data_list_rionorte.html')), name='manifesto_detail'),

]
