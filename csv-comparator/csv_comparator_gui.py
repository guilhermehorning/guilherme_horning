#!/usr/bin/env python3
"""
Interface Gráfica para o Sistema de Comparação de Arquivos CSV
Compara o conteúdo de dois arquivos CSV das tabelas DWT_DOCTO_FISCAL e DWT_DOCTO_FISCAL_SPED
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import threading
from datetime import datetime
import hashlib
import os
from pathlib import Path
from typing import Dict, List, Any

class CSVComparatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Arquivos CSV - DWT")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Variáveis
        self.file1_path = tk.StringVar()
        self.file2_path = tk.StringVar()
        self.is_comparing = False
        
        # Configurar o estilo
        self.setup_styles()
        
        # Criar interface
        self.create_widgets()
        
        # Centralizar janela
        self.center_window()
    
    def setup_styles(self):
        """Configura os estilos da interface"""
        style = ttk.Style()
        
        # Estilo para labels de sucesso
        style.configure('Success.TLabel', foreground='green')
        style.configure('Warning.TLabel', foreground='orange')
        style.configure('Error.TLabel', foreground='red')
        
        # Estilo para botões
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Cria todos os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky='nsew')
        
        # Configurar grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="🔍 Comparador de Arquivos CSV - DWT", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Seção de seleção de arquivos
        files_frame = ttk.LabelFrame(main_frame, text="Seleção de Arquivos", padding="10")
        files_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 10))
        files_frame.grid_columnconfigure(1, weight=1)
        
        # Arquivo 1
        ttk.Label(files_frame, text="📂 DWT_DOCTO_FISCAL:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        ttk.Entry(files_frame, textvariable=self.file1_path, state='readonly').grid(row=0, column=1, sticky='ew', padx=(0, 10))
        ttk.Button(files_frame, text="Selecionar", command=lambda: self.select_file(1)).grid(row=0, column=2)
        
        # Arquivo 2
        ttk.Label(files_frame, text="📂 DWT_DOCTO_FISCAL_SPED:").grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
        ttk.Entry(files_frame, textvariable=self.file2_path, state='readonly').grid(row=1, column=1, sticky='ew', padx=(0, 10), pady=(10, 0))
        ttk.Button(files_frame, text="Selecionar", command=lambda: self.select_file(2)).grid(row=1, column=2, pady=(10, 0))
        
        # Botão de comparação
        self.compare_btn = ttk.Button(main_frame, text="🔍 Comparar Arquivos", 
                                     command=self.start_comparison, style='Action.TButton')
        self.compare_btn.grid(row=2, column=0, columnspan=3, pady=20)
        
        # Barra de progresso e status
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(0, 10))
        progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="Pronto para comparar")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky='w')
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, sticky='ew', pady=(5, 0))
        
        # Status
        self.status_var = tk.StringVar(value="Selecione os arquivos para começar")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=2, column=0, sticky='w', pady=(5, 0))
        
        # Área de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados da Comparação", padding="10")
        results_frame.grid(row=4, column=0, columnspan=3, sticky='nsew', pady=(10, 0))
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Texto dos resultados com scroll
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, font=('Courier New', 10))
        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
    
    def select_file(self, file_num):
        """Seleciona um arquivo CSV ou Excel"""
        filetypes = [
            ('Todos os suportados', '*.csv;*.xlsx;*.xls'),
            ('CSV files', '*.csv'),
            ('Excel files', '*.xlsx;*.xls'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title=f"Selecionar arquivo {'DWT_DOCTO_FISCAL' if file_num == 1 else 'DWT_DOCTO_FISCAL_SPED'}",
            filetypes=filetypes
        )
        
        if filename:
            if file_num == 1:
                self.file1_path.set(filename)
            else:
                self.file2_path.set(filename)
            
            self.update_status()
    
    def update_status(self):
        """Atualiza o status baseado nos arquivos selecionados"""
        file1 = self.file1_path.get()
        file2 = self.file2_path.get()
        
        if file1 and file2:
            self.status_var.set("✅ Arquivos selecionados - Pronto para comparar!")
            self.compare_btn.configure(state='normal')
        elif file1 or file2:
            self.status_var.set("⚠️ Selecione o segundo arquivo")
            self.compare_btn.configure(state='disabled')
        else:
            self.status_var.set("📂 Selecione os arquivos para começar")
            self.compare_btn.configure(state='disabled')
    
    def start_comparison(self):
        """Inicia a comparação em thread separada"""
        if self.is_comparing:
            return
        
        file1 = self.file1_path.get()
        file2 = self.file2_path.get()
        
        if not file1 or not file2:
            messagebox.showerror("Erro", "Por favor, selecione ambos os arquivos.")
            return
        
        # Verificar se arquivos existem
        if not os.path.exists(file1):
            messagebox.showerror("Erro", f"Arquivo não encontrado:\n{file1}")
            return
        
        if not os.path.exists(file2):
            messagebox.showerror("Erro", f"Arquivo não encontrado:\n{file2}")
            return
        
        self.is_comparing = True
        self.compare_btn.configure(state='disabled', text="⏳ Comparando...")
        self.progress_bar.start()
        self.progress_var.set("🔍 Iniciando comparação...")
        
        # Executar comparação em thread separada
        thread = threading.Thread(target=self.compare_files, args=(file1, file2))
        thread.daemon = True
        thread.start()
    
    def compare_files(self, file1_path, file2_path):
        """Executa a comparação dos arquivos"""
        try:
            # Carregar arquivos
            self.root.after(0, lambda: self.progress_var.set("📂 Carregando arquivos..."))
            
            df1 = self._read_file_auto(file1_path)
            df2 = self._read_file_auto(file2_path)
            
            file1_name = Path(file1_path).name
            file2_name = Path(file2_path).name
            
            # Comparar estruturas
            self.root.after(0, lambda: self.progress_var.set("🔍 Comparando estruturas..."))
            structure_result = self.compare_structure(df1, df2)
            
            if not structure_result["columns_match"]:
                result = {
                    "success": True,
                    "structure_match": False,
                    "structure_result": structure_result,
                    "file1_name": file1_name,
                    "file2_name": file2_name,
                    "file1_count": len(df1),
                    "file2_count": len(df2)
                }
                self.root.after(0, lambda: self.show_results(result))
                return
            
            # Comparar dados
            self.root.after(0, lambda: self.progress_var.set("📊 Comparando dados..."))
            data_result = self.compare_data(df1, df2, structure_result["common_columns"])
            
            result = {
                "success": True,
                "structure_match": True,
                "structure_result": structure_result,
                "data_result": data_result,
                "file1_name": file1_name,
                "file2_name": file2_name,
                "file1_count": len(df1),
                "file2_count": len(df2)
            }
            
            self.root.after(0, lambda: self.show_results(result))
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e)
            }
            self.root.after(0, lambda: self.show_results(error_result))
    
    def compare_structure(self, df1, df2):
        """Compara a estrutura dos DataFrames"""
        cols1 = set(df1.columns)
        cols2 = set(df2.columns)
        
        return {
            "columns_match": cols1 == cols2,
            "file1_columns": list(cols1),
            "file2_columns": list(cols2),
            "missing_in_file1": list(cols2 - cols1),
            "missing_in_file2": list(cols1 - cols2),
            "common_columns": list(cols1 & cols2)
        }
    
    def compare_data(self, df1, df2, common_columns):
        """Compara dados dos DataFrames com análise campo por campo"""
        
        # Análise detalhada campo por campo (linha por linha)
        field_differences = []
        common_fields = []
        common_records_count = 0
        
        # Determina número mínimo de linhas para comparação posicional
        min_rows = min(len(df1), len(df2))
        
        # Analisa cada campo individualmente
        for col in common_columns:
            field_has_differences = False
            examples = []
            
            # Compara valores do campo linha por linha
            for row_idx in range(min_rows):
                val1 = df1.iloc[row_idx][col]
                val2 = df2.iloc[row_idx][col]
                
                norm_val1 = self._normalize_value(val1)
                norm_val2 = self._normalize_value(val2)
                
                if norm_val1 != norm_val2:
                    field_has_differences = True
                    if len(examples) < 3:  # Máximo 3 exemplos
                        examples.append({
                            'file1_value': val1,
                            'file2_value': val2,
                            'row_number': row_idx + 1
                        })
            
            if field_has_differences:
                # Conta quantas diferenças existem neste campo
                diff_count = sum(1 for i in range(min_rows) 
                               if self._normalize_value(df1.iloc[i][col]) != 
                                  self._normalize_value(df2.iloc[i][col]))
                
                field_differences.append({
                    'field_name': col,
                    'differences_count': diff_count,
                    'examples': examples
                })
            else:
                common_fields.append(col)
        
        # Conta registros completamente idênticos (todas as colunas iguais)
        for row_idx in range(min_rows):
            row_identical = True
            for col in common_columns:
                val1 = df1.iloc[row_idx][col]
                val2 = df2.iloc[row_idx][col]
                if self._normalize_value(val1) != self._normalize_value(val2):
                    row_identical = False
                    break
            if row_identical:
                common_records_count += 1
        
        # Registros únicos baseados em diferença de tamanho
        unique_records_file1 = max(0, len(df1) - min_rows) 
        unique_records_file2 = max(0, len(df2) - min_rows)
        
        # Dados dos registros únicos (se existirem)
        unique_file1_data = []
        unique_file2_data = []
        
        if unique_records_file1 > 0:
            unique_file1_data = [df1.iloc[i].to_dict() for i in range(min_rows, len(df1))][:5]
        
        if unique_records_file2 > 0:
            unique_file2_data = [df2.iloc[i].to_dict() for i in range(min_rows, len(df2))][:5]
        
        return {
            "common_records": common_records_count,
            "common_fields": common_fields,
            "common_fields_count": len(common_fields),
            "unique_in_file1": unique_records_file1,
            "unique_in_file2": unique_records_file2,
            "unique_file1_data": unique_file1_data,
            "unique_file2_data": unique_file2_data,
            "field_differences": field_differences,
            "are_identical": len(field_differences) == 0 and unique_records_file1 == 0 and unique_records_file2 == 0
        }
    
    def _normalize_value(self, value) -> str:
        """Normaliza valor para comparação"""
        if pd.isna(value):
            return "NULL"
        elif isinstance(value, str):
            return value.strip().replace(',', '.')
        else:
            return str(value).strip()
    
    def _read_file_auto(self, file_path: str) -> pd.DataFrame:
        """
        Lê arquivo CSV ou Excel com detecção automática de formato
        
        Args:
            file_path (str): Caminho do arquivo
            
        Returns:
            pd.DataFrame: DataFrame carregado
        """
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext in ['.xlsx', '.xls']:
            return self._read_excel_auto(file_path)
        else:
            return self._read_csv_auto(file_path)
    
    def _read_excel_auto(self, file_path: str) -> pd.DataFrame:
        """Lê arquivo Excel com diferentes configurações"""
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            df.columns = df.columns.str.strip().str.strip('"').str.strip("'")
            return df
        except Exception as e:
            try:
                df = pd.read_excel(file_path, sheet_name=0, engine='openpyxl')
                df.columns = df.columns.str.strip().str.strip('"').str.strip("'")
                return df
            except Exception:
                raise Exception(f"Erro ao ler arquivo Excel: {str(e)}")
    
    def _read_csv_auto(self, file_path: str) -> pd.DataFrame:
        """Lê arquivo CSV com detecção automática de formato"""
        configs = [
            {'sep': ';', 'encoding': 'utf-8', 'quotechar': '"'},
            {'sep': ',', 'encoding': 'utf-8', 'quotechar': '"'},
            {'sep': ';', 'encoding': 'utf-8', 'quoting': 3},  # QUOTE_NONE
            {'sep': ',', 'encoding': 'utf-8', 'quoting': 3},  # QUOTE_NONE
            {'sep': ';', 'encoding': 'latin1', 'quotechar': '"'},
            {'sep': ',', 'encoding': 'latin1', 'quotechar': '"'},
        ]
        
        for config in configs:
            try:
                df = pd.read_csv(file_path, **config)
                df.columns = df.columns.str.strip().str.strip('"').str.strip("'")
                
                if len(df.columns) > 1 and len(df) > 0:
                    return df
                    
            except Exception:
                continue
        
        raise Exception(f"Não foi possível ler o arquivo CSV: {file_path}")
    
    def generate_row_hash(self, row, columns):
        """Gera hash MD5 para uma linha usando colunas específicas"""
        values = []
        for col in sorted(columns):  # Ordena para garantir consistência
            val = row.get(col)
            if pd.isna(val):
                values.append("NULL")
            else:
                values.append(str(val).strip())
        
        row_string = "|".join(values)
        return hashlib.md5(row_string.encode('utf-8')).hexdigest()
    
    def show_results(self, result):
        """Mostra resultados na interface"""
        self.progress_bar.stop()
        self.is_comparing = False
        self.compare_btn.configure(state='normal', text="🔍 Comparar Arquivos")
        
        if not result["success"]:
            self.progress_var.set("❌ Erro na comparação")
            self.status_var.set("❌ Erro durante a comparação")
            self.status_label.configure(style='Error.TLabel')
            
            error_text = f"""
