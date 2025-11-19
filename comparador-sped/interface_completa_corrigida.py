#!/usr/bin/env python3
"""
Interface Gráfica Completa e Simplificada para Comparador SPED Fiscal
Versão corrigida com botão bem visível
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
import webbrowser
from datetime import datetime
import os

from sped_parser import SpedParser
from sped_comparator import SpedComparator, DifferenceType
from sped_report import SpedReportGenerator


class SpedComparatorGUIFixed:
    """Interface gráfica corrigida para o comparador SPED."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Comparador SPED Fiscal - Interface Completa")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Variáveis
        self.arquivo1_path = tk.StringVar()
        self.arquivo2_path = tk.StringVar()
        self.gerar_html = tk.BooleanVar(value=True)
        self.html_path = tk.StringVar(value="relatorio_sped_completo.html")
        self.comparator = None
        
        # Criar interface
        self.create_interface()
        
        # Centralizar janela
        self.center_window()
        
    def center_window(self):
        """Centraliza a janela na tela."""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
    def create_interface(self):
        """Cria toda a interface do usuário."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== TÍTULO =====
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="🔍 Comparador SPED Fiscal", 
                               font=('Arial', 18, 'bold'))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Interface Gráfica Completa", 
                                  font=('Arial', 10))
        subtitle_label.pack()
        
        # ===== SELEÇÃO DE ARQUIVOS =====
        files_frame = ttk.LabelFrame(main_frame, text="📁 Seleção de Arquivos SPED", padding="15")
        files_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Primeiro arquivo
        ttk.Label(files_frame, text="Primeiro arquivo:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=(5, 5))
        
        frame1 = ttk.Frame(files_frame)
        frame1.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        files_frame.columnconfigure(0, weight=1)
        
        self.entry1 = ttk.Entry(frame1, textvariable=self.arquivo1_path, font=('Arial', 9), width=60)
        self.entry1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(frame1, text="📂 Procurar...", 
                  command=lambda: self.select_file(self.arquivo1_path)).pack(side=tk.RIGHT)
        
        # Segunda arquivo
        ttk.Label(files_frame, text="Segunda arquivo:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=(5, 5))
        
        frame2 = ttk.Frame(files_frame)
        frame2.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.entry2 = ttk.Entry(frame2, textvariable=self.arquivo2_path, font=('Arial', 9), width=60)
        self.entry2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(frame2, text="📂 Procurar...", 
                  command=lambda: self.select_file(self.arquivo2_path)).pack(side=tk.RIGHT)
        
        # ===== OPÇÕES =====
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Opções", padding="15")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Checkbutton(options_frame, text="📝 Gerar relatório HTML automático", 
                       variable=self.gerar_html).pack(anchor=tk.W, pady=5)
        
        html_frame = ttk.Frame(options_frame)
        html_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(html_frame, text="Local do HTML:").pack(side=tk.LEFT)
        ttk.Entry(html_frame, textvariable=self.html_path, width=40).pack(
            side=tk.LEFT, padx=(10, 10), fill=tk.X, expand=True)
        ttk.Button(html_frame, text="💾 Salvar como...", 
                  command=self.select_html_file).pack(side=tk.RIGHT)
        
        # ===== BOTÃO PRINCIPAL DE AÇÃO =====
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=20)
        
        # BOTÃO PRINCIPAL - GRANDE E DESTACADO
        self.compare_button = tk.Button(
            action_frame,
            text="🔄 COMPARAR ARQUIVOS SPED",
            command=self.start_comparison,
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            height=2,
            width=25,
            relief=tk.RAISED,
            bd=3
        )
        self.compare_button.pack(pady=10)
        
        # Botões secundários
        secondary_frame = ttk.Frame(action_frame)
        secondary_frame.pack()
        
        ttk.Button(secondary_frame, text="🗑️ Limpar Campos", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(secondary_frame, text="❓ Ajuda", 
                  command=self.show_help).pack(side=tk.LEFT, padx=5)
        ttk.Button(secondary_frame, text="❌ Sair", 
                  command=self.root.destroy).pack(side=tk.LEFT, padx=5)
        
        # ===== ÁREA DE RESULTADOS =====
        results_frame = ttk.LabelFrame(main_frame, text="📊 Resultados da Comparação", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Notebook com abas
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba 1: Resumo
        self.create_summary_tab()
        
        # Aba 2: Detalhes
        self.create_details_tab()
        
        # Aba 3: Comparação Visual
        self.create_visual_comparison_tab()
        
        # ===== BARRA DE STATUS =====
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="✅ Pronto para comparação de arquivos SPED", 
                                     font=('Arial', 10))
        self.status_label.pack(side=tk.LEFT)
        
        self.progress_bar = ttk.Progressbar(status_frame, mode='indeterminate', length=200)
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 0))
        
    def create_summary_tab(self):
        """Cria aba de resumo."""
        summary_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(summary_frame, text="📊 Resumo Geral")
        
        self.summary_text = scrolledtext.ScrolledText(
            summary_frame, 
            height=15, 
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        
        # Texto inicial
        initial_text = """
