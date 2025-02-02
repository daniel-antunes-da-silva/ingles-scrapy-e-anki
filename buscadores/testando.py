from tkinter import filedialog


caminho = filedialog.asksaveasfilename(title='Selecione o local que deseja salvar', confirmoverwrite=True)
print(caminho)