# ENCOM - Package Control System

## Project Overview

ENCOM (Encomendas/Package Control System) is a Django-based web application designed to manage packages transported on passenger buses. The system enables bus companies to track packages sent between different cities and agencies, manage billing, generate reports, and maintain complete control over the package transportation business.

## Technology Stack

- **Framework**: Django 2.2.28
- **Python Version**: 3.5+
- **Database**: MySQL (with mysqlclient 1.4.6)
- **Admin Interface**: Django JET 1.0.8 (enhanced admin UI)
- **Key Dependencies**:
  - django-fast-paginator 1.0.4 (performance optimization)
  - django-localflavor 3.0.1 (Brazilian state choices)
  - python-stdnum 1.14 (standard number validation)
  - pytz 2020.1 (timezone handling)

## Project Structure

```
encomPython/
├── mysite/                 # Django project configuration
│   ├── settings.py        # Project settings (DB, apps, middleware)
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI application entry point
├── encom/                 # Main application
│   ├── models.py          # Data models (11 core models)
│   ├── views.py           # View logic (DetailViews)
│   ├── admin.py           # Admin interface configuration
│   ├── urls.py            # App URL patterns
│   ├── templates/         # HTML templates
│   │   ├── admin/        # Customized admin templates
│   │   └── encom/        # Report and receipt templates
│   ├── templatetags/      # Custom template tags
│   └── migrations/        # Database migrations
├── static/                # Static files (CSS, JS, images)
│   ├── admin/
│   ├── jet/
│   └── img/
├── env/                   # Virtual environment
├── db.sqlite3            # SQLite database (fallback)
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## Core Data Models

### 1. **Venda (Sale/Shipment)** - Primary transaction model
- Tracks package shipments between locations
- Links: Cliente (origin/destination), Localidade (origin/destination), Carro, Motorista, Empresa
- Payment tracking: dinheiro (cash), cartão (card), a_prazo (credit)
- Includes inline Items (produtos/products)
- Status: ATIVA or CANCELADA
- Freight responsibility: REMETENTE, DESTINATARIO, REDESPACHO
- Auto-saves user and agencia (agency/group) on creation

### 2. **Cliente (Customer)**
- Stores customer information
- Fields: nome, endereco, bairro, cidade, uf, cep, telefone, email
- Auto-uppercase on save for consistency

### 3. **Localidade (Location)**
- Brazilian cities/locations
- Uses STATE_CHOICES from django-localflavor
- Auto-uppercase on save

### 4. **Agencia (Agency)**
- Branch offices linked to locations
- Used for multi-tenant access control via Django Groups

### 5. **Produto (Product)**
- Package types with pricing
- Fields: nome, valor (decimal)

### 6. **Item**
- Junction model between Venda and Produto
- Tracks quantity (qtde) of each product in a sale

### 7. **Motorista (Driver)**
- Driver information: chapa, nome, cpf
- Can have primary and reserve drivers per trip

### 8. **Carro (Vehicle/Bus)**
- Bus/vehicle identification

### 9. **Empresa (Company)**
- Company/carrier information
- Fields: nome, cnpj, ie

### 10. **ExcessoBagagem (Excess Baggage)**
- Separate billing for excess baggage
- Similar structure to Venda but simplified
- Printable receipts

### 11. **Recebimento (Receipt/Reception)**
- Tracks when packages are received at destination
- OneToOne relationship with Venda
- Date tracking for delivery confirmation

### 12. **Manifesto (Manifest)**
- Daily vehicle manifests
- Groups all shipments by date, vehicle, and agency
- Auto-calculates total volumes

### 13. **Relatorio (Report)**
- Report generation model
- Types: ENVIO, EXCESSO DE BAGAGEM, RECEBIMENTO, GERAL
- Date range filtering
- Calculates financial totals

### 14. **Listagem (Listing)**
- Generic listing generator (currently: customer lists)

## Database Configuration

### Current Setup (settings.py:89-102)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'encomp',
        'USER': 'encomp',
        'PASSWORD': 'admtecacai',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**SECURITY WARNING**: Database credentials are currently hardcoded in settings.py. For production deployment:
1. Move credentials to environment variables
2. Use python-decouple or django-environ
3. Never commit `.env` files to version control

## Key Conventions and Patterns

### 1. **Multi-Tenancy via Groups**
- System uses Django Groups as "Agencias" (agencies)
- Special group "GERCOM" has super-admin privileges
- Non-GERCOM users only see their agency's data
- Implemented in ModelAdmin.get_queryset() methods

### 2. **Automatic Field Population**
```python
def save_model(self, request, obj, form, change):
    if getattr(obj, 'usuario', None) is None:
        obj.usuario = request.user
    if getattr(obj, 'agencia', None) is None:
        obj.agencia = request.user.groups.first()
    obj.save()
