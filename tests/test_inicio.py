from app import app

client = app.test_client()


def test_iniicio_status_code():
    resposta = client.get("/")

    assert resposta.status_code == 200


def test_inicio_message():
    resposta = client.get("/")

    assert resposta.get_data(as_text=True) == "Sistema de Gerenciamento Escolar"
