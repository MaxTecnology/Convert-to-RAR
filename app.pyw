from tkinter import filedialog, Tk, Button, Label, StringVar, Toplevel
from tkinter.ttk import Progressbar
from pyunpack import Archive
import os
import zipfile
import shutil
import threading

def converter_rar_para_zip():
    global arquivo_rar
    if arquivo_rar:
        # Define o nome do arquivo ZIP baseado no nome do arquivo RAR
        arquivo_zip = os.path.splitext(arquivo_rar)[0] + '.zip'

        # Atualiza a label com o caminho do arquivo
        label_text.set(f'Arquivo selecionado: {arquivo_rar}\nConversão em andamento...')

        # Criando um diretório temporário para extrair os arquivos RAR
        temp_dir = "temp_dir"
        os.makedirs(temp_dir, exist_ok=True)

        # Extraindo o arquivo RAR
        Archive(arquivo_rar).extractall(temp_dir)

        # Criando o arquivo ZIP
        with zipfile.ZipFile(arquivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    zipf.write(os.path.join(root, file),
                               os.path.relpath(os.path.join(root, file),
                               temp_dir))

        # Apagando o diretório temporário
        shutil.rmtree(temp_dir)

        label_text.set(f'Arquivo convertido com sucesso! Arquivo ZIP: {arquivo_zip}')
        progress['value'] = 100
    else:
        label_text.set('Nenhum arquivo foi selecionado.')

def selecionar_arquivo():
    # Criando a janela de seleção de arquivo
    global arquivo_rar
    arquivo_rar = filedialog.askopenfilename(filetypes=[('Arquivos RAR', '*.rar')])  # Abre a janela de seleção de arquivo

    # Verifica se um arquivo foi selecionado
    if arquivo_rar:
        # Atualiza a label com o caminho do arquivo
        label_text.set(f'Arquivo selecionado: {arquivo_rar}\nPressione "Iniciar Conversão" para começar.')
        progress['value'] = 0
    else:
        label_text.set('Nenhum arquivo foi selecionado.')

def start_conversion():
    threading.Thread(target=converter_rar_para_zip).start()

# Criando a janela principal
root = Tk()
root.title('Conversor RAR para ZIP')

# Adicionando um botão para selecionar o arquivo
button_select = Button(root, text='Selecionar arquivo RAR', command=selecionar_arquivo)
button_select.pack(padx=10, pady=10)

# Adicionando um botão para iniciar a conversão
button_convert = Button(root, text='Iniciar Conversão', command=start_conversion)
button_convert.pack(padx=10, pady=10)

# Adicionando uma label para mostrar as mensagens
label_text = StringVar()
label = Label(root, textvariable=label_text)
label.pack(padx=10, pady=10)

# Adicionando uma barra de progresso
progress = Progressbar(root, length=200, mode='determinate')
progress.pack(padx=10, pady=10)

# Inicia a GUI
root.mainloop()
