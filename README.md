# ENCOM [![Build Status](https://travis-ci.org/thiagopena/djangoSIGE.svg?branch=master)](https://travis-ci.org/thiagopena/djangoSIGE)

Distinction and Complexity

Let's imagine a passenger transport company that wants to earn a little more with the transport of objects in small packages such as, for example, a 'smartphone', notebook or a simple letter between the cities that passengers will be taken, because in the luggage compartment of the buses has enough space for this service, but without management software it is difficult to know the destination of the package and the company's billing with the packages transported, in addition, a package lost between trips can become a problem even bigger. Therefore, using the technology of the DJANGO-PYTHON framework, the ENCOM system has its ideal complexity for this management, as it has several solid modules and is a stable system that works with several table relationships, which in the end makes it good for use in which was designed to be for the management of packages carried on passenger buses.

ENCOM 

Encom – Package Control System is a system (web) developed to control packages that can be taken on passenger buses, where a passenger transport company can perfectly use for the management and control of (packages) transported in different buses to different agencies of different
cities, so the company that uses the system will have control of which city and agency the order left and what its destination, the order will make available
financial reports showing the value of all packages sent, received, with excess baggage and a general report showing the net income of all
package independent of the agency responsible for the order, the system will have the group registration that is the specific agency, and will have a user registration,
cars, customers, companies, excess baggage, location, manifest, driver, products, receipts, reports and sales, so the bus company will have all
financial and quantitative control of packages sent and received between agencies and cities.

![2022-04-14 (6)](https://user-images.githubusercontent.com/43224822/163429994-fcd09daa-98d1-4960-8131-89ca512ca027.jpg)


## Dependencies

- [Python](https://www.python.org/downloads/) - Versão 3.5+
- [django](http://www.djangoproject.com) == 2.2.1
- [apache2](https://www.apache.org/) (Opcional)
- [mod_wsgi](https://modwsgi.readthedocs.io/en/develop/) (Opcional)

## Installation:

0. Install the libraries/packages (on Linux):

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Synchronize the database:

```bash
python manage.py migrate
```

3. Create a user (System Administrator):

```bash
python manage.py createsuperuser
```

4. Test the installation by loading the development server (http://localhost:8000 in the browser):

```bash
python manage.py runserver
```

## Implementations

- Registration of cars, customers, companies, excess packages, locations, manifests, drivers, products, receipt, reports and sales
- Login/Logout
- Profile creation for each user.
- Definition of permissions for users.
- Creation and generation of reports (financial with values of each shipment separated by agency)
- Simple interface and in Portuguese

## credits

- [jallisson](https://github.com/jallisson)


## Help

As this is an ongoing project, any feedback is welcome.
