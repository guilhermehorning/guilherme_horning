import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
import os
import subprocess
import tempfile

# Esconde a janela do console no Windows de forma mais suave
try:
    import win32gui
    import win32con
    import time
    
    # Pequeno delay para permitir que o Explorer se estabilize
    time.sleep(0.1)
    
    # Encontra e esconde apenas janelas de console
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd):
            class_name = win32gui.GetClassName(hwnd)
            window_text = win32gui.GetWindowText(hwnd)
            # Esconde apenas se for uma janela de console do Python
            if 'ConsoleWindowClass' in class_name or 'python' in window_text.lower():
                win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        return True
    
    win32gui.EnumWindows(callback, [])
    
except ImportError:
    pass  # Se win32gui não estiver instalado, ignora

# Arquivo de configuração
CONFIG_FILE = "suite_config.ini"

# Função para carregar configurações
def carregar_config():
    import configparser
    config = configparser.ConfigParser()
    
    # Valores padrão
    default_config = {
        'suite_dir': r"C:\ThomsonReuters\Suite-Teste_Local",
        'teste_dir': r"C:\thomsonreuters\taxone_automacao_qa\teste",
        'obtido_dir': r"C:\thomsonreuters\taxone_automacao_qa\arquivos\obtido",
        'esperado_dir': r"C:\thomsonreuters\taxone_automacao_qa\arquivos\esperado"
    }
    
    try:
        config.read(CONFIG_FILE)
        return {
            'suite_dir': os.path.normpath(config.get('Diretorios', 'suite_dir', fallback=default_config['suite_dir'])),
            'teste_dir': os.path.normpath(config.get('Diretorios', 'teste_dir', fallback=default_config['teste_dir'])),
            'obtido_dir': os.path.normpath(config.get('Diretorios', 'obtido_dir', fallback=default_config['obtido_dir'])),
            'esperado_dir': os.path.normpath(config.get('Diretorios', 'esperado_dir', fallback=default_config['esperado_dir']))
        }
    except:
        return default_config

# Função para salvar configurações
def salvar_config(config_dict):
    import configparser
    config = configparser.ConfigParser()
    config['Diretorios'] = config_dict
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

# Carrega as configurações iniciais
config = carregar_config()
suite_dir = config['suite_dir']
teste_dir = config['teste_dir']
obtido_dir = config['obtido_dir']
esperado_dir = config['esperado_dir']

class JanelaConfig(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configurar Diretórios")
        self.geometry("800x400")  # Aumentei a altura para 400
        self.minsize(800, 400)    # Define um tamanho mínimo
        
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Variáveis
        self.suite_var = tk.StringVar(value=suite_dir)
        self.teste_var = tk.StringVar(value=teste_dir)
        self.obtido_var = tk.StringVar(value=obtido_dir)
        self.esperado_var = tk.StringVar(value=esperado_dir)
        
        # Suite Directory
        frame = ttk.LabelFrame(main_frame, text="Diretório Suite-Teste Local", padding="5")
        frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.suite_var, width=100).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Procurar", command=lambda: self.selecionar_dir(self.suite_var)).pack(side=tk.LEFT, padx=5)
        
        # Teste Directory
        frame = ttk.LabelFrame(main_frame, text="Diretório de Testes", padding="5")
        frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.teste_var, width=100).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Procurar", command=lambda: self.selecionar_dir(self.teste_var)).pack(side=tk.LEFT, padx=5)
        
        # Obtido Directory
        frame = ttk.LabelFrame(main_frame, text="Diretório Obtido", padding="5")
        frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.obtido_var, width=100).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Procurar", command=lambda: self.selecionar_dir(self.obtido_var)).pack(side=tk.LEFT, padx=5)
        
        # Esperado Directory
        frame = ttk.LabelFrame(main_frame, text="Diretório Esperado", padding="5")
        frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.esperado_var, width=100).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Procurar", command=lambda: self.selecionar_dir(self.esperado_var)).pack(side=tk.LEFT, padx=5)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Salvar", command=self.salvar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side=tk.LEFT, padx=5)
        
        # Torna a janela modal
        self.transient(parent)
        self.grab_set()
    
    def selecionar_dir(self, var):
        dir = tk.filedialog.askdirectory(initialdir=var.get())
        if dir:
            var.set(dir)
    
    def salvar(self):
        global suite_dir, teste_dir, obtido_dir, esperado_dir
        
        # Atualiza as variáveis globais normalizando os caminhos
        suite_dir = os.path.normpath(self.suite_var.get())
        teste_dir = os.path.normpath(self.teste_var.get())
        obtido_dir = os.path.normpath(self.obtido_var.get())
        esperado_dir = os.path.normpath(self.esperado_var.get())
        
        # Salva no arquivo de configuração
        config_dict = {
            'suite_dir': suite_dir,
            'teste_dir': teste_dir,
            'obtido_dir': obtido_dir,
            'esperado_dir': esperado_dir
        }
        salvar_config(config_dict)
        
        # Atualiza a lista de subpastas
        combo_subpasta['values'] = listar_subpastas()
        
        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        self.destroy()

