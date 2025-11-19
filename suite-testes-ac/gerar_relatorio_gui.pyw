#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Relatório Simplificado - Versão GUI
Interface gráfica para gerar relatórios do CT_SPED_FISCAL.xml
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import xml.etree.ElementTree as ET
import re
from datetime import datetime
import os

class GeradorRelatorioGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gerador de Relatórios - CT_SPED_FISCAL")
        self.root.geometry("600x500")
        
        # Variáveis
        self.arquivo_xml = tk.StringVar()
        self.pasta_saida = tk.StringVar(value=r"c:\thomsonreuters\Suite-Teste_Local\relatorios")
        
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(main_frame, text="Gerador de Relatórios XML", 
                         font=('Arial', 14, 'bold'))
        titulo.pack(pady=(0, 20))
        
        # Seleção de arquivo XML
        xml_frame = ttk.LabelFrame(main_frame, text="Arquivo XML", padding="5")
        xml_frame.pack(fill=tk.X, pady=5)
        
        ttk.Entry(xml_frame, textvariable=self.arquivo_xml, width=70).pack(side=tk.LEFT, padx=5)
        ttk.Button(xml_frame, text="Procurar", command=self.selecionar_xml).pack(side=tk.LEFT)
        
        # Pasta de saída
        saida_frame = ttk.LabelFrame(main_frame, text="Pasta de Saída", padding="5")
        saida_frame.pack(fill=tk.X, pady=5)
        
        ttk.Entry(saida_frame, textvariable=self.pasta_saida, width=70).pack(side=tk.LEFT, padx=5)
        ttk.Button(saida_frame, text="Procurar", command=self.selecionar_pasta).pack(side=tk.LEFT)
        
        # Botões de ação
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Gerar Relatório Simplificado", 
                  command=self.gerar_simplificado).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Gerar Relatório Completo", 
                  command=self.gerar_completo).pack(side=tk.LEFT, padx=5)
        
        # Área de log
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=15)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configuração padrão
        self.arquivo_xml.set(r"c:\thomsonreuters\taxone_automacao_qa\teste\SPED\CT_SPED_FISCAL.xml")
        
    def log(self, mensagem):
        """Adiciona mensagem ao log"""
        self.log_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {mensagem}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def selecionar_xml(self):
        """Seleciona arquivo XML"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo XML",
            filetypes=[("Arquivos XML", "*.xml"), ("Todos os arquivos", "*.*")]
        )
        if arquivo:
            self.arquivo_xml.set(arquivo)
            
    def selecionar_pasta(self):
        """Seleciona pasta de saída"""
        pasta = filedialog.askdirectory(title="Selecionar pasta de saída")
        if pasta:
            self.pasta_saida.set(pasta)
            
    def extrair_dados_simplificado(self, caminho_xml):
        """Extrai dados de forma simplificada"""
        try:
            tree = ET.parse(caminho_xml)
            root = tree.getroot()
        except ET.ParseError as e:
            self.log(f"Erro ao processar XML: {e}")
            return None
        
        empresas = set()
        estabelecimentos = set()
        periodos = set()
        total_testes = 0
        
        for teste in root.findall('.//teste'):
            total_testes += 1
            
            # Extrai empresa
            for libparam in teste.findall('libparam'):
                if libparam.text and 'EMPRESA;' in libparam.text:
                    empresas.add(libparam.text.split(';')[1])
            
            # Extrai estabelecimentos e períodos
            for execpkg in teste.findall('execpkg'):
                if execpkg.text:
                    texto = execpkg.text
                    
                    # Estabelecimentos
                    padroes_estab = [
                        r"[Pp]cod_[Ee]stab\s*=>\s*'([^']+)'",
                        r"pcodestab\s*=>\s*'([^']+)'"
                    ]
                    
                    for padrao in padroes_estab:
                        matches = re.findall(padrao, texto)
                        estabelecimentos.update(matches)
                    
                    # Períodos
                    padroes_periodo = [
                        r"[Pp]dataini\s*=>\s*to_date\('([^']+)','dd/mm/yyyy'\)",
                        r"pmesanoapur\s*=>\s*to_date\('([^']+)','dd/mm/yyyy'\)"
                    ]
                    
                    for padrao in padroes_periodo:
                        matches = re.findall(padrao, texto)
                        for match in matches:
                            try:
                                mes_ano = '/'.join(match.split('/')[1:])
                                periodos.add(mes_ano)
                            except:
                                periodos.add(match)
        
        return {
            'total_testes': total_testes,
            'empresas': sorted(list(empresas)),
            'estabelecimentos': sorted(list(estabelecimentos)),
            'periodos': sorted(list(periodos))
        }
        
    def gerar_simplificado(self):
        """Gera relatório simplificado"""
        if not self.arquivo_xml.get():
            messagebox.showerror("Erro", "Selecione um arquivo XML")
            return
            
        if not os.path.exists(self.arquivo_xml.get()):
            messagebox.showerror("Erro", "Arquivo XML não encontrado")
            return
            
        self.log("Iniciando geração de relatório simplificado...")
        
        try:
            # Extrai dados
            dados = self.extrair_dados_simplificado(self.arquivo_xml.get())
            if dados is None:
                return
                
            # Cria pasta de saída
            pasta_saida = self.pasta_saida.get()
            os.makedirs(pasta_saida, exist_ok=True)
            
            # Nome do arquivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            arquivo_saida = os.path.join(pasta_saida, f"relatorio_simplificado_{timestamp}.txt")
            
            # Gera relatório
            with open(arquivo_saida, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("RELATÓRIO SIMPLIFICADO - CT_SPED_FISCAL.xml\n")
                f.write("=" * 60 + "\n")
                f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n\n")
                
                f.write(f"📊 TOTAL DE TESTES: {dados['total_testes']}\n\n")
                
                f.write("🏢 EMPRESAS UTILIZADAS:\n")
                f.write("-" * 25 + "\n")
                for i, empresa in enumerate(dados['empresas'], 1):
                    f.write(f"{i:2d}. {empresa}\n")
                f.write(f"\nTotal: {len(dados['empresas'])} empresa(s)\n\n")
                
                f.write("🏪 ESTABELECIMENTOS UTILIZADOS:\n")
                f.write("-" * 32 + "\n")
                estabs = dados['estabelecimentos']
                colunas = 4
                for i in range(0, len(estabs), colunas):
                    linha = ""
                    for j in range(colunas):
                        if i + j < len(estabs):
                            linha += f"{estabs[i+j]:<15}"
                    f.write(f"{linha}\n")
                f.write(f"\nTotal: {len(dados['estabelecimentos'])} estabelecimento(s)\n\n")
                
                f.write("📅 PERÍODOS UTILIZADOS (MÊS/ANO):\n")
                f.write("-" * 35 + "\n")
                por_ano = {}
                for periodo in dados['periodos']:
                    try:
                        if '/' in periodo:
                            partes = periodo.split('/')
                            if len(partes) >= 2:
                                ano = partes[1]
                                if ano not in por_ano:
                                    por_ano[ano] = []
                                por_ano[ano].append(partes[0])
                    except:
                        continue
                
                for ano in sorted(por_ano.keys()):
                    meses = sorted(set(por_ano[ano]), key=int)
                    f.write(f"{ano}: {', '.join(meses)}\n")
                
                f.write(f"\nTotal: {len(dados['periodos'])} período(s) diferentes\n\n")
                
                f.write("📈 ESTATÍSTICAS:\n")
                f.write("-" * 15 + "\n")
                if len(dados['empresas']) > 0:
                    f.write(f"• Média de testes por empresa: {dados['total_testes'] / len(dados['empresas']):.1f}\n")
                    f.write(f"• Estabelecimentos por empresa: {len(dados['estabelecimentos']) / len(dados['empresas']):.1f}\n")
                f.write(f"• Períodos diferentes: {len(dados['periodos'])}\n")
                
                f.write("\n" + "=" * 60 + "\n")
            
            self.log(f"✅ Relatório gerado: {arquivo_saida}")
            messagebox.showinfo("Sucesso", f"Relatório gerado com sucesso!\n\n{arquivo_saida}")
            
            # Abre a pasta
            os.startfile(pasta_saida)
            
        except Exception as e:
            self.log(f"❌ Erro: {e}")
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")
            
    def gerar_completo(self):
        """Chama o gerador completo"""
        self.log("Executando gerador de relatório completo...")
        try:
            import subprocess
            result = subprocess.run(['python', 'gerar_relatorio_xml.py'], 
                                  capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                self.log("✅ Relatório completo gerado com sucesso!")
                messagebox.showinfo("Sucesso", "Relatório completo gerado com sucesso!")
                # Abre a pasta de relatórios
                os.startfile(self.pasta_saida.get())
            else:
                self.log(f"❌ Erro: {result.stderr}")
                messagebox.showerror("Erro", f"Erro ao gerar relatório: {result.stderr}")
                
        except Exception as e:
            self.log(f"❌ Erro: {e}")
            messagebox.showerror("Erro", f"Erro ao executar: {e}")
    
    def executar(self):
        """Inicia a interface"""
        self.root.mainloop()

if __name__ == "__main__":
    app = GeradorRelatorioGUI()
    app.executar()