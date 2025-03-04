import json
import os
import pytest
from guest_manager import GuestManager, BASE_PATH, GUEST_FILE

@pytest.fixture
def temp_guest_manager(tmp_path, monkeypatch):
    """Fixture to create a GuestManager instance with a temporary directory."""
    # Create a temporary directory for guest data
    test_dir = tmp_path / "party_bot"
    test_dir.mkdir()
    test_guest_file = test_dir / "guests.json"

    # Monkey-patch BASE_PATH and GUEST_FILE to use the temporary directory
    monkeypatch.setattr("guest_manager.BASE_PATH", str(test_dir))
    monkeypatch.setattr("guest_manager.GUEST_FILE", str(test_guest_file))

    # Initialize GuestManager with an empty guests dictionary
    gm = GuestManager()
    gm.guests = {}
    return gm

# --- In-Memory Operation Tests ---
def test_add_guest(temp_guest_manager):
    """Test adding a guest to the in-memory dictionary."""
    user_id = 123
    guest_data = {"name": "Alice", "song": "Song", "dress": "Formal", "status": "attending"}
    temp_guest_manager.add_guest(user_id, guest_data)
    assert user_id in temp_guest_manager.guests
    assert temp_guest_manager.guests[user_id]["name"] == "Alice"

def test_remove_guest(temp_guest_manager):
    """Test removing a guest from the in-memory dictionary."""
    user_id = 456
    guest_data = {"name": "Bob", "song": "Song", "dress": "Casual", "status": "attending"}
    temp_guest_manager.add_guest(user_id, guest_data)
    temp_guest_manager.remove_guest(user_id)
    assert user_id not in temp_guest_manager.guests

# --- Persistence Tests ---
def test_save_and_load_guests(temp_guest_manager):
    """Test saving guests to file and loading them in a new instance synchronously."""
    user_id = 123
    guest_data = {"name": "Alice", "song": "Song", "dress": "Formal", "status": "attending"}
    temp_guest_manager.add_guest(user_id, guest_data)
    temp_guest_manager.save_guests()

    # Create a new GuestManager instance to verify persistence
    new_gm = GuestManager()
    assert user_id in new_gm.guests
    assert new_gm.guests[user_id]["name"] == "Alice"

@pytest.mark.asyncio
async def test_save_and_load_guests_async(temp_guest_manager):
    """Test saving and loading guests asynchronously."""
    user_id = 456
    guest_data = {"name": "Bob", "song": "Song", "dress": "Casual", "status": "attending"}
    temp_guest_manager.add_guest(user_id, guest_data)
    await temp_guest_manager.save_guests_async()

    # Create a new GuestManager instance and load asynchronously
    new_gm = GuestManager()
    new_gm.guests = await new_gm.load_guests_async()
    assert user_id in new_gm.guests
    assert new_gm.guests[user_id]["name"] == "Bob"

# --- Error Handling Tests ---
def test_load_nonexistent_file(temp_guest_manager):
    """Test loading guests when the file does not exist."""
    # Ensure the guest file does not exist
    if os.path.exists(GUEST_FILE):
        os.remove(GUEST_FILE)
    gm = GuestManager()
    assert gm.guests == {}, "Expected empty dictionary when file does not exist"

def test_load_invalid_json(temp_guest_manager):
    """Test loading guests from a file with invalid JSON."""
    # Write invalid JSON to the guest file
    with open(GUEST_FILE, "w") as file:
        file.write("invalid json")
    gm = GuestManager()
    assert gm.guests == {}, "Expected empty dictionary when JSON is invalid"

# --- Full Cycle Test ---
def test_add_and_remove_guest_with_save(temp_guest_manager):
    """Test the full cycle of adding, saving, removing, and reloading guests."""
    user_id = 202
    guest_data = {"name": "Eve", "song": "Song", "dress": "Formal", "status": "attending"}
    temp_guest_manager.add_guest(user_id, guest_data)
    temp_guest_manager.save_guests()

    # Verify persistence in a new instance
    new_gm = GuestManager()
    assert user_id in new_gm.guests

    # Remove the guest and save
    new_gm.remove_guest(user_id)
    new_gm.save_guests()

    # Verify removal in a new instance
    final_gm = GuestManager()
    assert user_id not in final_gm.guests

# --- Edge Case Tests ---
def test_add_guest_minimal_data(temp_guest_manager):
    """Test adding a guest with minimal data and verifying persistence."""
    user_id = 303
    guest_data = {"name": "Minimal", "status": "attending"}
    temp_guest_manager.add_guest(user_id, guest_data)
    temp_guest_manager.save_guests()
    new_gm = GuestManager()
    assert user_id in new_gm.guests
    assert new_gm.guests[user_id]["name"] == "Minimal"
    assert "song" not in new_gm.guests[user_id]

def test_add_guest_special_characters(temp_guest_manager):
    """Test adding a guest with special characters and verifying persistence."""
    user_id = 404
    guest_data = {"name": "Alice & Bob", "song": "Song with 🎵", "dress": "Formal", "status": "attending"}
    temp_guest_manager.add_guest(user_id, guest_data)
    temp_guest_manager.save_guests()
    new_gm = GuestManager()
    assert user_id in new_gm.guests
    assert new_gm.guests[user_id]["name"] == "Alice & Bob"
    assert new_gm.guests[user_id]["song"] == "Song with 🎵"