import sqlite3
from model import CNH

DB_NAME = "cnhs.db"

# ================================
# Conexão e criação da tabela
# ================================
def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cnhs (
            registro TEXT PRIMARY KEY,
            nome TEXT,
            cpf TEXT,
            categoria TEXT,
            primeira_habilitacao TEXT,
            nascimento_data TEXT,
            nascimento_local TEXT,
            uf_nascimento TEXT,
            emissao TEXT,
            validade TEXT,
            identidade TEXT,
            emissor TEXT,
            uf_emissao TEXT,
            nacionalidade TEXT,
            filiacao1 TEXT,
            filiacao2 TEXT
        )
    """)
    conn.commit()
    conn.close()

# Criar tabela ao importar o módulo
criar_tabela()


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
        cnh_dict = nova_cnh.to_dict()

        conn = conectar()
        cursor = conn.cursor()

        campos = ", ".join(cnh_dict.keys())
        valores = ", ".join(["?" for _ in cnh_dict])
        cursor.execute(f"INSERT INTO cnhs ({campos}) VALUES ({valores})", tuple(cnh_dict.values()))

        conn.commit()
        conn.close()

        return cnh_dict

    except sqlite3.IntegrityError:
        raise ValueError("Já existe uma CNH com esse número de registro")
    except Exception as e:
        raise ValueError(f"Erro ao adicionar CNH: {str(e)}")


# ==========================================================
# Serviço: Listar CNHs
# ==========================================================
def listar_cnhs():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cnhs")
    colunas = [descricao[0] for descricao in cursor.description]
    resultados = cursor.fetchall()

    conn.close()

    return [dict(zip(colunas, linha)) for linha in resultados]


# ==========================================================
# Serviço: Atualizar CNH
# ==========================================================
def atualizar_cnh(cnh_registro, dados):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cnhs WHERE registro = ?", (cnh_registro,))
    if cursor.fetchone() is None:
        conn.close()
        raise IndexError("CNH não encontrada")

    # Atualiza apenas campos enviados
    for chave, valor in dados.items():
        campo = chave.lower()

        if campo == "categoria":
            valor = valor.upper()

        elif campo == "validade":
            from datetime import datetime
            valor = datetime.strptime(valor, "%d-%m-%Y").strftime("%d/%m/%Y")

        elif campo == "nome":
            valor = valor.title()

        elif campo == "cpf":
            cpf = valor.replace(".", "").replace("-", "")
            valor = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

        cursor.execute(f"UPDATE cnhs SET {chave} = ? WHERE registro = ?", (valor, cnh_registro))

    conn.commit()
    conn.close()

    return {"registro": cnh_registro, **dados}


# ==========================================================
# Serviço: Deletar CNH
# ==========================================================
def deletar_cnh(cnh_registro):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cnhs WHERE registro = ?", (cnh_registro,))
    if cursor.fetchone() is None:
        conn.close()
        raise IndexError("CNH não encontrada")

    cursor.execute("DELETE FROM cnhs WHERE registro = ?", (cnh_registro,))
    conn.commit()
    conn.close()

    return {"mensagem": "CNH deletada com sucesso", "registro": cnh_registro}
