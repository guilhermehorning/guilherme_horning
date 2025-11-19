# -*- coding: utf-8 -*-
"""
Sistema de Leitura de Arquivo TXT de Estorno de Débito
Baseado no layout CAT154-12
"""

import csv
import pandas as pd
from pathlib import Path
from typing import List, Dict
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os


class LeitorEstornoDebito:
    def __init__(self):
        self.layout_tipo1 = []
        self.layout_tipo2 = []
        self.dados_importados = []
        
        # Layout do Registro Tipo 2 - Registro de Estorno de Débito
        # Baseado na aba "Registro de Estorno de Débito" do Excel original
        self.layout_tipo2_manual = [
            '1 - Tipo "2" ( Estorno de Débitos)',
            '2 - CNPJ ou CPF do destinatário',
            '3 - IE do destinatário',
            '4 - Razão Social do destinatário',
            '5 - Código de Identificação da Unidade Cons.',
            '6 - Número da NFCEE objeto de estorno',
            '7 - Série da NFCEE objeto de estorno',
            '8 - Data de emissão',
            '9 - Data de vencimento',
            '10 - Valor Total (com 2 decimais)',
            '11 - BC ICMS (com 2 decimais)',
            '12 - ICMS (com 2 decimais)',
            '13 - Número da NFCEE substituta',
            '14 - Série da NFCEE substituta',
            '15 - Data de emissão',
            '16 - Data de vencimento',
            '17 - Valor Total (com 2 decimais)',
            '18 - BC ICMS (com 2 decimais)',
            '19 - ICMS (com 2 decimais)',
            '20 - Hipótese de estorno',
            '21 - Motivo do estorno'
        ]
    
    def carregar_layout_csv(self, caminho_csv: str):
        """Carrega o layout do Registro Tipo 1 do CSV"""
        try:
            # Ler linha por linha para ter mais controle
            with open(caminho_csv, 'r', encoding='latin-1', errors='ignore') as f:
                linhas = f.readlines()
            
            self.layout_tipo1 = []
            
            # Pular a linha de cabeçalho
            for i, linha in enumerate(linhas[1:], start=1):
                linha = linha.strip()
                if not linha:
                    continue
                
                # Separar por ;
                partes = linha.split(';')
                
                if len(partes) >= 2:
                    numero = partes[0].strip()  # Coluna N°
                    conteudo = partes[1].strip()  # Coluna CONTEÚDO
                    
                    if conteudo:
                        # Formato: "Nº - Nome do Campo"
                        campo_formatado = f"{numero} - {conteudo}"
                        self.layout_tipo1.append(campo_formatado)
            
            print(f"✓ Layout carregado: {len(self.layout_tipo1)} campos do Registro Tipo 1")
            return True
        except Exception as e:
            print(f"✗ Erro ao carregar layout: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def importar_txt(self, caminho_txt: str):
        """Importa o arquivo TXT e separa por tipo de registro"""
        try:
            with open(caminho_txt, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            
            self.dados_importados = []
            
            for linha in linhas:
                linha = linha.strip()
                if not linha:
                    continue
                
                campos = linha.split(';')
                tipo = campos[0]
                
                if tipo == '1':
                    # Registro de Controle
                    registro = {
                        'tipo': 1,
                        'campos': campos,
                        'layout': self.layout_tipo1
                    }
                elif tipo == '2':
                    # Registro de Estorno de Débito
                    registro = {
                        'tipo': 2,
                        'campos': campos,
                        'layout': self.layout_tipo2_manual
                    }
                
                self.dados_importados.append(registro)
            
            print(f"✓ Arquivo importado: {len(self.dados_importados)} registros")
            return True
        except Exception as e:
            print(f"✗ Erro ao importar TXT: {e}")
            return False
    
    def exibir_dados(self):
        """Exibe os dados importados com o mapeamento do layout"""
        if not self.dados_importados:
            print("Nenhum dado importado!")
            return
        
        for idx, registro in enumerate(self.dados_importados, 1):
            tipo = registro['tipo']
            campos = registro['campos']
            layout = registro['layout']
            
            print(f"\n{'='*80}")
            print(f"REGISTRO #{idx} - TIPO {tipo}")
            print(f"{'='*80}\n")
            
            # Mapeia campos com layout
            for i, valor in enumerate(campos):
                if i < len(layout):
                    nome_campo = layout[i]
                else:
                    nome_campo = f"Campo {i+1}"
                
                print(f"{nome_campo:50s} : {valor}")
            
            print(f"\n{'='*80}")
    
    def exportar_excel(self, caminho_saida: str):
        """Exporta os dados para Excel com formatação"""
        try:
            with pd.ExcelWriter(caminho_saida, engine='openpyxl') as writer:
                # Registro Tipo 1
                registros_tipo1 = [r for r in self.dados_importados if r['tipo'] == 1]
                if registros_tipo1:
                    dados = []
                    for reg in registros_tipo1:
                        linha = {}
                        for i, valor in enumerate(reg['campos']):
                            nome_campo = reg['layout'][i] if i < len(reg['layout']) else f"Campo {i+1}"
                            linha[nome_campo] = valor
                        dados.append(linha)
                    
                    df1 = pd.DataFrame(dados)
                    df1.to_excel(writer, sheet_name='Registro Controle', index=False)
                
                # Registro Tipo 2
                registros_tipo2 = [r for r in self.dados_importados if r['tipo'] == 2]
                if registros_tipo2:
                    dados = []
                    for reg in registros_tipo2:
                        linha = {}
                        for i, valor in enumerate(reg['campos']):
                            nome_campo = reg['layout'][i] if i < len(reg['layout']) else f"Campo {i+1}"
                            linha[nome_campo] = valor
                        dados.append(linha)
                    
                    df2 = pd.DataFrame(dados)
                    df2.to_excel(writer, sheet_name='Registro Estorno Débito', index=False)
            
            print(f"✓ Arquivo Excel exportado: {caminho_saida}")
            return True
        except Exception as e:
            print(f"✗ Erro ao exportar Excel: {e}")
            return False


class InterfaceGrafica:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Leitor de Estorno de Débito CAT154-12")
        self.root.geometry("1000x700")
        
        self.leitor = LeitorEstornoDebito()
        self.arquivo_csv = None
        self.arquivo_txt = None
        
        # Carregar CSV automaticamente se existir
        self.caminho_csv_default = r"c:\Users\6028437\Desktop\demandas\937908\DE_PARA_Geracao_Arq_Estorno_Debito_CAT154_12.csv"
        
        self.criar_interface()
        self.carregar_csv_automatico()
    
    def criar_interface(self):
        # Frame superior - Seleção de arquivos
        frame_arquivos = ttk.LabelFrame(self.root, text="Seleção de Arquivos", padding=10)
        frame_arquivos.pack(fill='x', padx=10, pady=5)
        
        # Layout CSV
        ttk.Label(frame_arquivos, text="Layout (CSV):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.label_csv = ttk.Label(frame_arquivos, text="Nenhum arquivo selecionado", foreground='gray')
        self.label_csv.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        ttk.Button(frame_arquivos, text="Selecionar", command=self.selecionar_csv).grid(row=0, column=2, padx=5, pady=5)
        
        # Arquivo TXT
        ttk.Label(frame_arquivos, text="Arquivo TXT:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.label_txt = ttk.Label(frame_arquivos, text="Nenhum arquivo selecionado", foreground='gray')
        self.label_txt.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        ttk.Button(frame_arquivos, text="Selecionar", command=self.selecionar_txt).grid(row=1, column=2, padx=5, pady=5)
        
        # Botão Processar
        ttk.Button(frame_arquivos, text="PROCESSAR", command=self.processar, 
                   style='Accent.TButton').grid(row=2, column=0, columnspan=3, pady=10)
        
        # Frame meio - Navegação de registros
        frame_nav = ttk.Frame(self.root)
        frame_nav.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(frame_nav, text="<< Anterior", command=self.registro_anterior).pack(side='left', padx=5)
        self.label_registro = ttk.Label(frame_nav, text="Nenhum registro carregado", font=('Arial', 10, 'bold'))
        self.label_registro.pack(side='left', padx=20)
        ttk.Button(frame_nav, text="Próximo >>", command=self.proximo_registro).pack(side='left', padx=5)
        
        # Frame visualização - Treeview
        frame_vis = ttk.LabelFrame(self.root, text="Dados do Registro", padding=10)
        frame_vis.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview para exibir dados
        self.tree = ttk.Treeview(frame_vis, columns=('Campo', 'Valor'), show='headings', height=20)
        self.tree.heading('Campo', text='Nome do Campo')
        self.tree.heading('Valor', text='Conteúdo')
        self.tree.column('Campo', width=400)
        self.tree.column('Valor', width=400)
        
        scrollbar = ttk.Scrollbar(frame_vis, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Frame inferior - Botões de ação
        frame_acoes = ttk.Frame(self.root)
        frame_acoes.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(frame_acoes, text="Exportar para Excel", command=self.exportar).pack(side='left', padx=5)
        ttk.Button(frame_acoes, text="Limpar", command=self.limpar).pack(side='left', padx=5)
        
        self.registro_atual = 0
    
    def carregar_csv_automatico(self):
        """Carrega o CSV automaticamente se o arquivo existir"""
        if os.path.exists(self.caminho_csv_default):
            if self.leitor.carregar_layout_csv(self.caminho_csv_default):
                self.arquivo_csv = self.caminho_csv_default
                nome_arquivo = os.path.basename(self.caminho_csv_default)
                self.label_csv.config(text=f"✓ {nome_arquivo}", foreground='green')
                messagebox.showinfo("Layout Carregado", f"Layout carregado automaticamente:\n{nome_arquivo}")
    
    def selecionar_csv(self):
        arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo de Layout (CSV)",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if arquivo:
            self.arquivo_csv = arquivo
            self.label_csv.config(text=Path(arquivo).name, foreground='green')
    
    def selecionar_txt(self):
        arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo TXT",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if arquivo:
            self.arquivo_txt = arquivo
            self.label_txt.config(text=Path(arquivo).name, foreground='green')
    
    def processar(self):
        if not self.arquivo_csv or not self.arquivo_txt:
            messagebox.showerror("Erro", "Selecione os dois arquivos antes de processar!")
            return
        
        # Carregar layout
        if not self.leitor.carregar_layout_csv(self.arquivo_csv):
            messagebox.showerror("Erro", "Falha ao carregar o layout CSV!")
            return
        
        # Importar TXT
        if not self.leitor.importar_txt(self.arquivo_txt):
            messagebox.showerror("Erro", "Falha ao importar o arquivo TXT!")
            return
        
        # Exibir primeiro registro
        self.registro_atual = 0
        self.exibir_registro()
        
        messagebox.showinfo("Sucesso", f"Arquivo processado!\n{len(self.leitor.dados_importados)} registros importados.")
    
    def exibir_registro(self):
        if not self.leitor.dados_importados:
            return
        
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Pegar registro atual
        registro = self.leitor.dados_importados[self.registro_atual]
        tipo = registro['tipo']
        campos = registro['campos']
        layout = registro['layout']
        
        # Atualizar label
        total = len(self.leitor.dados_importados)
        tipo_nome = "Registro Controle" if tipo == 1 else "Registro Estorno de Débito"
        self.label_registro.config(text=f"Registro {self.registro_atual + 1}/{total} - {tipo_nome}")
        
        # Preencher treeview
        for i, valor in enumerate(campos):
            nome_campo = layout[i] if i < len(layout) else f"Campo {i+1}"
            self.tree.insert('', 'end', values=(nome_campo, valor))
    
    def proximo_registro(self):
        if not self.leitor.dados_importados:
            return
        
        if self.registro_atual < len(self.leitor.dados_importados) - 1:
            self.registro_atual += 1
            self.exibir_registro()
    
    def registro_anterior(self):
        if not self.leitor.dados_importados:
            return
        
        if self.registro_atual > 0:
            self.registro_atual -= 1
            self.exibir_registro()
    
    def exportar(self):
        if not self.leitor.dados_importados:
            messagebox.showwarning("Aviso", "Nenhum dado para exportar!")
            return
        
        arquivo = filedialog.asksaveasfilename(
            title="Salvar como",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if arquivo:
            if self.leitor.exportar_excel(arquivo):
                messagebox.showinfo("Sucesso", f"Dados exportados com sucesso!\n{arquivo}")
                # Abrir arquivo
                os.startfile(arquivo)
    
    def limpar(self):
        self.leitor.dados_importados = []
        self.registro_atual = 0
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.label_registro.config(text="Nenhum registro carregado")
    
    def executar(self):
        self.root.mainloop()


# Modo de uso
if __name__ == "__main__":
    # Abre a interface gráfica por padrão
    app = InterfaceGrafica()
    app.executar()