❌ ERRO NA COMPARAÇÃO

Detalhes do erro:
{result['error']}

💡 POSSÍVEIS SOLUÇÕES:
• Verifique se os arquivos são CSV válidos
• Certifique-se que os arquivos não estão abertos em outro programa
• Verifique se os arquivos têm headers na primeira linha
• Tente arquivos menores para teste
            """
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, error_text.strip())
            return
        
        # Gera relatório
        report = self.generate_report(result)
        
        # Atualiza interface baseado no resultado
        if not result["structure_match"]:
            self.progress_var.set("⚠️ Estruturas diferentes")
            self.status_var.set("⚠️ Arquivos têm estruturas diferentes")
            self.status_label.configure(style='Warning.TLabel')
        elif result["data_result"]["are_identical"]:
            self.progress_var.set("🎉 Arquivos idênticos!")
            self.status_var.set("🎉 Os arquivos são completamente idênticos!")
            self.status_label.configure(style='Success.TLabel')
        else:
            # Calcula o total correto de diferenças
            if result["data_result"].get('field_differences'):
                field_differences_count = len(result["data_result"]['field_differences'])
                self.progress_var.set(f"⚠️ {field_differences_count} campos diferentes")
                self.status_var.set(f"⚠️ Encontradas diferenças em {field_differences_count} campos")
            else:
                differences = result["data_result"]["unique_in_file1"] + result["data_result"]["unique_in_file2"]
                self.progress_var.set(f"⚠️ {differences} registros diferentes")
                self.status_var.set(f"⚠️ Encontrados {differences} registros diferentes")
            self.status_label.configure(style='Warning.TLabel')
        
        # Mostra relatório
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, report)
        
        # Mostra popup com resumo
        self.show_summary_popup(result)
    
    def generate_report(self, result):
        """Gera relatório detalhado"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
