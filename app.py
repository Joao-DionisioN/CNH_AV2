from flask import Flask, request, jsonify, Response
import services
from model import CNH
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ==========================================================
# Função util para respostas HTML estilizadas
# ==========================================================
def styled_response(title, content, color="#2bb067"):
    return Response(f"""
    <div style='font-family: Segoe UI, sans-serif; color: #222; padding: 30px;
                background: #f8f9fa; border-radius: 12px; width: 90%; max-width: 850px;
                margin: 40px auto; box-shadow: 0 0 15px rgba(0,0,0,0.1);'>
        <h2 style='color:{color}; text-align:center;'>{title}</h2>
        <pre style='background:#edf2f7; padding:15px; border-radius:8px; overflow-x:auto;
                    white-space:pre-wrap; font-size:14px;'>{content}</pre>
        <p style='font-size:13px; text-align:center; color:#666; margin-top:20px;'>
            Desenvolvido com 💻 Flask — por Nycole e Dionisio
        </p>
    </div>
    """, mimetype="text/html")


def styled_page(title, html_content, color="#2bb067"):
    """Retorna uma página estilizada onde o conteúdo pode conter HTML (formulários, imagens etc.)."""
    return Response(f"""
    <div style='font-family: Segoe UI, sans-serif; color: #222; padding: 30px;
                background: #f8f9fa; border-radius: 12px; width: 90%; max-width: 850px;
                margin: 40px auto; box-shadow: 0 0 15px rgba(0,0,0,0.1);'>
        <h2 style='color:{color}; text-align:center;'>{title}</h2>
        <div style='background:#fff; padding:20px; border-radius:8px; font-size:14px; color:#222;'>
            {html_content}
        </div>
        <p style='font-size:13px; text-align:center; color:#666; margin-top:20px;'>
            Desenvolvido com 💻 Flask — por Nycole e Dionisio
        </p>
    </div>
    """, mimetype="text/html")


def smart_response(obj, status=200, title=None):
    """Retorna JSON para clientes API ou uma página estilizada quando o cliente aceita HTML.

    - Se o cliente aceitar HTML, exibimos o conteúdo (obj) como JSON formatado dentro de
      `styled_response` para manter o estilo das páginas de ajuda.
    - Caso contrário, retornamos `jsonify(obj)` com o status.
    """
    accept = request.headers.get('Accept', '')
    wants_html = request.accept_mimetypes.accept_html or 'text/html' in accept

    if wants_html:
        if isinstance(obj, str):
            content = obj
        else:
            try:
                content = json.dumps(obj, ensure_ascii=False, indent=2)
            except Exception:
                content = str(obj)

        page_title = title or (obj.get('mensagem') if isinstance(obj, dict) and 'mensagem' in obj else 'Resposta')
        return styled_response(page_title, content), status

    return jsonify(obj), status

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
        return smart_response({"erro": "O corpo da requisição deve estar em formato JSON."}, status=400)
    try:
        dados = request.get_json(force=True)
        mensagem_retorno = services.adicionar_cnh(dados)
        return smart_response({
            "mensagem": "CNH adicionada com sucesso!",
            "cnh": mensagem_retorno
        }, status=201, title="✅ CNH adicionada")
    except ValueError as e:
        return smart_response({"erro": str(e)}, status=400)
    except Exception as e:
        return smart_response({"erro": f"Erro interno: {str(e)}"}, status=500)

# ==========================================================
# Rota: Listar CNHs (JSON)
# ==========================================================
@app.route("/cnhs", methods=["GET"])
def listar_cnhs():
    try:
        lista = services.listar_cnhs()
        return smart_response(lista, status=200, title="📋 Lista de CNHs")
    except Exception as e:
        return smart_response({"erro": f"Erro ao listar CNHs: {str(e)}"}, status=500)

