from cx_Freeze import setup, Executable
import sys

# Caminho correto do arquivo principal
arquivo_principal = "app.py"

icone_arquivo = "imagens/icone_programa.ico"

# Configuração dos arquivos extras
build_exe_options = {
    "packages": ["requests", "openpyxl", "PIL", "customtkinter"],
    "include_files": [
        ("arquivos_extras", "arquivos_extras"),  # Mantém a pasta no build
        ("imagens", "imagens"),
    ],
    "include_msvcr": True,  # Inclui as DLLs do Visual C++ Redistributable
}

executables = [
    Executable(
        script=arquivo_principal,
        base="Win32GUI" if sys.platform == "win32" else None,
        target_name="Automated English Study.exe",
        icon=icone_arquivo
    )
]

setup(
    name="Automated English Study",
    version="1.0",
    description="Programa que automatiza a busca de significados de palavras em inglês, "
                "e traz frases contendo essas palavras. Além disso, gera um arquivo .xlsx,"
                " que serve para automatizar a inserção no aplicativo Anki, através da extensão AnkiConnect.",
    options={"build_exe": build_exe_options},
    executables=executables,
)
