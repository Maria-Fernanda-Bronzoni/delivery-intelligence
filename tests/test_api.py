from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_rota_inicial():
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == (
        "Delivery Intelligence API funcionando!"
    )


def test_previsao_atraso():
    pedido = {
        "customer_state": "RJ",
        "quantidade_itens": 2,
        "valor_produtos": 150.0,
        "valor_frete": 25.0,
        "quantidade_vendedores": 1,
        "quantidade_estados_vendedores": 1,
        "tem_vendedor_mesmo_estado": 1,
        "tem_multiplos_vendedores": 0,
        "dia_semana_compra": 2,
        "hora_compra": 14,
        "mes_compra": 8,
        "prazo_estimado_dias": 20.0
    }

    resposta = client.post("/prever", json=pedido)

    assert resposta.status_code == 200

    resultado = resposta.json()

    assert resultado["risco_atraso"] in [0, 1]
    assert 0 <= resultado["probabilidade_atraso"] <= 1
    assert resultado["limiar_utilizado"] == 0.6

    classificacao_esperada = (
        "Atrasado"
        if resultado["risco_atraso"] == 1
        else "Não atrasado"
    )

    assert resultado["classificacao"] == classificacao_esperada


def test_pedido_incompleto():
    resposta = client.post("/prever", json={
        "customer_state": "RJ"
    })

    assert resposta.status_code == 422