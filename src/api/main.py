from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parents[2]
MODELS_DIR = BASE_DIR / "models"

modelo = joblib.load(MODELS_DIR / "modelo_atraso.pkl")
configuracao = joblib.load(MODELS_DIR / "configuracao.pkl")

limiar = configuracao["limiar"]

app = FastAPI(
    title="Delivery Intelligence API",
    description="API para previsão de risco de atraso em pedidos.",
    version="1.0.0"
)

class Pedido(BaseModel):
    customer_state: str = Field(min_length=2, max_length=2)
    quantidade_itens: int = Field(ge=1)
    valor_produtos: float = Field(ge=0)
    valor_frete: float = Field(ge=0)
    quantidade_vendedores: int = Field(ge=1)
    quantidade_estados_vendedores: int = Field(ge=1)
    tem_vendedor_mesmo_estado: int = Field(ge=0, le=1)
    tem_multiplos_vendedores: int = Field(ge=0, le=1)
    dia_semana_compra: int = Field(ge=0, le=6)
    hora_compra: int = Field(ge=0, le=23)
    mes_compra: int = Field(ge=1, le=12)
    prazo_estimado_dias: float = Field(gt=0)

@app.get("/")
def inicio():
    return {"mensagem": "Delivery Intelligence API funcionando!"}

@app.post("/prever")
def prever_atraso(pedido: Pedido):
    dados = pd.DataFrame([pedido.model_dump()])

    probabilidade = float(modelo.predict_proba(dados)[0][1])
    previsao = int(probabilidade >= limiar)

    return {
        "risco_atraso": previsao,
        "classificacao": "Atrasado" if previsao else "Não atrasado",
        "probabilidade_atraso": round(probabilidade, 4),
        "limiar_utilizado": limiar
    }