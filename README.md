# mamaa-api
API to access mamaa stock data in near real time.

## Como rodar
1. Abra o seu editor favorito na raiz do projeto
2. Com o python instalado, crie um abiente virtual e ative-o
   1. Rode o comando `python =m venv venv` e aguarde.
   2. Se você estiver no windows, rode o comando `.\venv\Scripts\activate` para entrar dentro do ambiente virtual. Se você estiver no Linux ou Mac, rode o comando `. venv/bin/activate`. Após isso, você deverá ver um `(venv)` no início da sua linha de comando.
3. Com o ambiente virtual ativo, atualize o gerenciador de pacotes `pip` rodando o comando `pip install --upgrade pip` (aqui, se você estiver no Windows, pode ser que ele dê uma mensagem de erro, mas não se preocupe, pois é um alarme falso. Você pode verificar a versão instalada do pip rodando o comando `pip --version`).
4. Após isso, execute o comando `pip install -r requirements.txt` para instalar todas as dependências do projeto.
5. Por fim, com o Docker previamente instalado na sua máquina, rode o comando `docker-compose up` para subir tanto a API de Flask, quanto o banco de dados Redis (fizemos assim para eliminar a necessidade de você ter que instalar o redis na sua máquina).

## Disclaimers
- Hosts, senhas, portas e outras informações foram colocadas como variáveis de ambiente num arquivo `.env` **não versionado**. Consulte os devs para obter esse valores, ou então acesse as ocnfigurações do repositório do GitHub que você conseguirá ver.
