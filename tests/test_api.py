from app.exchange_client import ExchangeRateError, UnsupportedCurrencyError


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_convert_success(client, mocker):
    mocker.patch("app.service.get_rate", return_value=5.0)

    response = client.get("/convert?amount=200&currency=BRL")

    assert response.status_code == 200
    assert response.json() == {
        "amount_usd": 200.0,
        "currency": "BRL",
        "converted": 1000.0,
        "rate": 5.0,
    }


def test_convert_normalizes_lowercase_currency(client, mocker):
    mocker.patch("app.service.get_rate", return_value=5.0)

    response = client.get("/convert?amount=200&currency=brl")

    assert response.status_code == 200
    assert response.json()["currency"] == "BRL"


def test_convert_unsupported_currency_returns_400(client, mocker):
    mocker.patch(
        "app.service.get_rate",
        side_effect=UnsupportedCurrencyError("Currency 'XYZ' is not supported"),
    )

    response = client.get("/convert?amount=200&currency=XYZ")

    assert response.status_code == 400
    assert "not supported" in response.json()["detail"]


def test_convert_provider_down_returns_503(client, mocker):
    mocker.patch(
        "app.service.get_rate",
        side_effect=ExchangeRateError("Exchange rate provider is unavailable"),
    )

    response = client.get("/convert?amount=200&currency=BRL")

    assert response.status_code == 503


def test_convert_missing_parameters_returns_422(client):
    response = client.get("/convert")
    assert response.status_code == 422


def test_convert_invalid_amount_returns_422(client):
    response = client.get("/convert?amount=-5&currency=BRL")
    assert response.status_code == 422