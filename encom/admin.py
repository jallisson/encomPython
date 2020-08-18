from django.contrib import admin
from .models import Carro
from .models import Localidade
from .models import Cliente
from .models import Empresa
from .models import Produto
from .models import Motorista
from .models import Venda
from .models import Item
from .models import Relatorio
from .models import Recebimento
from .models import ExcessoBagagem
from .models import Manifesto
from django import forms
from django.forms.models import BaseInlineFormSet

class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1
    formset = RequiredInlineFormSet

    #tava na VendaAdmin
    #form = RequerenteForm
    #list_per_page = 50
    #search_fields = ('localidade_origem', 'localidade_destino', 'tipo_frete', 'responsavel_frete', 'cliente_origem', 'cliente_destino','valor_nota','data_venda', 'situacao_venda')

class VendaAdmin(admin.ModelAdmin):
    
	 
    list_display = ('id', 'imprimir', 'agencia', 'localidade_origem', 'localidade_destino', 'tipo_frete', 'responsavel_frete', 'get_clienteo', 'get_cliented', 'valor_nota', 'data_venda', 'situacao_venda', 'usuario',)#, 'lista')
    list_filter = ('id',)
    inlines = [ItemInline]
    list_per_page = 10
    search_fields = ('id',)
    
    fieldsets = [
            ('Dados Principais', {
                'classes': ('suit-tab', 'suit-tab-general',),
                'fields': ['responsavel_frete', 'hora_saida',  'empresa', ('localidade_origem', 'localidade_destino'), ('cliente_origem', 'cliente_destino'),'carro' , ('motorista_principal', 'motorista_reserva'), 'situacao_venda'],
            }),
        	('Tipo de Pagamento', {
            	'classes': ('suit-tab', 'suit-tab-general',),
                'fields': [('dinheiro'), ('valor_dinheiro'), ('cartao'), ('valor_cartao', 'cartoes'), ('tipo_frete')]#, 'valor_nota'] #'produto']
            	#'fields': [('dinheiro', 'american_express', 'cred_shop'), ('master_card', 'visa', 'dinner_clubs'), ('valor_dinheiro', 'valor_cartao'),('tipo_frete')]#, 'valor_nota'] #'produto']
        	}),]

    class Meta:
             model = Venda
    
    def get_queryset(self, request):
        qs = super(VendaAdmin, self).get_queryset(request)
        
        if not self.agencia == 'GERCOM':
         return qs.filter(agencia=request.user.groups.first())	
        else:
         
         return qs.filter()
   
    def get_queryset(self, request):
        qs = super(VendaAdmin, self).get_queryset(request)
        if not (request.user.is_superuser or request.user.groups.filter(name__iexact='GERCOM').exists()):         
         return qs.filter(agencia=request.user.groups.first())
        else:
         return qs.filter()

        

    """
    def get_queryset(self, request):
        qs = super(VendaAdmin, self).get_queryset(request)
        if not request.user.groups.filter(name__iexact='GERCOM').exists():
         return qs.filter(agencia=request.user.groups.first())   
        else:
        
         return qs.filter()

    """      
    
    def save_model(self, request, obj, form, change):
            if getattr(obj, 'usuario', None) is None:
                    obj.usuario = request.user
            if getattr(obj, 'agencia', None) is None:
                    obj.agencia = request.user.groups.first()
            obj.save()
    

    def get_clienteo(self, obj):

        return obj.cliente_origem.nome

    #get_name.admin_order_field  = 'name'  #Allows column order sorting

    get_clienteo.short_description = 'Cliente Origem'  #Renames column head

    def get_cliented(self, obj):

        return obj.cliente_destino.nome

    #get_name.admin_order_field  = 'name'  #Allows column order sorting

    get_cliented.short_description = 'Cliente Destino'  #Renames column head

    def get_readonly_fields(self, request, obj=None):
    	user_group = request.user.groups.values_list('name', flat=True)
    	rfo = super(VendaAdmin, self).get_readonly_fields(request, obj)
    	if not request.user.groups.filter(name__iexact='GERCOM').exists():
    	 rfo += ('situacao_venda',)
    	return rfo

class RelatorioForm(forms.ModelForm):
    TIPOS = (
        ('ENVIO', 'ENVIO'),
        ('RECEBIMENTO', 'RECEBIMENTO'),
        ('GERAL', 'GERAL'),
        
    )
    tipo = forms.CharField(widget=forms.RadioSelect(attrs={'class': 'inline'}, choices=TIPOS), initial='ENVIO')
    class Meta:
        model = Relatorio
        fields = ['tipo',]


