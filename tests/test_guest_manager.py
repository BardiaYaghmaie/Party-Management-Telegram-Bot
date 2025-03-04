import json
import tempfile
import pytest
from guest_manager import GuestManager, BASE_PATH, GUEST_FILE


@pytest.fixture
def temp_guest_manager(tmp_path, monkeypatch):
    # Create a temporary directory for guest data
    test_dir = tmp_path / "party_bot"
    test_dir.mkdir()
    test_guest_file = test_dir / "guests.json"

    # Monkey-patch the BASE_PATH and GUEST_FILE used in guest_manager.py
    monkeypatch.setattr("guest_manager.BASE_PATH", str(test_dir))
    monkeypatch.setattr("guest_manager.GUEST_FILE", str(test_guest_file))

    gm = GuestManager()
    gm.guests = {}
    return gm


def test_add_guest(temp_guest_manager):
    user_id = 123
    guest_data = {"name": "Alice", "song": "Song", "dress": "Formal", "status": "attending"}
    temp_guest_manager.add_guest(user_id, guest_data)
    assert user_id in temp_guest_manager.guests
    assert temp_guest_manager.guests[user_id]["name"] == "Alice"


def test_remove_guest(temp_guest_manager):
    user_id = 456
    guest_data = {"name": "Bob", "song": "Song", "dress": "Casual", "status": "attending"}
    temp_guest_manager.add_guest(user_id, guest_data)
    temp_guest_manager.remove_guest(user_id)
    assert user_id not in temp_guest_manager.guests