═══════════════════════════════════════════════════════════════════════════════
🔍 RELATÓRIO DE COMPARAÇÃO DE ARQUIVOS CSV
═══════════════════════════════════════════════════════════════════════════════

📅 Data/Hora: {timestamp}
📂 Arquivo 1: {result['file1_name']}
📂 Arquivo 2: {result['file2_name']}

───────────────────────────────────────────────────────────────────────────────
📊 INFORMAÇÕES BÁSICAS
───────────────────────────────────────────────────────────────────────────────
Registros no arquivo 1: {result['file1_count']:,}
Registros no arquivo 2: {result['file2_count']:,}
Estruturas coincidem: {'✅ Sim' if result['structure_match'] else '❌ Não'}
        """
        
        if not result["structure_match"]:
            struct = result["structure_result"]
            report += f"""
───────────────────────────────────────────────────────────────────────────────
🏗️ DIFERENÇAS NA ESTRUTURA
───────────────────────────────────────────────────────────────────────────────
            """
            
            if struct["missing_in_file1"]:
                report += f"\n❌ Colunas em {result['file2_name']} mas não em {result['file1_name']}:\n"
                for col in struct["missing_in_file1"]:
                    report += f"   • {col}\n"
            
            if struct["missing_in_file2"]:
                report += f"\n❌ Colunas em {result['file1_name']} mas não em {result['file2_name']}:\n"
                for col in struct["missing_in_file2"]:
                    report += f"   • {col}\n"
            
            report += "\n⚠️ Não é possível comparar dados devido às diferenças de estrutura."
        
        else:
            data = result["data_result"]
            report += f"""