def abrir_config():
    """Abre a janela de configuração de diretórios"""
    JanelaConfig(root)

class JanelaCopia(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Copiar Entre Pastas")
        self.geometry("600x500")
        
        # Variáveis
        self.origem_var = tk.StringVar(value=obtido_dir)
        self.destino_var = tk.StringVar(value=esperado_dir)
        
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame origem
        origem_frame = ttk.LabelFrame(main_frame, text="Pasta de Origem", padding="5")
        origem_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Entry(origem_frame, textvariable=self.origem_var, width=70).pack(side=tk.LEFT, padx=5)
        ttk.Button(origem_frame, text="Procurar", command=self.selecionar_origem).pack(side=tk.LEFT, padx=5)
        
        # Frame destino
        destino_frame = ttk.LabelFrame(main_frame, text="Pasta de Destino", padding="5")
        destino_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Entry(destino_frame, textvariable=self.destino_var, width=70).pack(side=tk.LEFT, padx=5)
        ttk.Button(destino_frame, text="Procurar", command=self.selecionar_destino).pack(side=tk.LEFT, padx=5)
        
        # Lista de arquivos com scrollbar
        list_frame = ttk.LabelFrame(main_frame, text="Arquivos a serem copiados", padding="5")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para conter a lista e a scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Lista de arquivos
        self.lista_arquivos = tk.Listbox(list_container, width=70, height=15, 
                                       yscrollcommand=scrollbar.set)
        self.lista_arquivos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configura a scrollbar
        scrollbar.config(command=self.lista_arquivos.yview)
        
        # Frame para os botões no final da janela
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Centraliza os botões
        btn_container = ttk.Frame(btn_frame)
        btn_container.pack(anchor=tk.CENTER)
        
        # Botões com tamanho fixo
        ttk.Button(btn_container, text="Atualizar Lista", width=20, command=self.atualizar_lista).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_container, text="Copiar Arquivos", width=20, command=self.copiar_arquivos).pack(side=tk.LEFT, padx=10)
        
        # Atualiza a lista inicial
        self.atualizar_lista()
        
        # Configura o layout mínimo da janela
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())
        
        # Torna a janela modal
        self.transient(parent)
        self.grab_set()
    
    def selecionar_origem(self):
        pasta = tk.filedialog.askdirectory(initialdir=self.origem_var.get())
        if pasta:
            self.origem_var.set(pasta)
            self.atualizar_lista()
    
    def selecionar_destino(self):
        pasta = tk.filedialog.askdirectory(initialdir=self.destino_var.get())
        if pasta:
            self.destino_var.set(pasta)
    
    def atualizar_lista(self):
        self.lista_arquivos.delete(0, tk.END)
        origem = self.origem_var.get()
        if not os.path.exists(origem):
            messagebox.showerror("Erro", "Pasta de origem não encontrada")
            return
            
        for root, dirs, files in os.walk(origem):
            for file in files:
                caminho_completo = os.path.join(root, file)
                caminho_relativo = os.path.relpath(caminho_completo, origem)
                self.lista_arquivos.insert(tk.END, caminho_relativo)
    
    def copiar_arquivos(self):
        origem = self.origem_var.get()
        destino = self.destino_var.get()
        
        if not os.path.exists(origem):
            messagebox.showerror("Erro", "Pasta de origem não encontrada")
            return
        
        try:
            # Cria o diretório de destino se não existir
            os.makedirs(destino, exist_ok=True)
            
            # Copia os arquivos mantendo a estrutura
            total = self.lista_arquivos.size()
            copiados = 0
            
            for i in range(total):
                arquivo_rel = self.lista_arquivos.get(i)
                origem_path = os.path.join(origem, arquivo_rel)
                destino_path = os.path.join(destino, arquivo_rel)
                
                # Cria os diretórios necessários
                os.makedirs(os.path.dirname(destino_path), exist_ok=True)
                
                # Copia o arquivo
                import shutil
                shutil.copy2(origem_path, destino_path)
                copiados += 1
            
            messagebox.showinfo("Sucesso", f"{copiados} arquivos copiados com sucesso!")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar arquivos: {str(e)}")

