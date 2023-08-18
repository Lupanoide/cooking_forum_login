
from fastapi.testclient import TestClient
from src.app.main import app


def test_docs_route():
    with TestClient(app) as test_client:
        response = test_client.get('/docs')
        assert response.status_code == 200


def test_check_single_signup_route():
    with TestClient(app) as test_client:
        response = test_client.post('/signup', json={
            'username': 'giancarlo@magal.li',
            'password': 'piazzaGrande',
            'name': 'Giancarlo',
            'surname': 'Magalli',
            })
        assert response.status_code == 201


def test_check_double_signup_route():
    with TestClient(app) as test_client:
        response = test_client.post('/signup', json={
            'username': 'michele@guar.di',
            'password': 'piazzaGrande',
            'name': 'Michele',
            'surname': 'Guardì',
            })
        assert response.status_code == 201
        response = test_client.post('/signup', json={
            'username': 'michele@guar.di',
            'password': 'piazzaGrande',
            'name': 'Michele',
            'surname': 'Guardì',
            })
        assert response.status_code == 409

def test_check_signup_unacceptable_user():
    with TestClient(app) as test_client:
        response = test_client.post('/signup', json={
            'username': 'maraVenier',
            'password': 'domenicaIn',
            'name': 'Mara',
            'surname': 'Venier',
            })
        assert response.status_code == 422

def test_check_signup_unacceptable_password():
    with TestClient(app) as test_client:
        response = test_client.post('/signup', json={
            'username': 'mara@eni.er',
            'password': '1234',
            'name': 'Mara',
            'surname': 'Venier',
            })
        assert response.status_code == 422

def test_check_linear_login():
    with TestClient(app) as test_client:
        response = test_client.post('/login',
                                    json={'username': 'giancarlo@magal.li'
                                    , 'password': 'piazzaGrande'})
        assert response.status_code == 200


def test_check_linear_login_with_wrong_password():
    with TestClient(app) as test_client:
        response = test_client.post('/login',
                                    json={'username': 'giancarlo@magal.li'
                                    , 'password': 'IFattiVostri'})
        assert response.status_code == 401


def test_check_inexistent_user_login():
    with TestClient(app) as test_client:
        response = test_client.post('/login',
                                    json={'username': 'carlo@con.ti',
                                    'password': 'LEredità'})
        assert response.status_code == 404


def test_check_generate_otp():
    with TestClient(app) as test_client:
        response = test_client.post('/signup', json={
            'username': 'simona@ventu.ra',
            'password': 'MaiDireGol',
            'name': 'Simona',
            'surname': 'Ventura',
            'two_factors_login_enabled': True,
            })
        assert response.status_code == 201
        response = test_client.post('/generate_otp',
                                    json={'username': 'simona@ventu.ra'
                                    })
        assert response.status_code == 200


def test_check_generate_otp_with_2fa_disabled():
    with TestClient(app) as test_client:
        response = test_client.post('/generate_otp',
                                    json={'username': 'giancarlo@magal.li'
                                    })
        assert response.status_code == 403


def test_check_generate_otp_inexistent_user():
    with TestClient(app) as test_client:
        response = test_client.post('/generate_otp',
                                    json={'username': 'carlo@con.ti'})
        assert response.status_code == 404


def test_check_validate_otp():
    with TestClient(app) as test_client:
        response = test_client.post('/validate_otp',
                                    json={'username': 'simona@ventu.ra'
                                    , 'otp': 'YLvbXXd1'})
    assert response.status_code == 401
