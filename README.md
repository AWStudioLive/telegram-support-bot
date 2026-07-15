# Telegram Support Bot 🤖

🌐 **Read this in other languages:** [Русский](#telegram-support-bot-ru)

An asynchronous Telegram bot designed to automate customer technical support.

The bot acts as a bridge between the customer and the administration: it forwards text inquiries, screenshots, and log files to a dedicated topic within the admin group, allowing operators to reply to users directly using Telegram's built-in functionality (Reply/Callback).

## 🛠 Tech Stack
* **Language:** Python 3.14 (Slim image in Docker)
* **Telegram API Library:** aiogram 3.x (Asynchronous development)
* **Configuration Validation:** Pydantic-Settings v2 (strict environment variables validation)
* **Logging:** Custom `StreamHandler` with color-coded levels for convenient debugging in the Docker console
* **Infrastructure:** Docker / Docker Compose

## 🚀 Key Architectural Decisions
* **Separation of Business Logic:** Event routing is divided into independent routers (`client_router` and `admin_router`).
* **Universal Media Handling:** The bot correctly processes and forwards regular text, configuration files, screenshots, or logs, while preserving the user's ID mapping.
* **"Claim Ticket" System:** Ticket locking via Callback buttons is implemented to prevent multiple administrators from sending duplicate responses.
* **Telegram Topics Integration:** Supports distributing incoming tickets into specific topics inside the admin group.

---

## 📦 Deployment Guide

### Step 1: Setting up Telegram Infrastructure

Before running the code, you need to set up the environment in Telegram:

1. **Create a bot:**
   * Message the official `@BotFather` bot and create a new bot using the `/newbot` command.
   * Save the received token (`TG_SUPPORT_BOT_TOKEN`).

2. **Create an administrator group (admin panel):**
   * Create a **public** or **private group** in Telegram that your support operators will join.
   * Add your newly created bot to this group and **grant it administrator privileges** (needed for editing messages and updating ticket statuses).
   * Make sure to enable the **Topics** toggle in the group settings.

3. **Create the required topics:**
   * Open the created group and create two topics:
     * A topic for incoming tickets (e.g., named `"Support"`).
     * A topic for system logs (e.g., named `"Logs / Errors"`).
   * Retrieve the group ID (`TG_ADMIN_GROUP_ID`) and the IDs of the created topics (`TG_TOPIC_SUPPORT_ID` and `TG_TOPIC_LOGS_ID`) for the `.env` configuration.

4. **Configure the environment file:**
   * Create a `.env` file in the root directory based on [.env.example](./.env.example) and fill in all the retrieved IDs and tokens.

---

### Step 2: Deployment Options

Choose the most convenient deployment option for your environment:

#### Option A: Running from a Pre-built Image (Docker Hub)
The fastest way to deploy the bot without downloading the source code. Create a local `.env` file with your tokens and run:

```bash
# 1. Pull the pre-built image
docker pull awstudiodev/titan-cloud-support-bot:latest

# 2. Run the container (passing the local .env configuration file)
docker run -d --name telegram-support-bot --env-file .env awstudiodev/titan-cloud-support-bot:latest
```

#### Option B: Running from Source Code (For Development)
If you want to customize the bot or run it locally:

```bash
# 1. Clone the repository (replace with your repository URL)
git clone <your_repository_url>
cd telegram-support-bot

# 2. Copy the configuration template and fill in your tokens
cp .env.example .env

# 3. Build and launch the project locally
docker compose up -d --build
```