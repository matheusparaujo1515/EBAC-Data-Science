import subprocess
import sys
from pathlib import Path

# Caminho para o diretório do projeto
project_path = Path("C:/Users/Matheus-Educar/Documents/Mod16")

# Caminho para o arquivo requirements.txt
requirements_path = project_path / "requirements.txt"

# Comando para listar as dependências instaladas
cmd = [sys.executable, "-m", "pip", "freeze"]

# Executa o comando e captura a saída
result = subprocess.run(cmd, capture_output=True, text=True)

# Verifica se a execução foi bem-sucedida
if result.returncode == 0:
    # Extrai a lista de dependências
    dependencies = result.stdout.splitlines()
    
    # Escreve as dependências no arquivo requirements.txt
    with open(requirements_path, "w") as file:
        for dependency in dependencies:
            file.write(dependency + "\n")
    
    print("Arquivo requirements.txt gerado com sucesso!")
else:
    print("Erro ao gerar o arquivo requirements.txt")