```
- Current user and their agency are auto-assigned to records
- Never override these manually

### 3. **Text Normalization**
- Many models auto-uppercase text fields on save
- Maintains data consistency
- Examples: Cliente, Localidade, Empresa, Motorista

### 4. **Inline Editing**
- Venda uses ItemInline for adding products
- RequiredInlineFormSet ensures at least one item exists
- `extra = 1` provides one blank form

### 5. **Printable Documents**
- Models have `imprimir()` method returning HTML link
- Uses `get_absolute_url()` pointing to DetailView
- Templates generate printer-friendly receipts and manifests

### 6. **Fast Pagination**
```python
paginator = FastPaginator
list_per_page = 50
FAST_PAGINATION_TIMEOUT = 5
```
- Uses django-fast-paginator for performance
- Avoids slow COUNT(*) queries on large tables

### 7. **Localization**
- Language: Brazilian Portuguese (pt-br)
- Timezone: 'Etc/GMT+3'
- Date format: d/m/Y (DD/MM/YYYY)
- Decimal separator: comma
- Thousand separator: enabled

### 8. **Readonly Fields by Permission**
```python
def get_readonly_fields(self, request, obj=None):
    rfo = super(VendaAdmin, self).get_readonly_fields(request, obj)
    if not request.user.groups.filter(name__iexact='GERCOM').exists():
        rfo += ('situacao_venda',)
    return rfo
```
- Non-admin users cannot cancel sales (change situacao_venda)

## URL Structure

### Admin Interface
- `/` - Django admin (main interface)
- `/jet/` - Django JET URLs

### App URLs (prefix: `/encom/`)
- `/encom/venda/<id>` - Print sale receipt
- `/encom/relatorio/<id>` - View report
- `/encom/excessobagagem/<id>` - Print excess baggage receipt
- `/encom/manifesto/<id>` - Print manifest
- `/encom/listagem/<id>` - View listing

All views require login (wrapped with `login_required`)

## Development Workflow

### Initial Setup
```bash
# Create virtual environment
python -m venv env
source env/bin/activate  # Linux/Mac
# or: env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure database
# Edit mysite/settings.py with correct MySQL credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Making Model Changes
1. Edit models in `encom/models.py`
2. Create migration: `python manage.py makemigrations`
3. Review migration file in `encom/migrations/`
4. Apply migration: `python manage.py migrate`
5. Update admin.py if needed (list_display, fieldsets, etc.)

### Adding New Features
1. **Model first**: Define data structure in models.py
2. **Admin second**: Register in admin.py with appropriate AdminClass
3. **Views (if needed)**: Add DetailView or ListView in views.py
4. **URLs**: Map URL pattern in urls.py
5. **Templates**: Create HTML template in encom/templates/encom/

### Testing
- No automated tests currently exist (tests.py is empty)
- Manual testing through admin interface
- **RECOMMENDATION**: Add tests for:
  - Model validation (unique_together constraints)
  - Permission checks (agency filtering)
  - Calculation methods (valor_nota, desconto, totalvolumes)
  - Report generation accuracy

## Security Considerations

### Current Issues (DO NOT IGNORE)
1. **SECRET_KEY exposed** in settings.py - Move to environment variable
2. **DEBUG = True** in production - Set to False for production
3. **Database credentials** hardcoded - Use environment variables
4. **ALLOWED_HOSTS** contains production IPs - Review for current deployment
5. **No HTTPS enforcement** - Add security middleware for production

### Recommended Actions Before Production
```python
# In settings.py (or better, use environment variables):
import os
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
    }
}

# Add security middleware
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Access Control Pattern
```python
# Always filter by agency for non-admin users:
def get_queryset(self, request):
    qs = super(YourAdmin, self).get_queryset(request)
    if not (request.user.is_superuser or request.user.groups.filter(name__iexact='GERCOM').exists()):
        return qs.filter(agencia=request.user.groups.first())
    return qs