def abrir_janela_copia():
    """Abre a janela de cópia entre pastas"""
    JanelaCopia(root)

def abrir_pasta_obtido():
    """Abre a pasta 'obtido' no explorador de arquivos"""
    try:
        os.startfile(obtido_dir)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir pasta 'obtido': {str(e)}")

def abrir_pasta_esperado():
    """Abre a pasta 'esperado' no explorador de arquivos"""
    try:
        os.startfile(esperado_dir)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir pasta 'esperado': {str(e)}")

def listar_subpastas():
    """Encontra a pasta específica do teste executado"""
    # Remove a extensão .xml do nome e extrai o prefixo (UT, CT, etc)
    nome_teste = os.path.splitext(xml_nome)[0]
    prefixo = nome_teste.split('_')[0]  # Pega UT ou CT
    
    # Monta o padrão de pasta que estamos procurando (ex: UT_SPED_FISCAL)
    padrao_pasta = f"{prefixo}_{modulo}"
    
    # Debug: mostra o que estamos procurando
    output_text.insert(tk.END, f"\nProcurando pasta com padrão: {padrao_pasta}\n")
    output_text.insert(tk.END, f"Em: {pasta_base}\n")
    
    # Primeiro procura a pasta do módulo (ex: UT_SPED_FISCAL)
    for item in os.listdir(pasta_base):
        caminho_item = os.path.join(pasta_base, item)
        if os.path.isdir(caminho_item) and item.startswith(padrao_pasta):
            # Depois procura a pasta da demanda (ADO...) dentro da pasta do módulo
            output_text.insert(tk.END, f"Encontrou pasta do módulo: {item}\n")
            output_text.insert(tk.END, f"Procurando pasta da demanda em: {caminho_item}\n")
            
            # Lista todas as pastas ADO dentro do módulo
            for subitem in os.listdir(caminho_item):
                caminho_subitem = os.path.join(caminho_item, subitem)
                if os.path.isdir(caminho_subitem) and subitem.startswith("ADO"):
                    output_text.insert(tk.END, f"Encontrou pasta da demanda: {subitem}\n")
                    return caminho_subitem
    
    output_text.insert(tk.END, "Nenhuma pasta encontrada com o padrão especificado\n")
    return None