───────────────────────────────────────────────────────────────────────────────
📋 COMPARAÇÃO DOS DADOS
───────────────────────────────────────────────────────────────────────────────
Registros completamente idênticos: {data['common_records']:,}
Únicos no arquivo 1: {data['unique_in_file1']:,}
Únicos no arquivo 2: {data['unique_in_file2']:,}
            """
            
            # Mostra informações sobre campos
            if data.get('common_fields_count', 0) > 0:
                report += f"Campos com valores idênticos: {data['common_fields_count']:,}\n"
            if data.get('field_differences'):
                report += f"Campos com diferenças: {len(data['field_differences']):,}\n"
            
            if data["are_identical"]:
                report += """
🎉 RESULTADO: OS ARQUIVOS SÃO IDÊNTICOS!
✅ Todos os registros coincidem perfeitamente.
✅ As estruturas são iguais.
✅ Os dados são completamente iguais.
                """
            else:
                # Calcula o total correto de diferenças
                if data.get('field_differences'):
                    total_field_differences = len(data['field_differences'])
                    report += f"""
⚠️ RESULTADO: OS ARQUIVOS TÊM DIFERENÇAS!
❌ Total de campos com diferenças: {total_field_differences:,}
📊 Registros únicos: {data['unique_in_file1']} + {data['unique_in_file2']} = {data['unique_in_file1'] + data['unique_in_file2']}
                    """
                else:
                    total_diff = data['unique_in_file1'] + data['unique_in_file2']
                    report += f"""