🔍 COMPARADOR SPED FISCAL - AGUARDANDO COMPARAÇÃO

📋 INSTRUÇÕES:
1. Selecione os dois arquivos SPED nos campos acima
2. Clique no botão verde "COMPARAR ARQUIVOS SPED"
3. Aguarde o processamento (pode demorar para arquivos grandes)
4. Os resultados aparecerão aqui e na aba "Detalhes"

💡 DICA: O relatório HTML será gerado automaticamente para melhor visualização.
        """
        
        self.summary_text.insert(tk.END, initial_text)
        
    def create_details_tab(self):
        """Cria aba de detalhes com análise campo por campo."""
        details_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(details_frame, text="📋 Detalhes das Diferenças")
        
        # Criar PanedWindow para dividir a visualização
        paned_window = ttk.PanedWindow(details_frame, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Frame superior: Lista de diferenças
        top_frame = ttk.LabelFrame(paned_window, text="Lista de Diferenças", padding="5")
        paned_window.add(top_frame, weight=1)
        
        # Treeview para diferenças (mais compacto)
        columns = ('Tipo', 'Registro', 'Linha1', 'Linha2', 'Campos')
        self.details_tree = ttk.Treeview(top_frame, columns=columns, show='headings', height=8)
        
        # Configurar cabeçalhos
        self.details_tree.heading('Tipo', text='Tipo')
        self.details_tree.heading('Registro', text='Registro')
        self.details_tree.heading('Linha1', text='Arq1')
        self.details_tree.heading('Linha2', text='Arq2')
        self.details_tree.heading('Campos', text='Campos Alterados')
        
        # Configurar larguras
        self.details_tree.column('Tipo', width=100)
        self.details_tree.column('Registro', width=80)
        self.details_tree.column('Linha1', width=60)
        self.details_tree.column('Linha2', width=60)
        self.details_tree.column('Campos', width=200)
        
        # Scrollbars para treeview
        tree_v_scroll = ttk.Scrollbar(top_frame, orient="vertical", command=self.details_tree.yview)
        tree_h_scroll = ttk.Scrollbar(top_frame, orient="horizontal", command=self.details_tree.xview)
        self.details_tree.configure(yscrollcommand=tree_v_scroll.set, xscrollcommand=tree_h_scroll.set)
        
        # Layout do treeview
        self.details_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        tree_h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(0, weight=1)
        
        # Frame inferior: Detalhes da diferença selecionada
        bottom_frame = ttk.LabelFrame(paned_window, text="Detalhes da Diferença Selecionada", padding="5")
        paned_window.add(bottom_frame, weight=2)
        
        # Área de detalhes com scroll
        self.details_text = scrolledtext.ScrolledText(
            bottom_frame, 
            height=12, 
            font=('Consolas', 9),
            wrap=tk.WORD,
            bg='#f8f9fa'
        )
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        # Texto inicial
        initial_details = """
📋 DETALHES DAS DIFERENÇAS

👆 Clique em uma diferença na lista acima para ver os detalhes completos aqui.

