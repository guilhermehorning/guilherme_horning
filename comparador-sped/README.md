# Comparador de Arquivos SPED Fiscal

Este programa permite comparar dois arquivos SPED Fiscal (EFD - Escrituração Fiscal Digital) e gera um relatório detalhado das diferenças encontradas.

## 📋 Características

- **Análise Completa**: Compara todos os registros e campos dos arquivos SPED
- **Detecção de Diferenças**: Identifica registros adicionados, removidos e modificados
- **Relatórios Detalhados**: Gera relatórios no console e opcionalmente em HTML
- **Estatísticas**: Mostra resumo quantitativo das diferenças por tipo de registro
- **Fácil de Usar**: Interface simples via linha de comando

## 🛠️ Requisitos

- Python 3.7 ou superior
- Os arquivos devem estar no formato padrão SPED Fiscal (campos separados por pipe `|`)

## 📖 Como Usar

### Uso Básico

```bash
python comparador_sped.py arquivo1.txt arquivo2.txt
```

### Com Relatório HTML

```bash
python comparador_sped.py arquivo1.txt arquivo2.txt --html relatorio.html
```

### Com Informações Detalhadas

```bash
python comparador_sped.py arquivo1.txt arquivo2.txt --verbose
```

## 📝 Exemplos

### Comparação Simples
```bash
python comparador_sped.py 5190720_GHSP_01_2025_EFD.TXT 5190793_GHSP_01_2025_EFD_PÓS_PACOTE.TXT
```

### Comparação com Relatório HTML
```bash
python comparador_sped.py sped_original.txt sped_modificado.txt --html relatorio_diferencias.html
```

## 📊 Tipos de Diferenças Detectadas

1. **Registros Adicionados (➕)**: Registros que existem apenas no segundo arquivo
2. **Registros Removidos (➖)**: Registros que existem apenas no primeiro arquivo
3. **Registros Modificados (🔄)**: Registros que existem em ambos mas com campos diferentes

## 📈 Relatórios Gerados

### Relatório no Console
- Resumo geral com contadores
- Estatísticas por tipo de registro
- Detalhes linha por linha das diferenças
- Campos específicos alterados

### Relatório HTML (Opcional)
- Interface visual mais amigável
- Código colorido para diferentes tipos de diferenças
- Navegação facilitada
- Tabelas organizadas

## 🏗️ Estrutura do Projeto

```
comparador_sped/
├── comparador_sped.py      # Script principal
├── sped_parser.py          # Parser de arquivos SPED
├── sped_comparator.py      # Lógica de comparação
├── sped_report.py          # Gerador de relatórios
└── README.md              # Este arquivo
```

## ⚙️ Módulos

### `sped_parser.py`
- Classe `SpedParser`: Faz o parsing de arquivos SPED
- Classe `SpedRecord`: Representa um registro individual

### `sped_comparator.py`
- Classe `SpedComparator`: Executa a comparação entre arquivos
- Classes de diferenças: `RecordDifference`, `FieldDifference`

### `sped_report.py`
- Classe `SpedReportGenerator`: Gera relatórios em console e HTML

### `comparador_sped.py`
- Script principal com interface de linha de comando

## 🔍 Exemplo de Saída

```
🔍 COMPARADOR DE ARQUIVOS SPED FISCAL
==================================================

================================================================================
RELATÓRIO DE COMPARAÇÃO SPED FISCAL
================================================================================

Arquivo 1: 5190720_GHSP_01_2025_EFD.TXT
Arquivo 2: 5190793_GHSP_01_2025_EFD_PÓS_PACOTE.TXT
Data da comparação: 09/10/2025 14:30:15

--- RESUMO GERAL ---
Total de diferenças encontradas: 0
Registros adicionados: 0
Registros removidos: 0
Registros modificados: 0

✅ Os arquivos são idênticos!
```

## 🚨 Códigos de Saída

- `0`: Arquivos são idênticos
- `1`: Diferenças encontradas
- `130`: Operação cancelada pelo usuário

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique se os arquivos estão no formato SPED correto
2. Certifique-se de ter Python 3.7+ instalado
3. Verifique se os caminhos dos arquivos estão corretos

## 📄 Formatos Suportados

- Arquivos `.txt` (mais comum)
- Arquivos `.sped`
- Arquivos `.efd`
- Qualquer arquivo texto com formato SPED (campos separados por `|`)

## 🎯 Casos de Uso

- **Auditoria**: Verificar alterações em arquivos SPED
- **Controle de Qualidade**: Validar processamento de dados fiscais
- **Debugging**: Identificar onde ocorreram mudanças
- **Compliance**: Documentar alterações para órgãos fiscalizadores