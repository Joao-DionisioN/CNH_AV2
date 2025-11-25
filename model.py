from datetime import datetime

# ==========================================================
# Modelo: CNH
# ==========================================================
class CNH:
    def __init__(
        self, nome, cpf, registro, categoria, primeira_habilitacao,
        nascimento_data, nascimento_local, uf_nascimento,
        emissao, validade, identidade, emissor, uf_emissao,
        nacionalidade, filiacao1, filiacao2
    ):
        self.nome = self.format_string(nome)
        self.cpf = self.format_cpf(cpf)
        self.registro = registro
        self.categoria = categoria.upper()
        self.primeira_habilitacao = self.formatar_data(primeira_habilitacao)
        self.nascimento_data = self.formatar_data(nascimento_data)
        self.nascimento_local = self.format_string(nascimento_local)
        self.uf_nascimento = uf_nascimento.upper()
        self.emissao = self.formatar_data(emissao)
        self.validade = self.formatar_data(validade)
        self.identidade = identidade
        self.emissor = emissor.upper()
        self.uf_emissao = uf_emissao.upper()
        self.nacionalidade = self.format_string(nacionalidade)
        self.filiacao1 = self.format_string(filiacao1)
        self.filiacao2 = self.format_string(filiacao2)

    # ==========================================================
    # Regras e utilitários de formatação (pertencem ao model)
    # ==========================================================
    @staticmethod
    def format_string(texto):
        return texto.replace("_", " ").title()

    @staticmethod
    def format_cpf(cpf):
        cpf = cpf.replace(".", "").replace("-", "")
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf

    @staticmethod
    def formatar_data(data_str):
        return datetime.strptime(data_str, "%d-%m-%Y").strftime("%d/%m/%Y")

    # ==========================================================
    # Representação em dicionário (para retorno de API)
    # ==========================================================
    def to_dict(self):
        return {
            "nome": self.nome,
            "primeira_habilitacao": self.primeira_habilitacao,
            "nascimento_data": self.nascimento_data,
            "nascimento_local": self.nascimento_local,
            "uf_nascimento": self.uf_nascimento,
            "emissao": self.emissao,
            "validade": self.validade,
            "identidade": self.identidade,
            "emissor": self.emissor, 
            "uf_emissao": self.uf_emissao,
            "cpf": self.cpf,
            "registro": self.registro,
            "categoria": self.categoria,
            "nacionalidade": self.nacionalidade,
            "filiacao1": self.filiacao1, 
            "filiacao2": self.filiacao2
        }
    