🔍 O que será mostrado:
• Conteúdo completo dos registros
• Comparação campo por campo
• Valores antigos vs. novos
• Posição exata das diferenças
        """
        self.details_text.insert(tk.END, initial_details)
        
        # Bind para seleção no treeview
        self.details_tree.bind('<<TreeviewSelect>>', self.on_difference_selected)
        
    def create_visual_comparison_tab(self):
        """Cria aba de comparação visual lado a lado."""
        visual_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(visual_frame, text="👁️ Comparação Visual")
        
        # PanedWindow horizontal para dividir lado a lado
        visual_paned = ttk.PanedWindow(visual_frame, orient=tk.HORIZONTAL)
        visual_paned.pack(fill=tk.BOTH, expand=True)
        
        # Lado esquerdo: Arquivo 1
        left_frame = ttk.LabelFrame(visual_paned, text="📄 Arquivo 1", padding="5")
        visual_paned.add(left_frame, weight=1)
        
        self.visual_text1 = scrolledtext.ScrolledText(
            left_frame,
            font=('Consolas', 9),
            wrap=tk.NONE,
            bg='#fff5f5',
            height=20
        )
        self.visual_text1.pack(fill=tk.BOTH, expand=True)
        
        # Lado direito: Arquivo 2
        right_frame = ttk.LabelFrame(visual_paned, text="📄 Arquivo 2", padding="5")
        visual_paned.add(right_frame, weight=1)
        
        self.visual_text2 = scrolledtext.ScrolledText(
            right_frame,
            font=('Consolas', 9),
            wrap=tk.NONE,
            bg='#f5fff5',
            height=20
        )
        self.visual_text2.pack(fill=tk.BOTH, expand=True)
        
        # Frame inferior para controles
        control_frame = ttk.Frame(visual_frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(control_frame, text="🔍 Filtrar por registro:").pack(side=tk.LEFT)
        
        self.filter_var = tk.StringVar()
        filter_entry = ttk.Entry(control_frame, textvariable=self.filter_var, width=15)
        filter_entry.pack(side=tk.LEFT, padx=(5, 5))
        
        ttk.Button(control_frame, text="🔍 Filtrar", 
                  command=self.apply_visual_filter).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🗑️ Limpar Filtro", 
                  command=self.clear_visual_filter).pack(side=tk.LEFT, padx=5)
        
        # Texto inicial
        initial_visual = """
👁️ COMPARAÇÃO VISUAL LADO A LADO

📋 Como usar:
• Os arquivos serão mostrados lado a lado após a comparação
• Registros diferentes serão destacados
• Use o filtro para procurar registros específicos
• Scroll horizontal e vertical disponível

