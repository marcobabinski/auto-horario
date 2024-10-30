# Auto-Horario
Repositório da PPI de 2024/2 referente ao desenvolvimento da plataforma Auto-horário para a APAE FW

## Instalação
#### 1 Instalar o GIT
Acesse o site oficial do git, na página de downloads para windows, no link  https://git-scm.com/downloads/win e baixe a versão compatível com a versão do seu sistema operacional. 
<br/>
#### 2 Clonar o repositório
Abra o terminal do git (gitBash) e execute o comando `git clone https://github.com/marcobabinski/auto-horario.git`, para clonar o repositório do github para o seu computador.
<br/>
#### 3 Instalar o python
Acesse o link de download no site oficial do python https://www.python.org/downloads/ e faça o download de uma versão do python (acima do 3.12).
<br/>
#### 4 Criar virtualenv
O objetivo de criar um ambiente virtual (virtualenv) é isolar o gerenciamento de pacotes do Python, evitando conflitos entre bibliotecas de diferentes projetos. Para criar um ambiente virtual, você deve executar o comando `python -m venv venv`, que criará uma pasta chamada venv na raiz do seu projeto. Esta pasta conterá uma instalação isolada do Python e suas bibliotecas.<br/>
    Após criar o ambiente virtual, é necessário ativá-lo. Primeiro, execute `Set-ExecutionPolicy Unrestricted` no PowerShell como administrador para permitir a execução de scripts. Em seguida, ative o ambiente virtual com o comando `venv\Scripts\activate`. Ao ativar, você verá o nome do ambiente (venv) na linha de comando, indicando que todos os comandos subsequentes usarão o Python e as bibliotecas do ambiente virtual.
<br/>
#### 5 Instalar dependencias venv
Após ativar o ambiente virtual, o próximo passo é instalar as dependências necessárias para o seu projeto. Isso é feito com o comando `pip install -r requirements.txt`, que lê o arquivo requirements.txt e instala todas as bibliotecas listadas. Essa etapa é crucial para garantir que o projeto tenha todas as dependências corretas, evitando problemas de compatibilidade.
<br/>
#### 6 Instalar node
Para desenvolver o projeto, você precisará instalar o Node.js. Acesse o link Download https://nodejs.org/pt/download/prebuilt-installer e baixe o instalador apropriado para o seu sistema operacional. Após a instalação, você terá acesso ao Node.js e ao npm (Node Package Manager), que são essenciais para o desenvolvimento e gerenciamento de pacotes.
<br/>
#### 7 Instalar dependencias node
Com o Node.js instalado, o próximo passo é instalar as dependências do projeto definidas no arquivo package.json. Para isso, navegue até a raiz do projeto e execute o comando `npm install`. Este comando irá buscar todas as dependências necessárias e instalá-las, assim como o pip faz para o Python.
<br/>
#### 8 Instalar o modulo de refresh automático (TBD)
<br/>

<<<<<<< HEAD
> Quote block
=======
## Execução (desenvolvimento)

### 1. Entrar na venv

Para começar a desenvolver, você precisa ativar o ambiente virtual. Execute o seguinte comando:

`venv\Scripts\activate`

Com o ambiente virtual ativado, todas as dependências do Python instaladas anteriormente estarão disponíveis.

### 2. Rodar o compiler tailwind
Para compilar os estilos do Tailwind CSS durante o desenvolvimento, utilize o comando a seguir. Certifique-se de que você está na raiz do projeto:

`npm run dev` 

### 3. Rodar o runserver
Finalmente, para iniciar o servidor do projeto, execute o seguinte comando na raiz do projeto:

`python.exe .\manage.py runserver`

Após rodar este comando, o servidor estará em execução, e você poderá acessar a aplicação no navegador. Normalmente, a URL será http://127.0.0.1:8000/
>>>>>>> cfe3fcae488e3dcf2c9d6ccd2ccd1c2d1f93a6d6
