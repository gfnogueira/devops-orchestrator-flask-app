import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_endpoint(client):
    """Test the main hello endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == "Hello from Flask DevOps App!"
    assert 'version' in data

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'checks' in data

def test_ready_endpoint(client):
    """Test readiness endpoint"""
    response = client.get('/ready')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'ready'

def test_metrics_endpoint(client):
    """Test Prometheus metrics endpoint"""
    response = client.get('/metrics')
    assert response.status_code == 200
    assert 'text/plain' in response.content_type

def test_data_api_endpoint(client):
    """Test the data API endpoint"""
    response = client.get('/api/data')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'data' in data
    assert data['count'] == 3
    assert len(data['data']) == 3

def test_not_found(client):
    """Test 404 handling"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Not found'

def test_metrics_collection(client):
    """Test that metrics are properly collected"""
    # Make some requests
    client.get('/')
    client.get('/health')
    client.get('/api/data')
    
    # Check metrics
    response = client.get('/metrics')
    metrics_text = response.data.decode('utf-8')
    
    # Verify that our custom metrics are present
    assert 'http_requests_total' in metrics_text
    assert 'http_request_duration_seconds' in metrics_text