💡 Aguardando comparação...
        """
        
        self.visual_text1.insert(tk.END, initial_visual)
        self.visual_text2.insert(tk.END, initial_visual)
        
    def apply_visual_filter(self):
        """Aplica filtro na comparação visual."""
        if not self.comparator:
            messagebox.showwarning("Aviso", "Execute uma comparação primeiro.")
            return
            
        filter_text = self.filter_var.get().strip().upper()
        if not filter_text:
            self.update_visual_comparison()
            return
            
        # Filtrar registros
        self.update_visual_comparison(filter_record=filter_text)
        
    def clear_visual_filter(self):
        """Limpa o filtro da comparação visual."""
        self.filter_var.set("")
        if self.comparator:
            self.update_visual_comparison()
    
    def on_difference_selected(self, event):
        """Chamado quando uma diferença é selecionada no treeview."""
        selection = self.details_tree.selection()
        if not selection or not self.comparator:
            return
            
        # Obter índice da diferença selecionada
        item = self.details_tree.item(selection[0])
        values = item['values']
        
        if not values:
            return
            
        # Encontrar a diferença correspondente
        try:
            # O índice está armazenado como tag do item
            diff_index = int(self.details_tree.item(selection[0], 'tags')[0])
            difference = self.comparator.differences[diff_index]
            
            # Mostrar detalhes da diferença
            self.show_difference_details(difference)
            
        except (IndexError, ValueError):
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, "❌ Erro ao carregar detalhes da diferença selecionada.")
    
    def show_difference_details(self, difference):
        """Mostra os detalhes completos de uma diferença."""
        self.details_text.delete(1.0, tk.END)
        
        # Cabeçalho
        text = f"📋 DETALHES DA DIFERENÇA - REGISTRO {difference.record_type}\n"
        text += "=" * 60 + "\n\n"
        
        # Informações básicas
        if difference.difference_type == DifferenceType.RECORD_ADDED:
            text += "🟢 TIPO: Registro ADICIONADO\n"
            text += f"📍 LOCALIZAÇÃO: Linha {difference.line_number_file2} (apenas no arquivo 2)\n\n"
            
            text += "📄 CONTEÚDO DO REGISTRO:\n"
            text += "-" * 40 + "\n"
            text += f"{difference.record_file2.raw_line}\n\n"
            
            text += "🔍 CAMPOS DO REGISTRO:\n"
            text += "-" * 30 + "\n"
            for i, campo in enumerate(difference.record_file2.fields):
                text += f"Campo {i:2d}: {campo}\n"
                
        elif difference.difference_type == DifferenceType.RECORD_REMOVED:
            text += "🔴 TIPO: Registro REMOVIDO\n"
            text += f"📍 LOCALIZAÇÃO: Linha {difference.line_number_file1} (apenas no arquivo 1)\n\n"
            
            text += "📄 CONTEÚDO DO REGISTRO:\n"
            text += "-" * 40 + "\n"
            text += f"{difference.record_file1.raw_line}\n\n"
            
            text += "🔍 CAMPOS DO REGISTRO:\n"
            text += "-" * 30 + "\n"
            for i, campo in enumerate(difference.record_file1.fields):
                text += f"Campo {i:2d}: {campo}\n"
                
        elif difference.difference_type == DifferenceType.RECORD_MODIFIED:
            text += "🟡 TIPO: Registro MODIFICADO\n"
            text += f"📍 LOCALIZAÇÃO: Linhas {difference.line_number_file1} ↔ {difference.line_number_file2}\n"
            text += f"🔢 CAMPOS ALTERADOS: {len(difference.field_differences)}\n\n"
            
            # Mostrar registros completos
            text += "📄 CONTEÚDO COMPLETO DOS REGISTROS:\n"
            text += "-" * 45 + "\n"
            text += f"Arquivo 1: {difference.record_file1.raw_line}\n"
            text += f"Arquivo 2: {difference.record_file2.raw_line}\n\n"
            
            # Análise campo por campo
            text += "🔍 ANÁLISE CAMPO POR CAMPO:\n"
            text += "-" * 35 + "\n"
            
            # Determinar o maior número de campos
            max_fields = max(len(difference.record_file1.fields), len(difference.record_file2.fields))
            
            for i in range(max_fields):
                campo1 = difference.record_file1.fields[i] if i < len(difference.record_file1.fields) else "[VAZIO]"
                campo2 = difference.record_file2.fields[i] if i < len(difference.record_file2.fields) else "[VAZIO]"
                
                if campo1 != campo2:
                    text += f"\n🔴 CAMPO {i:2d} - DIFERENTE:\n"
                    text += f"   Arquivo 1: '{campo1}'\n"
                    text += f"   Arquivo 2: '{campo2}'\n"
                else:
                    text += f"\n✅ Campo {i:2d} - Idêntico: '{campo1}'\n"
            
            # Resumo das diferenças específicas
            if difference.field_differences:
                text += f"\n\n📊 RESUMO DAS {len(difference.field_differences)} DIFERENÇAS:\n"
                text += "-" * 40 + "\n"
                for field_diff in difference.field_differences:
                    text += f"• Campo {field_diff.field_index}: "
                    text += f"'{field_diff.old_value}' → '{field_diff.new_value}'\n"
        
        text += f"\n\n💡 Dica: Este é o registro SPED tipo '{difference.record_type}'\n"
        text += "Para mais detalhes sobre este tipo de registro, consulte a documentação SPED."
        
        self.details_text.insert(tk.END, text)
        
    def select_file(self, path_var):
        """Seleciona arquivo SPED."""
        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo SPED Fiscal",
            filetypes=[
                ("Arquivos SPED", "*.txt *.sped *.efd"),
                ("Arquivos texto", "*.txt"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if arquivo:
            path_var.set(arquivo)
            
    def select_html_file(self):
        """Seleciona local para salvar HTML."""
        arquivo = filedialog.asksaveasfilename(
            title="Salvar relatório HTML",
            defaultextension=".html",
            filetypes=[("Arquivos HTML", "*.html"), ("Todos os arquivos", "*.*")]
        )
        if arquivo:
            self.html_path.set(arquivo)
            
    def clear_all(self):
        """Limpa todos os campos."""
        self.arquivo1_path.set("")
        self.arquivo2_path.set("")
        self.summary_text.delete(1.0, tk.END)
        
        # Limpar treeview
        for item in self.details_tree.get_children():
            self.details_tree.delete(item)
            
        self.status_label.config(text="🗑️ Campos limpos - Pronto para nova comparação")
        
        # Restaurar texto inicial
        initial_text = """
