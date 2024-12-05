import json


def test_health(client):
    """Test the health endpoint."""
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["status"] == "OK"


def test_count(client):
    """Test the count of pictures."""
    res = client.get("/count")
    assert res.status_code == 200
    assert "length" in res.json
    assert res.json["length"] >= 0  # Ensure count is non-negative


def test_data_contains_pictures(client):
    """Ensure pictures data is not empty."""
    res = client.get("/picture")
    assert res.status_code == 200
    assert isinstance(res.json, list)
    assert len(res.json) > 0  # Data should not be empty


def test_get_pictures_check_content_type_equals_json(client):
    """Check if the content type for pictures endpoint is JSON."""
    res = client.get("/picture")
    assert res.headers["Content-Type"] == "application/json"


def test_get_picture_by_id(client):
    """Test retrieving a picture by ID."""
    valid_id = 2
    res = client.get(f"/picture/{valid_id}")
    if res.status_code == 200:
        assert res.json["id"] == valid_id
    else:
        assert res.status_code == 404

    invalid_id = 404
    res = client.get(f"/picture/{invalid_id}")
    assert res.status_code == 404


def test_pictures_json_is_not_empty(client):
    """Verify that pictures data is not empty."""
    res = client.get("/picture")
    assert res.status_code == 200
    assert len(res.json) > 0  # Pictures data should have at least one item


def test_post_picture(client):
    """Test creating a new picture."""
    new_picture = {"id": 101, "event_city": "Phoenix"}
    res = client.post(
        "/picture", data=json.dumps(new_picture), content_type="application/json"
    )
    assert res.status_code == 201
    assert res.json["id"] == new_picture["id"]

    # Verify that the count increased
    res = client.get("/count")
    assert res.status_code == 200
    assert res.json["length"] > 0


def test_post_picture_duplicate(client):
    """Test duplicate picture creation."""
    picture = {"id": 102, "event_city": "Los Angeles"}
    
    # Clear existing data
    client.delete("/picture/clear")

    # Create a unique picture
    res = client.post(
        "/picture", data=json.dumps(picture), content_type="application/json"
    )
    assert res.status_code == 201

    # Attempt to post the same picture again
    res = client.post(
        "/picture", data=json.dumps(picture), content_type="application/json"
    )
    assert res.status_code == 409


def test_update_picture_by_id(client):
    """Test updating a picture by ID."""
    picture = {"id": 103, "event_city": "Dallas", "event_state": "TX"}
    client.post("/picture", data=json.dumps(picture), content_type="application/json")

    # Update the picture
    updated_data = {"event_city": "Houston", "event_state": "TX"}
    res = client.put(
        "/picture/103", data=json.dumps(updated_data), content_type="application/json"
    )
    assert res.status_code == 200
    assert res.json["event_city"] == "Houston"

    # Fetch and verify the updated picture
    res = client.get("/picture/103")
    assert res.status_code == 200
    assert res.json["event_city"] == "Houston"


def test_delete_picture_by_id(client):
    """Test deleting a picture by ID."""
    picture = {"id": 104, "event_city": "Chicago"}
    client.post("/picture", data=json.dumps(picture), content_type="application/json")

    # Verify initial count
    res = client.get("/count")
    initial_count = res.json["length"]

    # Delete the picture
    res = client.delete("/picture/104")
    assert res.status_code == 200
    assert res.json == {"message": "Picture deleted successfully"}

    # Verify count decreased
    res = client.get("/count")
    assert res.json["length"] == initial_count - 1

    # Verify the picture is no longer retrievable
    res = client.get("/picture/104")
    assert res.status_code == 404


def test_clear_pictures(client):
    """Test clearing all pictures."""
    res = client.delete("/picture/clear")
    assert res.status_code == 200
    assert res.json == {"message": "All pictures cleared"}

    # Verify that all pictures are cleared
    res = client.get("/picture")
    assert res.status_code == 404  # No pictures should exist