⚠️ RESULTADO: OS ARQUIVOS TÊM DIFERENÇAS!
❌ Total de registros com diferenças: {total_diff:,}
                    """
                
                # Mostra campos comuns (sem diferenças)
                if data.get('common_fields'):
                    report += f"\n{'─'*60}\n"
                    report += f"✅ CAMPOS SEM DIFERENÇAS ({len(data['common_fields'])} campos)\n"
                    report += f"{'─'*60}\n"
                    for i, field in enumerate(data['common_fields'][:10]):
                        report += f"   {i+1:2d}. {field}\n"
                    if len(data['common_fields']) > 10:
                        report += f"   ... e mais {len(data['common_fields']) - 10} campos\n"
                
                # Análise detalhada das diferenças por campo
                if data.get('field_differences'):
                    report += f"\n{'═'*80}\n"
                    report += f"🔍 ANÁLISE DETALHADA DAS DIFERENÇAS POR CAMPO ({len(data['field_differences'])} campos)\n"
                    report += f"{'═'*80}\n"
                    
                    for field_diff in data['field_differences'][:15]:  # Limita a 15 campos diferentes
                        report += f"\n📝 CAMPO: {field_diff['field_name']}\n"
                        report += f"   Diferenças encontradas: {field_diff['differences_count']} linha(s)\n"
                        report += f"{'-'*60}\n"
                        
                        for i, example in enumerate(field_diff['examples']):
                            file1_val = example['file1_value'] if example['file1_value'] is not None else 'NULL'
                            file2_val = example['file2_value'] if example['file2_value'] is not None else 'NULL'
                            
                            report += f"   Linha {example['row_number']}:\n"
                            report += f"      📂 {result['file1_name']}: '{file1_val}'\n"
                            report += f"      📂 {result['file2_name']}: '{file2_val}'\n"
                            if i < len(field_diff['examples']) - 1:
                                report += "\n"
                        report += "\n"
                    
                    if len(data['field_differences']) > 15:
                        report += f"... e mais {len(data['field_differences']) - 15} campos com diferenças\n"
                
                # Resumo dos registros únicos
                report += f"\n{'─'*60}\n"
                report += "📋 RESUMO DOS REGISTROS ÚNICOS\n"
                report += f"{'─'*60}\n"
                report += f"Registros únicos em {result['file1_name']}: {data['unique_in_file1']:,}\n"
                report += f"Registros únicos em {result['file2_name']}: {data['unique_in_file2']:,}\n"
        
        report += "\n═══════════════════════════════════════════════════════════════════════════════"
        
        return report.strip()
    
    def show_summary_popup(self, result):
        """Mostra popup com resumo dos resultados"""
        if not result["structure_match"]:
            messagebox.showwarning(
                "Estruturas Diferentes",
                f"❌ Os arquivos têm estruturas diferentes!\n\n"
                f"📂 {result['file1_name']}: {len(result['structure_result']['file1_columns'])} colunas\n"
                f"📂 {result['file2_name']}: {len(result['structure_result']['file2_columns'])} colunas\n\n"
                f"⚠️ Não é possível comparar os dados."
            )
        elif result["data_result"]["are_identical"]:
            messagebox.showinfo(
                "Arquivos Idênticos!",
                f"🎉 Os arquivos são completamente idênticos!\n\n"
                f"✅ {result['file1_count']:,} registros em cada arquivo\n"
                f"✅ Todas as estruturas coincidem\n"
                f"✅ Todos os dados são iguais"
            )
        else:
            data = result["data_result"]
            
            # Calcula o total correto de diferenças
            if data.get('field_differences'):
                field_differences_count = len(data['field_differences'])
                common_fields_count = data.get('common_fields_count', 0)
                
                message_parts = [
                    f"⚠️ Foram encontradas diferenças em {field_differences_count:,} campos!",
                    "",
                    f"📊 Registros completamente idênticos: {data['common_records']:,}",
                    f"📋 Únicos em {result['file1_name']}: {data['unique_in_file1']:,}",
                    f"📋 Únicos em {result['file2_name']}: {data['unique_in_file2']:,}",
                    ""
                ]
                
                if common_fields_count > 0:
                    message_parts.extend([
                        f"✅ Campos sem diferenças: {common_fields_count:,}",
                        f"🔍 Campos com diferenças: {field_differences_count:,}",
                        ""
                    ])
                
                message_parts.append("📄 Veja a análise detalhada dos campos abaixo.")
                
                messagebox.showwarning(
                    "Diferenças Encontradas",
                    "\n".join(message_parts)
                )
            else:
                total_diff = data['unique_in_file1'] + data['unique_in_file2']
                messagebox.showwarning(
                    "Diferenças Encontradas",
                    f"⚠️ Foram encontradas {total_diff:,} diferenças!\n\n"
                    f"📊 Registros completamente idênticos: {data['common_records']:,}\n"
                    f"📋 Únicos em {result['file1_name']}: {data['unique_in_file1']:,}\n"
                    f"📋 Únicos em {result['file2_name']}: {data['unique_in_file2']:,}\n\n"
                    f"📄 Veja o relatório detalhado abaixo."
                )


def main():
    """Função principal da interface gráfica"""
    root = tk.Tk()
    app = CSVComparatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()