def copiar_para_esperado():
    """Copia os arquivos da pasta obtido para a pasta esperado"""
    if not ultimo_teste['pasta'] or not ultimo_teste['xml']:
        messagebox.showerror("Erro", "Execute um teste primeiro")
        return
        
    try:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Iniciando processo de cópia...\n")
        output_text.insert(tk.END, f"Último teste executado: {ultimo_teste['pasta']}/{ultimo_teste['xml']}\n")
        
        # Encontra a pasta específica nos diretórios obtido e esperado
        pasta_obtido = encontrar_pasta_teste(obtido_dir, ultimo_teste['pasta'], ultimo_teste['xml'])
        if not pasta_obtido:
            messagebox.showerror("Erro", "Pasta do teste não encontrada em 'obtido'.\nExecute o teste primeiro.")
            return
            
        # Monta o caminho de destino espelhando a estrutura da pasta obtido
        subpath = os.path.relpath(pasta_obtido, obtido_dir)
        pasta_esperado = os.path.join(esperado_dir, subpath)
        
        if not os.path.exists(origem):
            messagebox.showerror("Erro", f"Pasta origem não encontrada: {origem}")
            return
            
        # Cria o diretório de destino se não existir
        os.makedirs(destino, exist_ok=True)
        
        # Função para copiar diretório recursivamente
        def copiar_recursivo(src, dst):
            if os.path.isdir(src):
                if not os.path.exists(dst):
                    os.makedirs(dst)
                for item in os.listdir(src):
                    s = os.path.join(src, item)
                    d = os.path.join(dst, item)
                    if os.path.isdir(s):
                        copiar_recursivo(s, d)
                    else:
                        if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                            import shutil
                            shutil.copy2(s, d)
                            output_text.insert(tk.END, f'Copiado: {item}\n')
        
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f'Copiando arquivos de:\n{origem}\npara:\n{destino}\n\n')
        copiar_recursivo(origem, destino)
        output_text.insert(tk.END, '\nCópia concluída com sucesso!\n')
        messagebox.showinfo("Sucesso", "Arquivos copiados com sucesso!")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao copiar arquivos: {str(e)}")
        output_text.insert(tk.END, f'\nErro ao copiar arquivos: {str(e)}\n')

def listar_subpastas():
    """Lista todas as subpastas do diretório de testes"""
    try:
        return [d for d in os.listdir(teste_dir) if os.path.isdir(os.path.join(teste_dir, d))]
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar subpastas: {str(e)}")
        return []

def listar_xmls(subpasta):
    """Lista todos os arquivos XML na subpasta selecionada"""
    if not subpasta:
        return []
    pasta = os.path.join(teste_dir, subpasta)
    try:
        return [f for f in os.listdir(pasta) if f.endswith('.xml')]
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar XMLs: {str(e)}")
        return []

def atualizar_xmls(*args):
    """Atualiza a lista de XMLs quando uma subpasta é selecionada"""
    subpasta = subpasta_var.get()
    xmls = listar_xmls(subpasta)
    combo_xml['values'] = xmls
    xml_var.set('')

def executar_suite():
    """Executa o SuiteTeste.jar com os parâmetros selecionados"""
    subpasta = subpasta_var.get()
    xml = xml_var.get()
    range_ = range_var.get().strip()

    if not subpasta or not xml:
        messagebox.showerror("Erro", "Selecione o agrupamento e o XML")
        return
    if not range_:
        messagebox.showerror("Erro", "Informe o range dos testes")
        return

    # Monta o caminho do XML usando os.path.join para evitar problemas com barras
    xml_abs_path = os.path.join(teste_dir, subpasta, xml)
    
    # Verifica se o arquivo XML existe
    if not os.path.isfile(xml_abs_path):
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f'Arquivo XML não encontrado: {xml_abs_path}\n')
        return

    # Exibe o caminho do XML para depuração
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f'Caminho XML usado: {xml_abs_path}\n')

    # Monta o caminho relativo do XML para o BAT usando os.path normalizando as barras
    xml_bat_path = os.path.normpath(xml_abs_path)
    # Remove a unidade de disco se presente para o comando Java
    if ':' in xml_bat_path:
        xml_bat_path = xml_bat_path.split(':', 1)[1]  # Remove C: mantendo o resto do caminho

    # Cria BAT temporário sem duplicar C:\
    bat_content = f'@echo off\nchcp 1252\ncd /d "{suite_dir}"\njava -jar SuiteTeste.jar "{xml_bat_path}" "RA{range_}" suitetesteAC.properties\n'
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False) as bat_file:
            bat_file.write(bat_content)
            bat_path = bat_file.name

        # Executa o BAT e captura a saída
        process = subprocess.Popen(
            bat_path, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            shell=True
        )

        # Exibe a saída em tempo real
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                output_text.insert(tk.END, output)
                output_text.see(tk.END)
                root.update()

        process.wait()
        os.unlink(bat_path)  # Remove o arquivo BAT temporário

    except Exception as e:
        output_text.insert(tk.END, f'\nErro ao executar os testes: {str(e)}\n')

