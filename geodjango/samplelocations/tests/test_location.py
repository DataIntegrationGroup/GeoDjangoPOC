"""
def test_get_geojson():
    response = client.get("/location/feature_collection")
    assert response.status_code == 200
    data = response.json()
    assert "type" in data
    assert data["type"] == "FeatureCollection"
    assert "features" in data
    assert len(data["features"]) > 0  # Assuming there are features in the collection


def test_get_shapefile():
    response = client.get("/location/shapefile")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/zip"
    assert "Content-Disposition" in response.headers
    assert (
        'attachment; filename="locations.zip"'
        == response.headers["Content-Disposition"]
    )
"""