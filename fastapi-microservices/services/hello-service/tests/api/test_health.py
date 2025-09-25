import pytest
from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    """
    Test health check endpoint
    """
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "service" in data  
    assert "version" in data
    assert "timestamp" in data
    
    assert data["status"] == "healthy"
    assert data["service"] == "hello-service"
    assert data["version"] == "1.0.0"

def test_health_check_includes_metrics(client: TestClient):
    """
    Test that health check includes system metrics
    """
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    
    data = response.json()
    assert "system_metrics" in data
    
    metrics = data["system_metrics"]
    assert "cpu_usage_percent" in metrics
    assert "memory_usage_percent" in metrics
    assert "memory_available_mb" in metrics
    assert "disk_usage_percent" in metrics
    assert "disk_free_gb" in metrics
    
    # Verify metrics are reasonable values
    assert 0 <= metrics["cpu_usage_percent"] <= 100
    assert 0 <= metrics["memory_usage_percent"] <= 100
    assert metrics["memory_available_mb"] > 0
    assert 0 <= metrics["disk_usage_percent"] <= 100
    assert metrics["disk_free_gb"] >= 0