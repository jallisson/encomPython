ENCOM Build Status
Distinção e Complexidade

Vamos imaginar em uma empresa de transportes de passageiros que quer faturar um pouco mais com o transporte de objetos em pacotes pequenos como, por exemplo, um ‘smartphone’, notebook ou uma simples carta entre as cidades que os passageiros serão levados, pois no bagageiro dos ônibus tem espaço suficiente para esse serviço, mas sem um ‘software’ de gestão fica complicado saber o destino do pacote e o faturamento que a empresa esteve com os pacotes transportados, além disso, um pacote perdido entre as viagens pode se tornar um problema ainda maior. Sendo assim usando a tecnologia do framework DJANGO-PYTHON, o sistema ENCOM tem sua complexidade ideal para essa gestão, pois dispõe de vários módulos sólidos e é um sistema estável que funciona com vários relacionamentos de tabelas que no final o torna bom para o uso em que foi designado ser para a gerenciamento dos pacotes transportado nos ônibus de passageiros.

ENCOM

Encom – Sistema de Controle de Pacotes é um sistema (web) desenvolvido para controle de pacotes que possa ser levado em ônibus de passageiro, onde uma empresa de ramo de transporte de passageiros poderá perfeitamente utilizar para a gestão e controle dos (pacotes) transportadas em diferentes ônibus para diferentes agências de várias cidades, assim a empresa que utilizar do sistema terá controle de qual cidade e agência partiu a encomenda e qual o seu destino, o encom disponibilizara de relatórios financeiros demonstrando o valor de todos os pacotes envidas, recebidas, com excesso de bagagem e um relatório geral demonstrado o lucro líquido de todas pacote independente da agência responsável pela encomenda, no sistema terá o cadastro de grupo que é a agência em específico, e contara com cadastro de usuário, carros, clientes, empresas, excesso de bagagem, localidade, manifesto, motorista, produtos, recebimentos relatórios e vendas, assim a empresa de ônibus terá todo controle financeiro e quantitativo de pacotes envidas e recebidas entre agências e cidades.

2022-04-14 (6)

image

image

image

Dependências
Python - Versão 3.5+
django == 2.2.1
apache2 (Opcional)
mod_wsgi (Opcional)
Instalação:
Instalar as bibliotecas/pacotes (no Linux):

Instalar dependências:

pip install -r requirements.txt
Sincronize a base de dados:
python manage.py migrate
Crie um usuário (Administrador do sistema):
python manage.py createsuperuser
Teste a instalação carregando o servidor de desenvolvimento (http://localhost:8000 no navegador):
python manage.py runserver
Implementações
Cadastro de carros, clientes, empresas, excessos de pacotes, localidades, manifestos, motoristas, produtos, recebimento, relatórios e vendas
Login/Logout
Criação de perfil para cada usuário.
Definição de permissões para usuários.
Criação e geração de relátorios (financeiros com valores de cada envio separado por agência)
Interface simples e em português
Créditos
jallisson
Ajuda
Como este é um projeto em desenvolvimento, qualquer feedback será bem-vindo.

© 2022 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About

