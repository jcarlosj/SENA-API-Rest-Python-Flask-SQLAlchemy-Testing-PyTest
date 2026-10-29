def test_health_endpoint_is_accessible(client):
    """Valida que la URL /health esté registrada y responda 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200

def test_users_endpoint_is_accessible(client):
    """Valida que la URL base de usuarios responda 200 OK."""
    response = client.get("/api/v1/users")
    assert response.status_code == 200

def test_url_not_found(client):
    """Valida que una URL inexistente responda con 404 Not Found."""
    response = client.get("/api/v1/ruta-inexistente")
    assert response.status_code == 404

def test_expected_routes_are_registered(app):
    """Verifica que las reglas de enrutamiento esperadas estén en la aplicación."""
    rutas_registradas = [rule.rule for rule in app.url_map.iter_rules()]

    rutas_esperadas = [
        "/health",
        "/api/v1/users",
        "/api/v1/users/<int:user_id>",
    ]

    for ruta in rutas_esperadas:
        assert ruta in rutas_registradas
