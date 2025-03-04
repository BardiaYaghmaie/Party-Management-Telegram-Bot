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
        if not os.path.exists(GUEST_FILE):
            return {}
        try:
            with open(GUEST_FILE, "r") as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"Error loading guests from file: {e}")
            return {}

    def save_guests(self):
        try:
            with open(GUEST_FILE, "w") as file:
                json.dump(self.guests, file, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Error saving guests to file: {e}")

    def add_guest(self, user_id, guest_data):
        self.guests[user_id] = guest_data
        self.save_guests()

    def remove_guest(self, user_id):
        if user_id in self.guests:
            del self.guests[user_id]
            self.save_guests()

    async def load_guests_async(self):
        if not os.path.exists(GUEST_FILE):
            return {}
        try:
            async with aiofiles.open(GUEST_FILE, "r") as file:
                data = await file.read()
                return json.loads(data)
        except Exception as e:
            logger.error(f"Error loading guests from file asynchronously: {e}")
            return {}

    async def save_guests_async(self):
        try:
            async with aiofiles.open(GUEST_FILE, "w") as file:
                await file.write(json.dumps(self.guests, ensure_ascii=False, indent=4))
        except Exception as e:
            logger.error(f"Error saving guests to file asynchronously: {e}")
