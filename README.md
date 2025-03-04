# Telegram Party Bot

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Telegram Party Bot** is a Python-based Telegram bot designed to simplify party planning by managing guest lists. Users can RSVP, provide their names, suggest songs for the party playlist, and choose their dress code (casual or formal). Built with the `python-telegram-bot` library, this bot communicates with users in **Persian (Farsi)**, making it ideal for Persian-speaking communities, while offering English documentation for developers.

**ربات تلگرام مهمانی** یک ربات مبتنی بر پایتون است که به شما کمک می‌کند لیست مهمانان مهمانی خود را به‌راحتی مدیریت کنید. کاربران می‌توانند حضور یا عدم حضور خود را اعلام کنند، نام خود را وارد کنند، آهنگی برای لیست پخش مهمانی پیشنهاد دهند و کد لباس خود (کژوال یا رسمی) را انتخاب کنند. این ربات به زبان **فارسی** با کاربران ارتباط برقرار می‌کند و برای جوامع پارسی‌زبان طراحی شده است.

## Features

- **RSVP Management**: Users can confirm or decline their attendance.
- **Guest Details**: Collects names, song suggestions, and dress code preferences.
- **Guest List Access**: Displays a list of attending guests with their details.
- **Admin Insights**: Provides an admin-only command to view attendance statistics.
- **Persian Interface**: Fully supports Persian (Farsi) for user interactions.
- **Dockerized Deployment**: Easy setup with Docker and Docker Compose.

## Installation

Follow these steps to set up the Telegram Party Bot on your system. You'll need [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed.

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/telegram-party-bot.git
cd telegram-party-bot
```

### Step 2: Configure Environment Variables
Create a `.env` file in the project root with the following variables:
```
TOKEN=your_telegram_bot_token
ADMIN_USER_ID=your_telegram_user_id
```
- **`TOKEN`**: Get this by creating a bot via [BotFather](https://t.me/botfather) on Telegram.
- **`ADMIN_USER_ID`**: Your Telegram user ID (find it by messaging [@userinfobot](https://t.me/userinfobot)).

### Step 3: Build and Run with Docker
```bash
docker-compose up --build
```
This command builds the Docker image and starts the bot. Once running, you can interact with it on Telegram.

## Usage

The bot communicates in **Persian (Farsi)** with users. Below are the instructions for both regular users and the admin.

### For Users

1. **Start the Bot**  
   Send the `/start` command to begin. The bot will respond with a welcome message in Persian and present three options:
   - **"میام"** (I'm coming)
   - **"نمیام"** (I'm not coming)
   - **"لیست مهمونا"** (Guest list)

2. **RSVP as Attending**  
   - Select **"میام"** to confirm attendance. The bot will guide you through these steps:
     - **نام شما؟** (Your name?): Enter your name.
     - **یه آهنگ پیشنهاد بده** (Suggest a song): Provide a song for the playlist.
     - **کد لباس؟ کژوال یا رسمی؟** (Dress code? Casual or Formal?): Choose **"کژوال"** or **"رسمی"**.
   - Once completed, your details are saved.

3. **Decline Attendance**  
   - Select **"نمیام"** if you’re not attending. You can change your response later by restarting with `/start`.

4. **View the Guest List**  
   - Choose **"لیست مهمونا"** to see all attending guests, including their names, song suggestions, and dress codes.  
   Example output:
   ```
   لیست مهمانان:
   1. علی - آهنگ: "شادمهر - عاشقتم" - کد لباس: رسمی
   2. سارا - آهنگ: "ابی - شب" - کد لباس: کژوال
   ```

### For Admins

- **View Statistics**  
  Send `/stats` to get the total number of attending guests.  
  Example response:  
  ```
  تعداد مهمانان حاضر: 5
  ```
  *Note*: This command is restricted to the user ID specified in `ADMIN_USER_ID`.

## Configuration

The bot relies on two environment variables, which must be defined in the `.env` file:

| Variable         | Description                                      | Example Value                   |
|------------------|--------------------------------------------------|---------------------------------|
| `TOKEN`          | Telegram Bot Token from BotFather                | `1234567890:ABCDEF...`         |
| `ADMIN_USER_ID`  | Telegram User ID of the admin                    | `123456789`                    |

Example `.env` file:
```
TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ
ADMIN_USER_ID=123456789
```

## Development

Interested in contributing or customizing the bot? Here’s what you need to know.

### Prerequisites
- **Python 3.10**: The bot’s runtime environment.
- **[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)**: Core library for Telegram integration.
- **[aiofiles](https://github.com/Tinche/aiofiles)**: For asynchronous file operations.

### Project Structure
- **`bot.py`**: Contains the bot’s logic and conversation handlers.
- **`guest_manager.py`**: Manages guest data and persists it to a JSON file.
- **`requirements.txt`**: Lists all Python dependencies.
- **`Dockerfile`**: Defines the Docker image.
- **`docker-compose.yml`**: Configures the Docker Compose setup.
- **`tests/`**: Directory for test files.

### Running Locally (Without Docker)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up the `.env` file (as above).
3. Run the bot:
   ```bash
   python bot.py
   ```

### Contributing
We welcome contributions! To get started:
1. Fork the repository.
2. Create a branch for your feature or fix: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Add feature XYZ"`.
4. Push your branch: `git push origin feature-name`.
5. Open a pull request with a detailed description of your changes.

## Testing

The project uses **[pytest](https://docs.pytest.org/)** for unit testing. Tests are located in the `tests` directory and cover the `GuestManager` class, persistence, and edge cases.

### Run Tests
```bash
pytest
```

To see detailed output:
```bash
pytest -v
```

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as per the license terms.

---

## Acknowledgments

- Thanks to the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) community for their amazing library.
- Special shoutout to Persian-speaking party planners who inspired this bot!

---

