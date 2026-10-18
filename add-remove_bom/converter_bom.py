import os
import argparse

def process_file(file_path, action):
    """
    Lê o arquivo e adiciona ou remove o BOM do UTF-8 conforme a ação desejada.
    """
    try:
        # Tenta ler o arquivo identificando e removendo o BOM se ele existir
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        
        has_bom = raw_data.startswith(b'\xef\xbb\xbf')
        
        # Se o arquivo já estiver no estado desejado, não faz nada
        if action == 'add' and has_bom:
            print(f"O arquivo já possui BOM: {file_path}")
            return
        if action == 'remove' and not has_bom:
            print(f"O arquivo já está sem BOM: {file_path}")
            return
            
        # Decodifica o conteúdo
        if has_bom:
            content = raw_data.decode('utf-8-sig')
        else:
            try:
                content = raw_data.decode('utf-8')
            except UnicodeDecodeError:
                # Caso o arquivo esteja em Windows-1252/ANSI, tenta converter para salvar corretamente
                content = raw_data.decode('cp1252')
        
        # Salva o arquivo com a nova codificação
        if action == 'add':
            with open(file_path, 'w', encoding='utf-8-sig') as f:
                f.write(content)
            print(f"🟢 BOM adicionado com sucesso: {file_path}")
        elif action == 'remove':
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"🔴 BOM removido com sucesso: {file_path}")
            
    except Exception as e:
        print(f"❌ Erro ao processar o arquivo {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Script para adicionar ou remover BOM (UTF-8) de arquivos.")
    parser.add_argument("caminho", help="Caminho do arquivo ou diretório para processar.")
    parser.add_argument("acao", choices=["add", "remove"], help="Escolha 'add' para adicionar o BOM ou 'remove' para remover.")
    parser.add_argument("--ext", default=".csv,.txt", help="Extensões de arquivo separadas por vírgula (padrão: .csv,.txt).")
    
    args = parser.parse_args()
    
    extensions = [ext.strip().lower() for ext in args.ext.split(',')]
    
    if os.path.isfile(args.caminho):
        process_file(args.caminho, args.acao)
    elif os.path.isdir(args.caminho):
        for root, _, files in os.walk(args.caminho):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    full_path = os.path.join(root, file)
                    process_file(full_path, args.acao)
    else:
        print("❌ Caminho inválido. Forneça um arquivo ou pasta existente.")

if __name__ == "__main__":
    main()
