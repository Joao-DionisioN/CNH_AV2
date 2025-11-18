from model import CNH

# Simulação de banco de dados
cnh_db = []

# ==========================================================
# Serviço: Adicionar CNH
# ==========================================================
def adicionar_cnh(dados):
    try:
        obrigatorios = ["nome", "cpf", "registro", "categoria"]
        for campo in obrigatorios:
            if campo not in dados or not dados[campo]:
                raise ValueError(f"O campo '{campo}' é obrigatório")

        nova_cnh = CNH(**dados)
        cnh_db.append(nova_cnh.to_dict())
        return nova_cnh.to_dict()
    except Exception as e:
        raise ValueError(f"Erro ao adicionar CNH: {str(e)}")

# ==========================================================
# Serviço: Listar CNHs
# ==========================================================
def listar_cnhs():
    return cnh_db

# ==========================================================
# Serviço: Atualizar CNH
# ==========================================================
def atualizar_cnh(cnh_registro, dados):
    cnh = next((item for item in cnh_db if item["Nº REGISTRO"] == cnh_registro), None)
    if not cnh:
        raise IndexError("CNH não encontrada")

    # Atualiza apenas campos enviados
    for chave, valor in dados.items():
        if chave.lower() == "categoria":
            cnh["CAT. HAB."] = valor.upper()
        elif chave.lower() == "validade":
            from datetime import datetime
            cnh["VALIDADE"] = datetime.strptime(valor, "%d-%m-%Y").strftime("%d/%m/%Y")
        elif chave.lower() == "nome":
            cnh["NOME E SOBRENOME"] = valor.title()
        elif chave.lower() == "cpf":
            cpf = valor.replace(".", "").replace("-", "")
            cnh["CPF"] = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        else:
            cnh[chave] = valor

    return cnh

# ==========================================================
# Serviço: Deletar CNH
# ==========================================================
def deletar_cnh(cnh_registro):
    global cnh_db
    cnh = next((item for item in cnh_db if item["Nº REGISTRO"] == cnh_registro), None)
    if not cnh:
        raise IndexError("CNH não encontrada")

    cnh_db = [item for item in cnh_db if item["Nº REGISTRO"] != cnh_registro]
    return cnh