class RelatorioAdmin(admin.ModelAdmin):

   list_display = ('id','data_inicial', 'data_final', 'tipo', 'agencia', 'usuario','imprimir',)
   list_per_page = 50
   form = RelatorioForm

   class Meta:
             model = Relatorio

   fieldsets = [
            ('Dados Principais', {
                'classes': ('suit-tab', 'suit-tab-general',),
                'fields': ['data_inicial', 'data_final', 'tipo', 'agencia'],
            }),]

   def save_model(self, request, obj, form, change):
            if getattr(obj, 'usuario', None) is None:
                    obj.usuario = request.user
            #if getattr(obj, 'agencia', None) is None:
            #        obj.agencia = request.user.groups.first()
            obj.save()

    

class CarroAdmin(admin.ModelAdmin):

   list_display = ('nome',)
   list_per_page = 50
   search_fields = ('nome',)
   ordering = ('nome',)

   class Meta:
             model = Carro

class LocalidadeAdmin(admin.ModelAdmin):

   list_display = ('nome','uf',)
   list_per_page = 50
   search_fields = ('nome',)
   ordering = ('nome',)

   class Meta:
             model = Localidade

class AgenciaAdmin(admin.ModelAdmin):

   list_per_page = 50


class ClienteAdmin(admin.ModelAdmin):

   list_display = ('nome','endereco','email',)
   list_per_page = 50
   search_fields = ('nome',)
   ordering = ('nome',)

   class Meta:
             model = Cliente
   

class EmpresaAdmin(admin.ModelAdmin):

   list_display = ('nome','cnpj','ie',)
   list_per_page = 50
   search_fields = ('nome', 'cnpj',)
   ordering = ('nome',)

   class Meta:
             model = Empresa

class ProdutoAdmin(admin.ModelAdmin):

   list_display = ('nome','valor',)
   list_per_page = 50
   search_fields = ('nome',)
   ordering = ('nome',)

   class Meta:
             model = Produto

class MotoristaAdmin(admin.ModelAdmin):

   list_display = ('chapa','nome','cpf',)
   list_per_page = 50
   search_fields = ('nome','chapa','cpf',)
   ordering = ('nome',)

   class Meta:
             model = Motorista

class ExcessoBagagemAdmin(admin.ModelAdmin):

   list_display = ('id','empresa','hora_saida', 'data', 'carro', 'quantidade', 'cliente', 'intinerario_origem','intinerario_destino','imprimir',)
   list_per_page = 50
   search_fields = ('id','carro','cliente')
   ordering = ('cliente',)

   class Meta:
             model = ExcessoBagagem

   fieldsets = [
            ('Dados Principais', {
                'classes': ('suit-tab', 'suit-tab-general',),
                'fields': ['empresa','hora_saida', 'data', 'carro', 'quantidade', 'cliente', 'intinerario_origem','intinerario_destino', 'item', 'valor'],
            }),]


   def save_model(self, request, obj, form, change):
            if getattr(obj, 'usuario', None) is None:
                    obj.usuario = request.user
            #if getattr(obj, 'agencia', None) is None:
            #        obj.agencia = request.user.groups.first()
            obj.save()

class RecebimentoAdmin(admin.ModelAdmin):
   
   #list_filter = ('usuario',)
   list_display = ('venda', 'data_recebimento', 'agencia', 'usuario',)
   list_per_page = 50
   search_fields = ('venda',)

   class Meta:
             model = Recebimento

   fieldsets = [
            ('Dados Principais', {
                'classes': ('suit-tab', 'suit-tab-general',),
                'fields': ['venda'],
            }),]

   def save_model(self, request, obj, form, change):
            if getattr(obj, 'usuario', None) is None:
                    obj.usuario = request.user
            if getattr(obj, 'agencia', None) is None:
                    obj.agencia = request.user.groups.first()
            obj.save()

class ManifestoAdmin(admin.ModelAdmin):
   
   #list_filter = ('usuario',)
   list_display = ('data_venda', 'carro', 'usuario', 'imprimir',)
   list_per_page = 50
   search_fields = ('data_venda',)

   class Meta:
             model = Manifesto

   fieldsets = [
            ('Dados Principais', {
                'classes': ('suit-tab', 'suit-tab-general',),
                'fields': ['data_venda', 'carro'],
            }),]

   def save_model(self, request, obj, form, change):
            if getattr(obj, 'usuario', None) is None:
                    obj.usuario = request.user
            #if getattr(obj, 'agencia', None) is None:
             #       obj.agencia = request.user.groups.first()
            obj.save()



#class ProdutoInline(admin.TabularInline):
#   model = Produto


admin.site.register(Carro, CarroAdmin)
admin.site.register(Localidade, LocalidadeAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Motorista, MotoristaAdmin)
admin.site.register(Venda, VendaAdmin)
admin.site.register(Relatorio, RelatorioAdmin)
admin.site.register(Recebimento, RecebimentoAdmin)
admin.site.register(ExcessoBagagem, ExcessoBagagemAdmin)
admin.site.register(Manifesto, ManifestoAdmin)