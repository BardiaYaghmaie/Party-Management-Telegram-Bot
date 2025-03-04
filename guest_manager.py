import os
import json
import logging
import aiofiles

# Define paths
BASE_PATH = "/data/party_bot/"
GUEST_FILE = os.path.join(BASE_PATH, "guests.json")
logger = logging.getLogger(__name__)

class GuestManager:
    def __init__(self):
        os.makedirs(BASE_PATH, exist_ok=True)
        self.guests = self.load_guests()

    def load_guests(self):
        """Load guest data from file with specific exception handling."""
        if not os.path.exists(GUEST_FILE):
            return {}
        try:
            with open(GUEST_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            logger.warning(f"Guest file {GUEST_FILE} not found, returning empty dict")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {GUEST_FILE}: {e}")
            return {}
        except PermissionError as e:
            logger.critical(f"Permission denied accessing {GUEST_FILE}: {e}")
            raise

    def save_guests(self):
        """Save guest data to file with specific exception handling."""
        try:
            with open(GUEST_FILE, "w") as file:
                json.dump(self.guests, file, ensure_ascii=False, indent=4)
        except PermissionError as e:
            logger.critical(f"Permission denied writing to {GUEST_FILE}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error saving guests to file: {e}")

    def add_guest(self, user_id, guest_data):
        """Add a guest to the dictionary without saving."""
        self.guests[user_id] = guest_data

    def remove_guest(self, user_id):
        """Remove a guest from the dictionary without saving."""
        if user_id in self.guests:
            del self.guests[user_id]

    async def load_guests_async(self):
        """Asynchronously load guest data with specific exception handling."""
        if not os.path.exists(GUEST_FILE):
            return {}
        try:
            async with aiofiles.open(GUEST_FILE, "r") as file:
                data = await file.read()
                return json.loads(data)
        except FileNotFoundError:
            logger.warning(f"Guest file {GUEST_FILE} not found, returning empty dict")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {GUEST_FILE}: {e}")
            return {}
        except PermissionError as e:
            logger.critical(f"Permission denied accessing {GUEST_FILE}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading guests asynchronously: {e}")
            return {}

    async def save_guests_async(self):
        """Asynchronously save guest data with specific exception handling."""
        try:
            async with aiofiles.open(GUEST_FILE, "w") as file:
                await file.write(json.dumps(self.guests, ensure_ascii=False, indent=4))
        except PermissionError as e:
            logger.critical(f"Permission denied writing to {GUEST_FILE}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error saving guests asynchronously: {e}")