🔍 COMPARADOR SPED FISCAL - AGUARDANDO COMPARAÇÃO

📋 INSTRUÇÕES:
1. Selecione os dois arquivos SPED nos campos acima
2. Clique no botão verde "COMPARAR ARQUIVOS SPED"
3. Aguarde o processamento (pode demorar para arquivos grandes)
4. Os resultados aparecerão aqui e na aba "Detalhes"

💡 DICA: O relatório HTML será gerado automaticamente para melhor visualização.
        """
        self.summary_text.insert(tk.END, initial_text)
        
    def validate_inputs(self):
        """Valida entradas do usuário."""
        if not self.arquivo1_path.get():
            messagebox.showerror("Erro", "❌ Por favor, selecione o primeiro arquivo SPED.")
            return False
            
        if not self.arquivo2_path.get():
            messagebox.showerror("Erro", "❌ Por favor, selecione o segunda arquivo SPED.")
            return False
            
        if not Path(self.arquivo1_path.get()).exists():
            messagebox.showerror("Erro", f"❌ Primeiro arquivo não encontrado:\n{self.arquivo1_path.get()}")
            return False
            
        if not Path(self.arquivo2_path.get()).exists():
            messagebox.showerror("Erro", f"❌ Segunda arquivo não encontrado:\n{self.arquivo2_path.get()}")
            return False
            
        return True
        
    def start_comparison(self):
        """Inicia comparação (função chamada pelo botão)."""
        if not self.validate_inputs():
            return
            
        # Desabilitar botão e mostrar progresso
        self.compare_button.config(state='disabled', text="⏳ Processando...", bg='#FFA500')
        self.progress_bar.start(10)
        self.status_label.config(text="🔄 Executando comparação... Aguarde.")
        
        # Executar em thread separada
        thread = threading.Thread(target=self.perform_comparison, daemon=True)
        thread.start()
        
    def perform_comparison(self):
        """Executa a comparação real."""
        try:
            # Criar comparador
            self.comparator = SpedComparator(self.arquivo1_path.get(), self.arquivo2_path.get())
            
            # Executar comparação
            differences = self.comparator.compare()
            
            # Gerar HTML se solicitado
            if self.gerar_html.get():
                report_generator = SpedReportGenerator(self.comparator)
                report_generator.generate_html_report(self.html_path.get())
            
            # Atualizar interface
            self.root.after(0, self.comparison_completed, differences)
            
        except Exception as e:
            self.root.after(0, self.comparison_error, str(e))
            
    def comparison_completed(self, differences):
        """Comparação concluída com sucesso."""
        # Reabilitar botão
        self.compare_button.config(state='normal', text="🔄 COMPARAR ARQUIVOS SPED", bg='#4CAF50')
        self.progress_bar.stop()
        
        # Atualizar resultados
        self.update_results()
        
        # Status final
        summary = self.comparator.get_summary()
        if summary['total_differences'] == 0:
            self.status_label.config(text="✅ Comparação concluída: Arquivos são IDÊNTICOS!")
            msg = "✅ ARQUIVOS SÃO IDÊNTICOS!\n\nNenhuma diferença foi encontrada entre os arquivos SPED."
        else:
            self.status_label.config(text=f"⚠️ Comparação concluída: {summary['total_differences']} diferenças encontradas")
            msg = f"""⚠️ DIFERENÇAS ENCONTRADAS

