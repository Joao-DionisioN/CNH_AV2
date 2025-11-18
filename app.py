from flask import Flask, request, jsonify, Response
import services
from model import CNH

app = Flask(__name__)

# ==========================================================
# Função util para respostas HTML estilizadas
# ==========================================================
def styled_response(title, content, color="#2b6cb0"):
    return Response(f"""
    <div style='font-family: Segoe UI, sans-serif; color: #222; padding: 30px;
                background: #f8f9fa; border-radius: 12px; width: 90%; max-width: 850px;
                margin: 40px auto; box-shadow: 0 0 15px rgba(0,0,0,0.1);'>
        <h2 style='color:{color}; text-align:center;'>{title}</h2>
        <pre style='background:#edf2f7; padding:15px; border-radius:8px; overflow-x:auto;
                    white-space:pre-wrap; font-size:14px;'>{content}</pre>
        <p style='font-size:13px; text-align:center; color:#666; margin-top:20px;'>
            Desenvolvido com 💻 Flask — por Nycole
        </p>
    </div>
    """, mimetype="text/html")

# ==========================================================
# Página inicial
# ==========================================================
@app.route('/')
def home():
    return styled_response(
        "🚦 API de Gestão de CNH",
        """Bem-vindo à API de Gestão de Carteiras Nacionais de Habilitação (CNH)!

Leia atentamente as instruções abaixo antes de usar qualquer rota:

Adicione o caminho ao final da URL (link da página) para acessar as rotas desejadas.
Ex: http://127.0.0.1:5000/help-add-cnh (adiciona /help-add-cnh à URL)

💡 Rotas de ajuda:
• /help-add-cnh       → Explica como ADICIONAR uma CNH passo a passo
• /help-list-cnh      → Explica como LISTAR todas as CNHs cadastradas
• /help-update-cnh    → Explica como ATUALIZAR campos de uma CNH existente
• /help-delete-cnh    → Explica como DELETAR uma CNH

📌 Dica: Sempre leia as rotas de ajuda antes de tentar adicionar, atualizar ou deletar CNHs.
Use "_" no lugar de espaços em nomes e cidades. Ex: João_Pessoa"""
    )

# ==========================================================
# Rota: Adicionar CNH (JSON)
# ==========================================================
@app.route("/cnhs", methods=["POST"])
def criar_cnh():
    if not request.is_json:
        return jsonify({"erro": "O corpo da requisição deve estar em formato JSON."}), 400
    try:
        dados = request.get_json(force=True)
        mensagem_retorno = services.adicionar_cnh(dados)
        return jsonify({
            "mensagem": "CNH adicionada com sucesso!",
            "cnh": mensagem_retorno
        }), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

# ==========================================================
# Rota: Listar CNHs (JSON)
# ==========================================================
@app.route("/cnhs", methods=["GET"])
def listar_cnhs():
    try:
        lista = services.listar_cnhs()
        return jsonify(lista), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar CNHs: {str(e)}"}), 500

# ==========================================================
# Rota: Atualizar CNH (JSON)
# ==========================================================
@app.route("/cnhs/<int:cnh_registro>", methods=["PUT"])
def atualizar_cnh(cnh_registro):
    if not request.is_json:
        return jsonify({"erro": "O corpo da requisição deve estar em formato JSON."}), 400
    try:
        dados = request.get_json(force=True)
        cnh_atualizada = services.atualizar_cnh(cnh_registro, dados)
        return jsonify({
            "mensagem": "CNH atualizada com sucesso!",
            "cnh": cnh_atualizada
        }), 200
    except IndexError as e:
        return jsonify({"erro": str(e)}), 404
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

# ==========================================================
# Rota: Deletar CNH (JSON)
# ==========================================================
@app.route("/cnhs/<int:cnh_registro>", methods=["DELETE"])
def deletar_cnh(cnh_registro):
    try:
        cnh_removida = services.deletar_cnh(cnh_registro)
        return jsonify({
            "mensagem": "CNH removida com sucesso!",
            "cnh": cnh_removida
        }), 200
    except IndexError as e:
        return jsonify({"erro": str(e)}), 404
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

# ==========================================================
# Rotas de ajuda (HTML estilizado)
# ==========================================================
@app.route('/help-add-cnh', methods=['GET'])
def help_add_cnh():
    return styled_response(
        "🆘 Adicionar CNH - Ajuda",
        """Como adicionar uma CNH passo a passo:

Envie uma requisição POST para /cnhs com o corpo em formato JSON.

📦 Exemplo de JSON:
{
  "nome": "João Silva",
  "primeira_habilitacao": "10-01-2020",
  "nascimento_data": "15-03-2002",
  "nascimento_local": "João Pessoa",
  "uf_nascimento": "PB",
  "emissao": "05-04-2023",
  "validade": "05-04-2033",
  "identidade": 1234567,
  "emissor": "SSP",
  "uf_emissao": "PB",
  "cpf": "12345678900",
  "registro": 987654321,
  "categoria": "AB",
  "nacionalidade": "Brasileiro",
  "filiacao1": "José Silva",
  "filiacao2": "Maria Silva"
}

💡 Envie via Postman, Insomnia ou qualquer cliente HTTP."""
    )

@app.route('/help-list-cnh', methods=['GET'])
def help_list_cnh():
    return styled_response(
        "📋 Listar CNHs - Ajuda",
        """Para listar todas as CNHs, envie uma requisição GET para:

➡️ /cnhs

O retorno será um array JSON com todas as CNHs cadastradas."""
    )

@app.route('/help-update-cnh', methods=['GET'])
def help_update_cnh():
    return styled_response(
        "🛠️ Atualizar CNH - Ajuda",
        """Para atualizar uma CNH existente:

Envie uma requisição PUT para /cnhs/&ltregistro&gt com o corpo em JSON.

📦 Exemplo de corpo:
{
  "categoria": "B",
  "validade": "05-04-2035"
}

💡 Apenas os campos enviados serão atualizados."""
    )

@app.route('/help-delete-cnh', methods=['GET'])
def help_delete_cnh():
    return styled_response(
        "🗑️ Deletar CNH - Ajuda",
        """Para deletar uma CNH existente:

Envie uma requisição DELETE para /cnhs/&ltregistro&gt

⚠️ Esta ação é irreversível!"""
    )

# ==========================================================
# Rodar aplicação
# ==========================================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