```

## Important Model Methods

### Venda
- `valor_nota()` - Calculates total bill (dinheiro + cartao)
- `valortotal()` - Sum of all items (produto.valor × qtde)
- `desconto()` - Difference between valortotal and valor_nota
- `total()` - Total quantity of items in this sale
- `totalvolumes()` - Total volumes for the date (all sales)

### Manifesto
- `totalvolumes()` - Total volumes for date + vehicle + agency

### Relatorio
- `get_valor()` - Total value for date range (by agency)
- `get_valor_geral()` - Total value for date range (all agencies)
- `get_valor_recebimento()` - Received packages value
- `get_valor_excessobagagem()` - Excess baggage total

## Template System

### Key Templates
- `encom/testerionorte.html` - Sale receipt (Venda)
- `encom/recibo_excesso_bagagem.html` - Excess baggage receipt
- `encom/venda_data_list_rionorte.html` - Sales report
- `encom/manifesto_data_list_rionorte.html` - Manifest printout
- `encom/listagem.html` - Customer listing

### Custom Template Tags
Located in `encom/templatetags/encom_tags.py`
- Use: `{% load encom_tags %}` in templates

### Admin Customization
- `admin/change_form.html` - Custom change form
- `admin/change_list.html` - Custom list view
- `admin/login.html` - Custom login page

## Static Files

### Configuration
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
MEDIA_ROOT = os.path.join(PROJECT_ROOT_PATH, 'media/')
MEDIA_URL = '/media/'
```

### Deployment
For production, collect static files:
```bash
python manage.py collectstatic
```

Configure Apache/Nginx to serve static files directly.

## Common Tasks for AI Assistants

### Adding a New Field to Venda
1. Add field to Venda model in models.py
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Add field to VendaAdmin.fieldsets in admin.py
5. Optionally add to list_display if needed in list view
6. Update templates if field should appear in receipts

### Creating a New Report Type
1. Add report type to TIPOS choices in models.py (Relatorio)
2. Add method in Relatorio class to calculate values (e.g., `get_valor_newtype()`)
3. Update RelatorioForm in admin.py with new choice
4. Create or modify template to display new report data
5. Update RelatorioDetail view if custom logic needed

### Adding Permission-Based Features
```python
# Check if user is in GERCOM group:
if request.user.groups.filter(name__iexact='GERCOM').exists():
    # Admin-only code

# Get user's agency:
user_agency = request.user.groups.first()

# Filter queryset by agency:
qs = qs.filter(agencia=user_agency)
```

### Debugging Tips
1. Check migrations are applied: `python manage.py showmigrations`
2. Access shell for testing: `python manage.py shell`
3. Check for errors in console when running dev server
4. Use Django Debug Toolbar for query optimization (add to INSTALLED_APPS)
5. Check logs for admin actions: Django admin has built-in logging

## Known Technical Debt

1. **Duplicate get_queryset methods** in some Admin classes (RelatorioAdmin, ExcessoBagagemAdmin, ManifestoAdmin)
2. **No automated tests** - Critical for preventing regressions
3. **Hardcoded credentials** - Security risk
4. **Mixed Portuguese/English** in code - Consider standardizing
5. **Commented-out code** should be removed or documented
6. **No API endpoints** - Consider REST API if mobile app needed
7. **backup files** (*.save, *.save.1) should be in .gitignore

## Git Branch Strategy

- Main branch: `master` (Portuguese spelling matches repo)
- Development happens on feature branches with prefix `claude/`
- All Claude Code sessions use branches starting with `claude/` and ending with session ID

## Environment Setup Checklist

When setting up development environment:
- [ ] Python 3.5+ installed
- [ ] MySQL server running
- [ ] Database 'encomp' created
- [ ] User 'encomp' with proper permissions
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Migrations applied (`python manage.py migrate`)
- [ ] Superuser created
- [ ] Groups created in admin (at minimum: GERCOM)
- [ ] Test data loaded (optional)

## Additional Notes

### Django JET Themes
System supports multiple color themes (default, green, light-green, light-violet, light-blue, light-gray). Users can select in admin interface.

### Allowed Hosts
Current configuration includes multiple IPs/domains. Review and update based on actual deployment:
- localhost / 127.0.0.1 (development)
- buscoop.pythonanywhere.com (PythonAnywhere deployment)
- Various internal IPs (10.0.0.16, 192.168.x.x)

### Related Documentation
- Django 2.2 docs: https://docs.djangoproject.com/en/2.2/
- Django JET: https://jet.readthedocs.io/
- Django Localflavor: https://django-localflavor.readthedocs.io/

---

**Last Updated**: December 2025
**Maintained By**: AI Assistant (Claude Code)
**Project Repository**: https://github.com/jallisson/encomPython
