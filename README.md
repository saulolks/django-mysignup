# django-mysignup
Repositório para desenvolvimento de APIs REST para cadastro, login e obtenção de informações de usuário.

# Tecnologias utilizadas
- Python 3.6
- Django 3.1.3
- Guicorn 20.0.4
- JSON Web Token
- Django ORM
- UUID4
- SQLite

# Acesso às APIs
O acesso as APIs são feitas pela seguinte URL: https://django-mysignup.herokuapp.com e os endpoints são os seguintes:

- [POST] /signup
  - Dados deverão ser passados no body.
- [POST] /signin
  - Dados deverão ser passados no body.
- [GET] /me
  - Dado deverá ser passado no header, no campo Authorization.

# Estrutura dos dados
O sistema consiste de três tabelas: User, Phone e Token.

## User
Esta tabela contém as seguintes colunas:
- id
- firstname
- lastname
- password
- email
- created_at
- last_login

A senha é encriptografada utilizando SHA256, criptografia que não possibilita o processo de engenharia reversa.

## Phones
Esta tabela contém as seguintes colunas:
- id
- user
- number
- country_area
- country_code

## Token
Esta tabela contém as seguintes colunas:
- id
- user
- hash
- timestamp

O timestamp representa o horário que o último hash foi gerado, para validar seu tempo e expiração. Os tokens são gerados via UUID4.

# Autenticação
É utilizado JWT para a autenticação no sistema. Este padrão encapsula o payload e criptografa. O payload do JWT é formado pelo Id do usuário e o token associado a ele.

No momento da verificação, além desencriptar, o sistema compara o token com o salvo no banco de dados e o usuário o qual pertence. Por fim, ainda verifica se o token não está expirado.

Para fins de testes, o tempo escolhido para expiração do token foi 3 minutos.