📊 Resumo:
• Total de diferenças: {summary['total_differences']}
• Registros adicionados: {summary['records_added']}
• Registros removidos: {summary['records_removed']}
• Registros modificados: {summary['records_modified']}

Verifique as abas "Resumo" e "Detalhes" para mais informações."""
        
        # Mostrar resultado
        messagebox.showinfo("Resultado da Comparação", msg)
        
        # Perguntar sobre HTML
        if self.gerar_html.get() and messagebox.askyesno("Abrir Relatório", 
                                                          "Deseja abrir o relatório HTML no navegador?"):
            webbrowser.open(f"file://{Path(self.html_path.get()).absolute()}")
            
    def comparison_error(self, error_msg):
        """Erro na comparação."""
        self.compare_button.config(state='normal', text="🔄 COMPARAR ARQUIVOS SPED", bg='#4CAF50')
        self.progress_bar.stop()
        self.status_label.config(text="❌ Erro na comparação")
        messagebox.showerror("Erro na Comparação", f"❌ Erro durante a comparação:\n\n{error_msg}")
        
    def update_results(self):
        """Atualiza as abas de resultados."""
        if not self.comparator:
            return
            
        # Atualizar resumo
        self.summary_text.delete(1.0, tk.END)
        
        summary = self.comparator.get_summary()
        
        text = "🔍 RELATÓRIO DE COMPARAÇÃO SPED FISCAL\n"
        text += "=" * 60 + "\n\n"
        text += f"📁 Arquivo 1: {Path(self.arquivo1_path.get()).name}\n"
        text += f"📁 Arquivo 2: {Path(self.arquivo2_path.get()).name}\n"
        text += f"🕒 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        text += "📊 ESTATÍSTICAS GERAIS\n"
        text += "-" * 40 + "\n"
        text += f"Total de diferenças: {summary['total_differences']}\n"
        text += f"Registros adicionados: {summary['records_added']}\n"
        text += f"Registros removidos: {summary['records_removed']}\n"
        text += f"Registros modificados: {summary['records_modified']}\n\n"
        text += f"Registros arquivo 1: {self.comparator.parser1.get_total_records()}\n"
        text += f"Registros arquivo 2: {self.comparator.parser2.get_total_records()}\n\n"
        
        if summary['total_differences'] == 0:
            text += "✅ RESULTADO: Os arquivos são IDÊNTICOS!\n"
        else:
            text += f"⚠️ RESULTADO: {summary['total_differences']} diferenças encontradas.\n"
            text += "\n💡 Veja a aba 'Detalhes' para informações completas.\n"
            
        if self.gerar_html.get():
            text += f"\n📝 Relatório HTML gerado em:\n{self.html_path.get()}\n"
            
        self.summary_text.insert(tk.END, text)
        
        # Atualizar detalhes
        for item in self.details_tree.get_children():
            self.details_tree.delete(item)
            
        for index, diff in enumerate(self.comparator.differences):
            tipo_icon = ""
            if diff.difference_type == DifferenceType.RECORD_ADDED:
                tipo_icon = "➕ Adicionado"
            elif diff.difference_type == DifferenceType.RECORD_REMOVED:
                tipo_icon = "➖ Removido"  
            elif diff.difference_type == DifferenceType.RECORD_MODIFIED:
                tipo_icon = "🔄 Modificado"
                
            linha1 = str(diff.line_number_file1) if diff.line_number_file1 else "-"
            linha2 = str(diff.line_number_file2) if diff.line_number_file2 else "-"
            
            # Informação mais detalhada sobre campos
            if diff.difference_type == DifferenceType.RECORD_MODIFIED and diff.field_differences:
                campo_info = f"{len(diff.field_differences)} campo"
                if len(diff.field_differences) > 1:
                    campo_info += "s"
                
                # Listar os primeiros campos alterados
                campos_alterados = []
                for field_diff in diff.field_differences[:3]:  # Mostrar até 3 campos
                    campos_alterados.append(f"C{field_diff.field_index}")
                
                if len(diff.field_differences) > 3:
                    campo_info += f" ({', '.join(campos_alterados)}...)"
                else:
                    campo_info += f" ({', '.join(campos_alterados)})" if campos_alterados else ""
                    
            elif diff.difference_type == DifferenceType.RECORD_ADDED:
                campo_info = f"Novo ({len(diff.record_file2.fields)} campos)"
            elif diff.difference_type == DifferenceType.RECORD_REMOVED:
                campo_info = f"Removido ({len(diff.record_file1.fields)} campos)"
            else:
                campo_info = "N/A"
                
            # Inserir com tag contendo o índice
            self.details_tree.insert('', tk.END, values=(
                tipo_icon, diff.record_type, linha1, linha2, campo_info
            ), tags=(str(index),))
        
        # Atualizar comparação visual
        self.update_visual_comparison()
        
    def update_visual_comparison(self, filter_record=None):
        """Atualiza a aba de comparação visual."""
        if not self.comparator:
            return
            
        # Limpar textos
        self.visual_text1.delete(1.0, tk.END)
        self.visual_text2.delete(1.0, tk.END)
        
        # Cabeçalhos
        header1 = f"📄 ARQUIVO 1: {Path(self.arquivo1_path.get()).name}\n"
        header1 += f"Total de registros: {self.comparator.parser1.get_total_records()}\n"
        header1 += "=" * 60 + "\n\n"
        
        header2 = f"📄 ARQUIVO 2: {Path(self.arquivo2_path.get()).name}\n"
        header2 += f"Total de registros: {self.comparator.parser2.get_total_records()}\n"
        header2 += "=" * 60 + "\n\n"
        
        self.visual_text1.insert(tk.END, header1)
        self.visual_text2.insert(tk.END, header2)
        
        # Se houver filtro, mostrar apenas registros filtrados
        if filter_record:
            self.show_filtered_records(filter_record)
        else:
            self.show_all_differences()
            
    def show_filtered_records(self, filter_record):
        """Mostra apenas registros que contêm o filtro."""
        records1 = self.comparator.parser1.get_records_by_type(filter_record)
        records2 = self.comparator.parser2.get_records_by_type(filter_record)
        
        if not records1 and not records2:
            self.visual_text1.insert(tk.END, f"❌ Nenhum registro tipo '{filter_record}' encontrado no arquivo 1\n")
            self.visual_text2.insert(tk.END, f"❌ Nenhum registro tipo '{filter_record}' encontrado no arquivo 2\n")
            return
            
        # Mostrar registros do tipo filtrado
        self.visual_text1.insert(tk.END, f"🔍 REGISTROS TIPO '{filter_record}' - ARQUIVO 1:\n\n")
        for record in records1:
            self.visual_text1.insert(tk.END, f"Linha {record.line_number}: {record.raw_line}\n")
            
        self.visual_text2.insert(tk.END, f"🔍 REGISTROS TIPO '{filter_record}' - ARQUIVO 2:\n\n")
        for record in records2:
            self.visual_text2.insert(tk.END, f"Linha {record.line_number}: {record.raw_line}\n")
            
    def show_all_differences(self):
        """Mostra todas as diferenças na comparação visual."""
        if not self.comparator.differences:
            self.visual_text1.insert(tk.END, "✅ ARQUIVOS SÃO IDÊNTICOS!\n")
            self.visual_text2.insert(tk.END, "✅ ARQUIVOS SÃO IDÊNTICOS!\n")
            return
            
        self.visual_text1.insert(tk.END, f"⚠️ DIFERENÇAS ENCONTRADAS ({len(self.comparator.differences)} total):\n\n")
        self.visual_text2.insert(tk.END, f"⚠️ DIFERENÇAS ENCONTRADAS ({len(self.comparator.differences)} total):\n\n")
        
        for i, diff in enumerate(self.comparator.differences[:20], 1):  # Mostrar até 20 diferenças
            if diff.difference_type == DifferenceType.RECORD_REMOVED:
                self.visual_text1.insert(tk.END, f"{i:2d}. ➖ REMOVIDO (Linha {diff.line_number_file1}):\n")
                self.visual_text1.insert(tk.END, f"    {diff.record_file1.raw_line}\n\n")
                self.visual_text2.insert(tk.END, f"{i:2d}. ➖ [REGISTRO REMOVIDO]\n")
                self.visual_text2.insert(tk.END, f"    (não existe no arquivo 2)\n\n")
                
            elif diff.difference_type == DifferenceType.RECORD_ADDED:
                self.visual_text1.insert(tk.END, f"{i:2d}. ➕ [REGISTRO ADICIONADO]\n")
                self.visual_text1.insert(tk.END, f"    (não existe no arquivo 1)\n\n")
                self.visual_text2.insert(tk.END, f"{i:2d}. ➕ ADICIONADO (Linha {diff.line_number_file2}):\n")
                self.visual_text2.insert(tk.END, f"    {diff.record_file2.raw_line}\n\n")
                
            elif diff.difference_type == DifferenceType.RECORD_MODIFIED:
                self.visual_text1.insert(tk.END, f"{i:2d}. 🔄 MODIFICADO (Linha {diff.line_number_file1}):\n")
                self.visual_text1.insert(tk.END, f"    {diff.record_file1.raw_line}\n\n")
                self.visual_text2.insert(tk.END, f"{i:2d}. 🔄 MODIFICADO (Linha {diff.line_number_file2}):\n") 
                self.visual_text2.insert(tk.END, f"    {diff.record_file2.raw_line}\n\n")
                
        if len(self.comparator.differences) > 20:
            remaining = len(self.comparator.differences) - 20
            self.visual_text1.insert(tk.END, f"\n💡 ... e mais {remaining} diferenças (use filtro para ver registros específicos)")
            self.visual_text2.insert(tk.END, f"\n💡 ... e mais {remaining} diferenças (use filtro para ver registros específicos)")
        
    def show_help(self):
        """Mostra ajuda."""
        help_window = tk.Toplevel(self.root)
        help_window.title("Ajuda - Comparador SPED")
        help_window.geometry("600x500")
        help_window.transient(self.root)
        
        help_text = """
