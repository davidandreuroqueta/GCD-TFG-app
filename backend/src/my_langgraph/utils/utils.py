import os 

def get_promt(file_name: str) -> str:
    """Get the prompt for the agent."""
    prompt_path = "./prompts/" + file_name + ".txt" 
    
    if not prompt_path:
        raise ValueError(f"Prompt {file_name} no encontrado.")
    
    try:
        # Intentar resolver la ruta absoluta del archivo
        abs_path = os.path.abspath(os.path.expanduser(prompt_path))
        print(f"Intentando cargar prompt desde: {abs_path}")
        
        with open(abs_path, "r", encoding="utf-8") as file:
            prompt_content = file.read()
            
        if not prompt_content.strip():
            raise ValueError(f"El archivo de prompt {prompt_path} está vacío")
            
        return prompt_content
        
    except FileNotFoundError:
        raise ValueError(f"No se encontró el archivo de prompt en {prompt_path}")
    except PermissionError:
        raise ValueError(f"Sin permisos para leer el archivo de prompt en {prompt_path}")
    except Exception as e:
        raise ValueError(f"Error al leer el archivo de prompt {prompt_path}: {str(e)}")