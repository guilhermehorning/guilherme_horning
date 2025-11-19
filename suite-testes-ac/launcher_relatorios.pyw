#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher para Scripts de Relatório
Interface simples para executar os geradores de relatório
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
from datetime import datetime

class LauncherRelatorios:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Executar Geradores de Relatório")
        self.root.geometry("500x400")
        
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(main_frame, text="🗂️ Geradores de Relatório", 
                         font=('Arial', 16, 'bold'))
        titulo.pack(pady=(0, 20))
        
        # Descrição
        desc = tk.Label(main_frame, 
                       text="Escolha qual gerador de relatório executar:",
                       font=('Arial', 10))
        desc.pack(pady=(0, 20))
        
        # Botões grandes
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(expand=True)
        
        # Botão Relatório Simplificado
        btn_simples = tk.Button(btn_frame, 
                               text="📋 Relatório Simplificado\n\n" +
                                    "Gera um resumo conciso com:\n" +
                                    "• Empresas utilizadas\n" +
                                    "• Estabelecimentos\n" +
                                    "• Períodos por ano\n" +
                                    "• Estatísticas básicas",
                               font=('Arial', 10),
                               bg='#e8f5e8',
                               fg='#2d5a2d',
                               relief='raised',
                               bd=2,
                               padx=20,
                               pady=15,
                               command=self.executar_simplificado)
        btn_simples.pack(pady=10, fill=tk.X)
        
        # Botão Relatório Completo
        btn_completo = tk.Button(btn_frame,
                                text="📊 Relatório Completo\n\n" +
                                     "Gera análise detalhada com:\n" +
                                     "• Relatório CSV detalhado\n" +
                                     "• Resumo completo\n" +
                                     "• Agrupamento por estabelecimento\n" +
                                     "• Dados completos de todos os testes",
                                font=('Arial', 10),
                                bg='#e8f0ff',
                                fg='#1a4d80',
                                relief='raised',
                                bd=2,
                                padx=20,
                                pady=15,
                                command=self.executar_completo)
        btn_completo.pack(pady=10, fill=tk.X)
        
        # Botão Interface Gráfica
        btn_gui = tk.Button(btn_frame,
                           text="🖥️ Interface Gráfica\n\n" +
                                "Abre interface completa com:\n" +
                                "• Seleção de arquivos\n" +
                                "• Configurações avançadas\n" +
                                "• Log em tempo real\n" +
                                "• Controle total do processo",
                           font=('Arial', 10),
                           bg='#fff5e6',
                           fg='#804020',
                           relief='raised',
                           bd=2,
                           padx=20,
                           pady=15,
                           command=self.abrir_gui)
        btn_gui.pack(pady=10, fill=tk.X)
        
        # Status
        self.status_var = tk.StringVar(value="Pronto para usar")
        status_label = tk.Label(main_frame, textvariable=self.status_var,
                               font=('Arial', 9), fg='gray')
        status_label.pack(pady=(20, 0))
        
    def atualizar_status(self, mensagem):
        """Atualiza a mensagem de status"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"[{timestamp}] {mensagem}")
        self.root.update()
        
    def executar_simplificado(self):
        """Executa o gerador simplificado"""
        self.atualizar_status("Executando relatório simplificado...")
        
        try:
            result = subprocess.run(['python', 'gerar_relatorio_simplificado.py'], 
                                  capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                self.atualizar_status("✅ Relatório simplificado concluído!")
                
                # Extrai informações do output
                lines = result.stdout.split('\n')
                resumo = "Relatório gerado com sucesso!"
                for line in lines:
                    if "Total de testes:" in line:
                        resumo += f"\n{line}"
                    elif "Empresas:" in line:
                        resumo += f"\n{line}"
                    elif "Total de estabelecimentos:" in line:
                        resumo += f"\n{line}"
                
                messagebox.showinfo("Sucesso", resumo)
                
                # Abre pasta de relatórios
                pasta_relatorios = r"c:\thomsonreuters\Suite-Teste_Local\relatorios"
                if os.path.exists(pasta_relatorios):
                    os.startfile(pasta_relatorios)
                    
            else:
                error_msg = result.stderr or "Erro desconhecido"
                self.atualizar_status("❌ Erro no relatório simplificado")
                messagebox.showerror("Erro", f"Erro ao gerar relatório:\n{error_msg}")
                
        except FileNotFoundError:
            self.atualizar_status("❌ Script não encontrado")
            messagebox.showerror("Erro", "Arquivo gerar_relatorio_simplificado.py não encontrado!")
        except Exception as e:
            self.atualizar_status(f"❌ Erro: {str(e)}")
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def executar_completo(self):
        """Executa o gerador completo"""
        self.atualizar_status("Executando relatório completo...")
        
        try:
            result = subprocess.run(['python', 'gerar_relatorio_xml.py'], 
                                  capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                self.atualizar_status("✅ Relatório completo concluído!")
                messagebox.showinfo("Sucesso", 
                                   "Relatório completo gerado com sucesso!\n\n" +
                                   "Arquivos gerados:\n" +
                                   "• Relatório detalhado (CSV)\n" +
                                   "• Relatório resumido (TXT)\n" +
                                   "• Relatório por estabelecimento (TXT)")
                
                # Abre pasta de relatórios
                pasta_relatorios = r"c:\thomsonreuters\Suite-Teste_Local\relatorios"
                if os.path.exists(pasta_relatorios):
                    os.startfile(pasta_relatorios)
                    
            else:
                error_msg = result.stderr or "Erro desconhecido"
                self.atualizar_status("❌ Erro no relatório completo")
                messagebox.showerror("Erro", f"Erro ao gerar relatório:\n{error_msg}")
                
        except FileNotFoundError:
            self.atualizar_status("❌ Script não encontrado")
            messagebox.showerror("Erro", "Arquivo gerar_relatorio_xml.py não encontrado!")
        except Exception as e:
            self.atualizar_status(f"❌ Erro: {str(e)}")
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def abrir_gui(self):
        """Abre a interface gráfica"""
        self.atualizar_status("Abrindo interface gráfica...")
        
        try:
            subprocess.Popen(['pythonw', 'gerar_relatorio_gui.pyw'])
            self.atualizar_status("Interface gráfica aberta!")
            
        except FileNotFoundError:
            self.atualizar_status("❌ Interface não encontrada")
            messagebox.showerror("Erro", "Arquivo gerar_relatorio_gui.pyw não encontrado!")
        except Exception as e:
            self.atualizar_status(f"❌ Erro: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao abrir interface: {str(e)}")
    
    def executar(self):
        """Inicia o launcher"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LauncherRelatorios()
    app.executar()