# Criar a janela principal
root = tk.Tk()
root.title("Suite de Testes - AC")
root.geometry("800x600")

# Configurações para abrir de forma menos intrusiva
root.wm_state('normal')  # Garante que a janela seja normal, não maximizada
root.focus_set()  # Define foco na janela
root.lift()  # Traz para frente sem forçar foco total
root.attributes('-topmost', False)  # Não força ficar sempre no topo

# Frame principal
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Frame de configuração
config_frame = ttk.Frame(main_frame)
config_frame.pack(fill=tk.X, pady=5)
btn_config = ttk.Button(config_frame, text="Configurar Diretórios", command=abrir_config)
btn_config.pack(anchor=tk.NW, padx=5)

# Subpasta (Agrupamento)
lbl_subpasta = tk.Label(main_frame, text='Selecione o agrupamento:', font=('Arial', 12))
lbl_subpasta.pack(pady=5)
subpasta_var = tk.StringVar()
combo_subpasta = ttk.Combobox(main_frame, textvariable=subpasta_var, state='readonly', font=('Arial', 11))
combo_subpasta['values'] = listar_subpastas()
combo_subpasta.pack(pady=5)
combo_subpasta.bind('<<ComboboxSelected>>', atualizar_xmls)

# XML
lbl_xml = tk.Label(main_frame, text='Selecione o XML:', font=('Arial', 12))
lbl_xml.pack(pady=5)
xml_var = tk.StringVar()
combo_xml = ttk.Combobox(main_frame, textvariable=xml_var, state='readonly', font=('Arial', 11))
combo_xml.pack(pady=5)

# Range
lbl_range = tk.Label(main_frame, text='Informe o range (ex: 14;14 ou 0;0 para todos):', font=('Arial', 12))
lbl_range.pack(pady=5)
range_var = tk.StringVar()
entry_range = ttk.Entry(main_frame, textvariable=range_var, font=('Arial', 11))
entry_range.pack(pady=5)

# Frame para os botões
btn_frame = ttk.Frame(main_frame)
btn_frame.pack(pady=10)

# Botão executar
btn_executar = ttk.Button(btn_frame, text="Executar Testes", command=executar_suite)
btn_executar.pack(side=tk.LEFT, padx=5)

# Botões para acessar pastas
btn_obtido = ttk.Button(btn_frame, text="Abrir Pasta Obtido", command=abrir_pasta_obtido)
btn_obtido.pack(side=tk.LEFT, padx=5)

btn_esperado = ttk.Button(btn_frame, text="Abrir Pasta Esperado", command=abrir_pasta_esperado)
btn_esperado.pack(side=tk.LEFT, padx=5)

# Botão para copiar entre pastas
btn_copiar = ttk.Button(btn_frame, text="Copiar Entre Pastas", command=abrir_janela_copia)
btn_copiar.pack(side=tk.LEFT, padx=5)

# Área de saída
output_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=('Consolas', 10))
output_text.pack(expand=True, fill='both', padx=10, pady=10)

root.mainloop()