🔍 AJUDA - COMPARADOR SPED FISCAL

📋 COMO USAR A INTERFACE:

1️⃣ SELECIONAR ARQUIVOS
   • Clique nos botões "📂 Procurar..." 
   • Selecione os arquivos SPED que deseja comparar
   • Formatos aceitos: .txt, .sped, .efd

2️⃣ EXECUTAR COMPARAÇÃO
   • Clique no botão verde "🔄 COMPARAR ARQUIVOS SPED"
   • Aguarde o processamento (pode demorar)
   • Os resultados aparecerão nas abas

3️⃣ VISUALIZAR RESULTADOS
   • Aba "📊 Resumo": Visão geral das diferenças
   • Aba "📋 Detalhes": Lista completa + análise campo por campo
   • Aba "👁️ Comparação Visual": Arquivos lado a lado
   • Relatório HTML: Arquivo visual detalhado

🔍 DETALHES AVANÇADOS:
   • Na aba "Detalhes", clique em qualquer diferença para ver:
     - Conteúdo completo dos registros
     - Análise campo por campo
     - Valores antigos vs. novos
   • Na aba "Visual", use filtros para ver registros específicos

🔍 TIPOS DE DIFERENÇAS:
➕ Adicionado: Registro só existe no segunda arquivo
➖ Removido: Registro só existe no primeiro arquivo
🔄 Modificado: Registro existe em ambos mas é diferente

💡 DICAS:
• Para arquivos grandes, aguarde pacientemente
• O relatório HTML oferece melhor visualização
• Use "Limpar" para reiniciar a comparação

❓ PROBLEMAS COMUNS:
• Arquivo não encontrado: Verifique o caminho
• Formato inválido: Certifique-se que é SPED válido
• Demora no processamento: Normal para arquivos grandes
        """
        
        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(help_window, text="Fechar", command=help_window.destroy).pack(pady=10)
        
    def run(self):
        """Executa a aplicação."""
        self.root.mainloop()


def main():
    """Função principal."""
    try:
        app = SpedComparatorGUIFixed()
        app.run()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao iniciar aplicação:\n{str(e)}")


if __name__ == "__main__":
    main()