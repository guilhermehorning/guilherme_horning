# Leitor de Estorno de Débito - CAT154-12

Sistema Python para importação e leitura de arquivos TXT de Estorno de Débito baseado no layout CAT154-12 (São Paulo).

## 📋 Funcionalidades

- ✅ Importação de arquivos TXT baseado em layout CSV
- ✅ Interface gráfica intuitiva (Tkinter)
- ✅ Visualização de registros de controle e estorno de débito
- ✅ Navegação entre registros
- ✅ Exportação para Excel com duas abas separadas
- ✅ Carregamento automático do layout

## 🚀 Como usar

### Pré-requisitos

```bash
pip install pandas openpyxl
```

### Executar

```bash
python leitor_estorno_debito.py
```

### Fluxo de uso

1. O programa abre com o layout CSV já carregado automaticamente
2. Clique em "Selecionar" para importar o arquivo TXT
3. Navegue entre os registros usando os botões ⬅️ ➡️
4. Exporte para Excel quando necessário

## 📁 Estrutura

- **Registro Tipo 1 (Controle)**: Dados do estabelecimento e responsável
- **Registro Tipo 2 (Estorno de Débito)**: Informações de estorno de NFCEE

## 🔧 Tecnologias

- Python 3.x
- Tkinter (interface gráfica)
- Pandas (manipulação de dados)
- openpyxl (exportação Excel)

## 📝 Observações

O layout é baseado na Portaria CAT 154/12 do Estado de São Paulo para declaração de estorno de débitos de ICMS.

---

**Desenvolvido por:** Guilherme Horning
