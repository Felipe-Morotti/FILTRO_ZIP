# Tutorial: Classificador de Arquivos em ZIP

> Este tutorial foi escrito para guiar qualquer pessoa — inclusive iniciantes — a replicar este projeto do zero em sua própria máquina.

---

## Sumário

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Requisitos de Hardware](#2-requisitos-de-hardware)
3. [Instalando o Python](#3-instalando-o-python)
4. [Instalando o Git](#4-instalando-o-git)
5. [Clonando o Repositório](#5-clonando-o-repositório)
6. [Criando e Ativando o Ambiente Virtual](#6-criando-e-ativando-o-ambiente-virtual)
7. [Instalando as Dependências](#7-instalando-as-dependências)
8. [Estrutura do Projeto](#8-estrutura-do-projeto)
9. [Como Executar](#9-como-executar)
10. [Saídas Esperadas](#10-saídas-esperadas)
11. [Solução de Problemas Comuns](#11-solução-de-problemas-comuns)

---

## 1. Visão Geral do Projeto

Este projeto realiza a **classificação automática de arquivos contidos em ZIPs**, organizando-os em categorias com base em seu tipo e conteúdo. Caso o arquivo seja um PDF, o sistema verifica ainda se ele se trata de um **DANFE** (Documento Auxiliar da Nota Fiscal Eletrônica) e, em caso afirmativo, se possui página de serviço (*PS*) anexada.

O pipeline é composto pelas seguintes etapas:

```
Arquivo .zip em raw_data/
        │
        ▼
[1] Extração e leitura dos arquivos contidos no ZIP
        │
        ▼
[2] Identificação do tipo de cada arquivo (PDF, JPG, XML...)
        │
        ▼
[3] Verificação: o PDF é um DANFE? Possui página de serviço?
        │
        ▼
[4] Classificação e movimentação para a pasta correta em filtered_data/
```

**Categorias de classificação:**

| Pasta de destino | Conteúdo |
|---|---|
| `filtered_data/jpg/` | Imagens JPG |
| `filtered_data/pdf/` | PDFs genéricos (não identificados como DANFE) |
| `filtered_data/pdf_danfe/` | PDFs identificados como DANFE com página de serviço |
| `filtered_data/pdf_danfe_no_ps/` | PDFs identificados como DANFE sem página de serviço |
| `filtered_data/pdf_no_ps/` | PDFs sem página de serviço (não DANFE) |
| `filtered_data/xml/` | Arquivos XML genéricos |
| `filtered_data/xml_danfe/` | Arquivos XML de NF-e (DANFE) |
| `filtered_data/quarentena/` | Arquivos não reconhecidos ou com erro na classificação |

**Principais bibliotecas utilizadas:**

| Biblioteca | Finalidade |
|---|---|
| `filetype` | Detecção do tipo real do arquivo pelo seu conteúdo binário |
| `pypdf` | Leitura e inspeção de arquivos PDF |
| `pathlib` | Manipulação de caminhos de arquivos |
| `logging` | Registro de logs durante a execução |

---

## 2. Requisitos de Hardware

Este projeto é **leve e roda inteiramente na CPU**. Não há necessidade de GPU.

| Componente | Mínimo |
|---|---|
| RAM | 4 GB |
| Espaço em disco | 1 GB livre (mais o espaço dos seus ZIPs) |
| Sistema Operacional | Windows, macOS ou Linux |

---

## 3. Instalando o Python

O projeto requer **Python 3.10 ou superior**.

### Verificando se o Python já está instalado

Abra um terminal (Prompt de Comando no Windows, Terminal no macOS/Linux) e execute:

```bash
python --version
```

ou

```bash
python3 --version
```

Se a versão exibida for `3.10.x` ou superior, pule para a [próxima seção](#4-instalando-o-git).

### Instalando o Python (caso necessário)

#### Windows

1. Acesse [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Clique em **"Download Python 3.x.x"** (versão mais recente)
3. Execute o instalador baixado
4. ✅ **IMPORTANTE:** Marque a opção **"Add Python to PATH"** antes de clicar em *Install Now*
5. Conclua a instalação e reabra o terminal

#### macOS

```bash
# Instalar via Homebrew (recomendado)
brew install python@3.11
```

Se não tiver o Homebrew, instale-o primeiro em [https://brew.sh/](https://brew.sh/).

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip -y
```

---

## 4. Instalando o Git

O Git é necessário para clonar (baixar) o repositório.

### Verificando se o Git já está instalado

```bash
git --version
```

Se retornar uma versão, pule para a [próxima seção](#5-clonando-o-repositório).

### Instalando o Git (caso necessário)

#### Windows

Baixe e instale em: [https://git-scm.com/download/win](https://git-scm.com/download/win)

Durante a instalação, mantenha as opções padrão.

#### macOS

```bash
brew install git
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install git -y
```

---

## 5. Clonando o Repositório

Navegue até a pasta onde deseja salvar o projeto e execute o comando abaixo no terminal, substituindo `<URL_DO_REPOSITORIO>` pela URL do repositório:

```bash
git clone <URL_DO_REPOSITORIO>
```

Em seguida, entre na pasta do projeto:

```bash
cd CLASSIFICADOR_ZIP
```

> 💡 **Dica:** Para navegar entre pastas no terminal, use `cd nome-da-pasta`. Para listar os arquivos de uma pasta, use `ls` (macOS/Linux) ou `dir` (Windows).

---

## 6. Criando e Ativando o Ambiente Virtual

Um **ambiente virtual** isola as dependências deste projeto das demais instalações do seu sistema, evitando conflitos entre versões de bibliotecas.

### Criando o ambiente virtual

Dentro da pasta do projeto, execute:

```bash
python -m venv venv
```

Isso criará uma pasta chamada `venv/` no diretório do projeto.

### Ativando o ambiente virtual

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

Após a ativação, você verá `(venv)` no início da linha do terminal, indicando que o ambiente está ativo:

```
(venv) C:\Users\seu-usuario\CLASSIFICADOR_ZIP>
```

> ⚠️ **Lembre-se:** O ambiente virtual precisa estar **ativo** sempre que for instalar dependências ou executar os scripts. Se fechar o terminal, ative-o novamente antes de continuar.

---

## 7. Instalando as Dependências

Com o ambiente virtual ativo, instale todas as dependências do projeto:

```bash
pip install -r requirements.txt
```

### Verificando a instalação

Após a conclusão, verifique se as bibliotecas foram instaladas corretamente:

```bash
python -c "import filetype; import pypdf; from pathlib import Path; import logging; print('Todas as dependências instaladas com sucesso!')"
```

Se a mensagem `Todas as dependências instaladas com sucesso!` aparecer, você está pronto para executar o projeto.

---

## 8. Estrutura do Projeto

Após clonar o repositório, você encontrará a seguinte estrutura de arquivos:

```
CLASSIFICADOR_ZIP/
│
├── raw_data/                    # Coloque aqui os ZIPs a serem classificados
│   └── hospede_do_zip/          # Pasta auxiliar de extração dos arquivos do ZIP
│
├── filtered_data/               # Arquivos classificados são organizados aqui
│   ├── jpg/                     # Imagens JPG
│   ├── pdf/                     # PDFs genéricos
│   ├── pdf_danfe/               # DANFEs com página de serviço
│   ├── pdf_danfe_no_ps/         # DANFEs sem página de serviço
│   ├── pdf_no_ps/               # PDFs sem página de serviço (não DANFE)
│   ├── xml/                     # XMLs genéricos
│   ├── xml_danfe/               # XMLs de NF-e
│   └── quarentena/              # Arquivos não reconhecidos ou com erro
│
├── log_register/                # Logs gerados durante a execução
│
├── src/                         # Scripts principais do pipeline
│   ├── main.py                  # Ponto de entrada — orquestra o pipeline completo
│   ├── classificador.py         # Lógica de classificação dos arquivos
│   └── verif_danfe.py           # Verificação se o PDF é um DANFE e se possui PS
│
├── Tools/                       # Utilitários auxiliares
│   ├── log.py                   # Configuração e gerenciamento de logs
│   └── utils.py                 # Funções auxiliares gerais
│
├── .gitignore
├── requirements.txt             # Lista de dependências do projeto
├── README.md                    # Descrição geral do projeto
└── TUTORIAL.md                  # Este arquivo
```

> 📁 **Antes de executar**, coloque seu(s) arquivo(s) `.zip` dentro da pasta `raw_data/`.

---

## 9. Como Executar

Com o ambiente virtual ativo e o(s) arquivo(s) `.zip` na pasta `raw_data/`, execute o pipeline principal:

```bash
python src/main.py
```

### O que acontece durante a execução

O terminal exibirá logs informando o progresso de cada etapa:

```
[INFO] Iniciando processamento do arquivo: arquivo.zip
[INFO] Extraindo arquivos do ZIP...
[INFO] Identificando tipo: documento_001.pdf → PDF
[INFO] Verificando DANFE: documento_001.pdf → DANFE com PS ✓
[INFO] Movendo para: filtered_data/pdf_danfe/
[INFO] Identificando tipo: imagem_001.jpg → JPG
[INFO] Movendo para: filtered_data/jpg/
[INFO] Classificação concluída. X arquivo(s) processado(s).
```

Os logs completos da execução são salvos automaticamente na pasta `log_register/`.

---

## 10. Saídas Esperadas

Ao final da execução, os arquivos do ZIP serão distribuídos entre as subpastas de `filtered_data/` conforme seu tipo e conteúdo:

| Pasta | Conteúdo |
|---|---|
| `filtered_data/jpg/` | Imagens JPG extraídas do ZIP |
| `filtered_data/pdf/` | PDFs genéricos |
| `filtered_data/pdf_danfe/` | PDFs identificados como DANFE com página de serviço |
| `filtered_data/pdf_danfe_no_ps/` | PDFs identificados como DANFE sem página de serviço |
| `filtered_data/pdf_no_ps/` | PDFs sem página de serviço (não DANFE) |
| `filtered_data/xml/` | Arquivos XML genéricos |
| `filtered_data/xml_danfe/` | Arquivos XML de NF-e |
| `filtered_data/quarentena/` | Arquivos não reconhecidos ou que geraram erro durante a classificação |
| `log_register/` | Arquivo de log com o registro completo da execução |

> 📋 Arquivos enviados para `quarentena/` merecem atenção: podem indicar tipos não suportados ou arquivos corrompidos. Consulte o log em `log_register/` para detalhes sobre cada caso.

---

## 11. Solução de Problemas Comuns

### ❌ `python` não é reconhecido no terminal

**Causa:** Python não foi adicionado ao PATH durante a instalação.

**Solução (Windows):** Tente usar `python3` no lugar de `python`. Se não funcionar, reinstale o Python marcando a opção **"Add Python to PATH"**.

---

### ❌ `ModuleNotFoundError` ao executar os scripts

**Causa:** O ambiente virtual não está ativo ou as dependências não foram instaladas corretamente.

**Solução:** Certifique-se de que o `(venv)` aparece no início do terminal. Se não aparecer, ative o ambiente virtual novamente (veja a [Seção 6](#6-criando-e-ativando-o-ambiente-virtual)) e reinstale as dependências:

```bash
pip install -r requirements.txt
```

---

### ❌ Arquivo ZIP não é processado

**Causa:** O arquivo `.zip` não está na pasta `raw_data/` ou está corrompido.

**Solução:** Verifique se o arquivo foi colocado corretamente em `raw_data/` e se consegue abri-lo manualmente. Arquivos corrompidos não podem ser processados.

---

### ❌ Muitos arquivos vão para `quarentena/`

**Causa:** Os arquivos dentro do ZIP possuem tipos não suportados pelo classificador, ou seus cabeçalhos estão corrompidos/incomuns.

**Solução:** Consulte o arquivo de log em `log_register/` para identificar quais arquivos foram para quarentena e o motivo. Arquivos com extensões incomuns ou sem extensão são os candidatos mais prováveis.

---

### ❌ `pip install -r requirements.txt` retorna erro de permissão

**Causa:** Tentativa de instalar pacotes sem o ambiente virtual ativo, no Python do sistema.

**Solução:** Ative o ambiente virtual antes de rodar o `pip install` (veja a [Seção 6](#6-criando-e-ativando-o-ambiente-virtual)).

---

*Tutorial elaborado para uso com o repositório CLASSIFICADOR_ZIP.*