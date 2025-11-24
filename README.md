# Binary Trees and Balancing

## Instalação

### Pré-requisitos
- Python 3.7 ou superior

### Configuração do Ambiente

#### 1. Criar o ambiente virtual
```bash
python -m venv venv
```

#### 2. Ativar o ambiente virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

#### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### Desativar o ambiente virtual
Quando terminar de trabalhar no projeto, você pode desativar o ambiente virtual com:
```bash
deactivate
```

## Instalação do Graphviz

Para visualizar as árvores graficamente, é necessário instalar o Graphviz no sistema.

### Passo 1: Instalar a biblioteca Python
```bash
pip install graphviz
```

### Passo 2: Instalar o executável Graphviz

#### Windows

**Opção 1 - Via winget (recomendado):**
```powershell
winget install graphviz
```

**Opção 2 - Download manual:**
1. Acesse: https://graphviz.org/download/
2. Baixe o instalador para Windows
3. Execute o instalador
4. **IMPORTANTE:** Marque a opção "Add Graphviz to PATH"
5. Reinicie o terminal/IDE após a instalação

#### Linux
```bash
sudo apt install graphviz
```

#### Mac
```bash
brew install graphviz
```

### Verificar instalação
Após instalar, reinicie o terminal e execute:
```bash
dot -V
```

Se o comando retornar a versão do Graphviz, a instalação foi bem-sucedida.