# ==========================================================
# Rota: Atualizar CNH (JSON)
# ==========================================================
@app.route("/cnhs/<int:cnh_registro>", methods=["PUT"])
def atualizar_cnh(cnh_registro):
    if not request.is_json:
        return smart_response({"erro": "O corpo da requisição deve estar em formato JSON."}, status=400)
    try:
        dados = request.get_json(force=True)
        cnh_atualizada = services.atualizar_cnh(cnh_registro, dados)
        return smart_response({
            "mensagem": "CNH atualizada com sucesso!",
            "cnh": cnh_atualizada
        }, status=200, title="🛠️ CNH atualizada")
    except IndexError as e:
        return smart_response({"erro": str(e)}, status=404)
    except Exception as e:
        return smart_response({"erro": f"Erro interno: {str(e)}"}, status=500)

# ==========================================================
# Rota: Deletar CNH (JSON)
# ==========================================================
@app.route("/cnhs/<int:cnh_registro>", methods=["DELETE"])
def deletar_cnh(cnh_registro):
    try:
        cnh_removida = services.deletar_cnh(cnh_registro)
        return smart_response({
            "mensagem": "CNH removida com sucesso!",
            "cnh": cnh_removida
        }, status=200, title="🗑️ CNH removida")
    except IndexError as e:
        return smart_response({"erro": str(e)}, status=404)
    except Exception as e:
        return smart_response({"erro": f"Erro interno: {str(e)}"}, status=500)

# ==========================================================
# Rota: Upload de arquivo (file)
# ==========================================================
# Config do upload
app.config["UPLOAD_FOLDER"] = services.UPLOAD_FOLDER


@app.route("/upload", methods=["GET", "POST"])
def upload():
    # Se for GET, retorna um formulário HTML estilizado para envio de arquivo
    if request.method == "GET":
        form_html = """
        <p>Envie um arquivo de imagem (PNG, JPG) ou PDF. O arquivo será enviado para o backend.</p>
        <form method='POST' action='/upload' enctype='multipart/form-data' style='display:flex; flex-direction:column; gap:12px;'>
            <input type='file' name='file' accept='.png,.jpg,.jpeg,.pdf' style='padding:8px;'/>
            <div style='display:flex; gap:8px;'>
                <button type='submit' style='background:#2b6cb0; color:#fff; border:none; padding:10px 14px; border-radius:8px; cursor:pointer;'>Enviar</button>
                <button type='reset' style='background:#edf2f7; color:#222; border:none; padding:10px 14px; border-radius:8px; cursor:pointer;'>Limpar</button>
            </div>
        </form>
        <hr/>
        <p style='font-size:13px; color:#555;'>Observação: Pasta de uploads: <strong>{}</strong></p>
        """.format(services.UPLOAD_FOLDER)

        return styled_page("📤 Upload de Arquivo", form_html)

    # POST: processa o upload enviado pelo formulário
    if "file" not in request.files:
        return smart_response({"erro": "Nenhum arquivo enviado"}, status=400)

    arquivo = request.files["file"]

    if arquivo.filename == "":
        return smart_response({"erro": "Nenhum arquivo selecionado"}, status=400)

    # Chama o service
    resultado = services.salvar_arquivo(arquivo)

    # Se o cliente aceitar HTML (navegador), mostramos uma página estilizada de sucesso
    accept = request.headers.get('Accept', '')
    if request.accept_mimetypes.accept_html or 'text/html' in accept:
        html = f"""
        <p><strong>Arquivo enviado com sucesso!</strong></p>
        <ul>
            <li>Nome original: {secure_filename(arquivo.filename)}</li>
            <li>Salvo em: {resultado.get('path', 'desconhecido')}</li>
            <li>Tamanho (bytes): {resultado.get('size', 'desconhecido')}</li>
        </ul>
        """
        return styled_page("✅ Upload concluído", html)

    return smart_response(resultado, status=200)

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
# Handlers de erro (HTML estilizado)
# ==========================================================
@app.errorhandler(404)
def not_found(error):
    return styled_response("404 — Não encontrado", "A rota solicitada não existe. Verifique a URL."), 404


@app.errorhandler(500)
def internal_error(error):
    return styled_response("500 — Erro interno", f"Ocorreu um erro interno: {str(error)}"), 500

# ==========================================================
# Rodar aplicação
# ==========================================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
