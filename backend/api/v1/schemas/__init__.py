from pydantic import BaseModel


class LancamentoCreateSchema(BaseModel):
    data_transacao: str
    valor: float
    descricao_original: str
    tipo_transacao: str


class MessageSchema(BaseModel):
    message: str
