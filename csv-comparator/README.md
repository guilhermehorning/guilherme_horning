# Comparador de Arquivos CSV - DWT

Sistema para comparação de arquivos CSV das tabelas `DWT_DOCTO_FISCAL` e `DWT_DOCTO_FISCAL_SPED`.

## 📋 Descrição

Este sistema compara o conteúdo de dois arquivos CSV ou Excel e identifica:
- Diferenças na estrutura (colunas)
- Registros únicos em cada arquivo
- Registros em comum
- Diferenças detalhadas campo por campo
- Relatório detalhado das diferenças

## 📊 Formatos Suportados

- **📄 CSV** (.csv) - Separadores automáticos (vírgula, ponto e vírgula)
- **📈 Excel** (.xlsx, .xls) - Primeira planilha por padrão
- **🔄 Misturado** - Pode comparar CSV com Excel
- **🌐 Encoding** - UTF-8 e Latin1 (detecção automática)

## �️ Versões Disponíveis

### 🎨 **Interface Gráfica** (RECOMENDADO)
- Interface amigável com botões e janelas
- Seleção de arquivos por clique
- Barra de progresso
- Relatórios formatados
- Popups informativos

### 💻 **Linha de Comando**
- Execução via terminal/prompt
- Ideal para automação
- Mais rápida para usuários avançados

## �🚀 Como Usar

### 🎨 **INTERFACE GRÁFICA** (Mais Fácil)

#### Opção 1: Executável Windows
```bash
executar_interface_grafica.bat
```

#### Opção 2: Execução Direta
```bash
python csv_comparator_gui.py
```

### 💻 **LINHA DE COMANDO** (Para Usuários Avançados)

#### Opção 1: Com Parâmetros
```bash
python csv_comparator.py "caminho/arquivo1.csv" "caminho/arquivo2.csv"
```

#### Opção 2: Execução Interativa
```bash
python csv_comparator.py
```
O sistema solicitará os caminhos dos arquivos.

#### Opção 3: Arquivo Batch (Windows)
```bash
executar_comparacao.bat
```

## 📁 Estrutura do Projeto

```
comparar_dwt/
├── csv_comparator_gui.py          # 🎨 Interface Gráfica (PRINCIPAL)
├── csv_comparator.py              # 💻 Linha de Comando
├── executar_interface_grafica.bat # 🚀 Executar Interface Gráfica
├── executar_comparacao.bat        # 💻 Executar Linha de Comando  
├── README.md                      # 📖 Este arquivo
├── .gitignore                     # 🚫 Arquivos ignorados pelo git
└── arquivos/                      # 📂 Seus arquivos CSV (opcional)
    ├── dwt_docto_fiscal.csv
    └── dwt_docto_fiscal_sped.csv
```

## 📊 Exemplo de Uso

### 🎨 Interface Gráfica
1. Execute: `executar_interface_grafica.bat`
2. Clique em "Procurar" para selecionar os arquivos (CSV ou Excel)
3. Clique em "Comparar Arquivos"
4. Veja os resultados na tela

### 💻 Linha de Comando

#### CSV vs CSV:
```bash
python csv_comparator.py "arquivo1.csv" "arquivo2.csv"
```

#### Excel vs Excel:
```bash
python csv_comparator.py "arquivo1.xlsx" "arquivo2.xlsx"
```

#### CSV vs Excel (Misturado):
```bash
python csv_comparator.py "arquivo1.csv" "arquivo2.xlsx"
```

## 📈 Códigos de Retorno

- `0`: Arquivos são idênticos
- `1`: Erro geral (arquivo não encontrado, erro de leitura, etc.)
- `2`: Estruturas diferentes (colunas não coincidem)
- `3`: Diferenças nos dados encontradas

## 🔍 O que o Sistema Compara

### Estrutura
- ✅ Verifica se ambos os arquivos têm as mesmas colunas
- 🔍 Identifica colunas presentes em um arquivo mas não no outro
- 📊 Conta o número de colunas de cada arquivo

### Dados
- 🔐 Compara linha por linha usando hash MD5
- 📋 Identifica registros únicos em cada arquivo
- 📈 Conta registros em comum
- 🚫 Trata valores nulos consistentemente
- ⚡ Otimizado para arquivos grandes

## 🎨 Interface Gráfica - Recursos

- 🖱️ **Seleção Fácil**: Clique para escolher arquivos
- 📊 **Barra de Progresso**: Veja o progresso da comparação
- 🎯 **Status Visual**: Cores indicam sucesso, aviso ou erro
- 📋 **Relatório Detalhado**: Resultados organizados e legíveis
- 🔔 **Popups Informativos**: Resumos rápidos dos resultados
- 🧹 **Botão Limpar**: Reinicia a interface facilmente

## 📝 Exemplo de Relatório

```
================================================================================
RELATÓRIO DE COMPARAÇÃO DE ARQUIVOS CSV
================================================================================
📂 Arquivo 1: dwt_docto_fiscal.csv
📂 Arquivo 2: dwt_docto_fiscal_sped.csv
📅 Data/Hora: 2025-10-01 14:30:45

📊 COMPARAÇÃO DOS DADOS
----------------------------------------
Registros em dwt_docto_fiscal.csv: 1,523
Registros em dwt_docto_fiscal_sped.csv: 1,520
Registros em comum: 1,520
Únicos em dwt_docto_fiscal.csv: 3
Únicos em dwt_docto_fiscal_sped.csv: 0

⚠️  RESULTADO: Os arquivos têm DIFERENÇAS!
❌ Total de diferenças encontradas: 3
```

## 🛠️ Requisitos

- Python 3.7+
- pandas
- openpyxl (para suporte Excel)

### Instalação das dependências
```bash
pip install pandas openpyxl
```

ou use o arquivo requirements.txt:
```bash
pip install -r requirements.txt
```

## 💡 Dicas de Uso

1. **Arquivos Grandes**: O sistema é otimizado para arquivos grandes usando hashing
2. **Encoding**: Usa UTF-8 por padrão
3. **Caminhos**: Pode usar caminhos absolutos ou relativos
4. **Aspas**: Coloque o caminho entre aspas se contiver espaços

## ❓ Solução de Problemas

### Erro "pandas not found"
```bash
pip install pandas
```

### Erro "arquivo não encontrado"
- Verifique o caminho do arquivo
- Use caminhos absolutos se necessário
- Coloque o caminho entre aspas

### Diferenças esperadas vs encontradas
- O sistema é case-sensitive
- Espaços em branco são considerados
- Valores nulos são tratados como "NULL"