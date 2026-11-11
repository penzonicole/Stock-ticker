# Currency & Weather Dashboard - Project 4

A full-stack Django web application that fetches real-time currency exchange rates and weather forecasts from external APIs, logs historical query records in a database, exposes a custom REST API endpoint, and renders dynamic UI updates, line charts, and asynchronous table rendering using JavaScript `fetch()`.

---

## 🚀 Features & Extra Challenges Implemented

- **Multi-Currency Tracking:** Simultaneous real-time queries for USD/BRL, EUR/BRL, and BTC/BRL trading pairs via AwesomeAPI.
- **Real-Time Weather Integration:** Live weather conditions (temperature and wind speed) integrated using the Open-Meteo API with configurations loaded dynamically via `.env`.
- **Interactive Variation Chart:** Dynamic line chart built with Chart.js to visualize exchange rate fluctuations over time.
- **In-Memory Caching:** Performance optimization using `django.core.cache` (2-minute TTL) to reduce redundant API calls and prevent rate limiting.
- **Background Scheduled Tasks:** Custom Django management command (`python manage.py atualizar_cotacoes`) for scheduled automated background updates.
- **Resilience & Fault Tolerance:** Graceful error handling for network timeouts and API failures on both server-side (`try/except`) and client-side (`.catch()`).
- **REST API Endpoint:** Read-only endpoint at `/api/historico/` built with Django REST Framework (DRF) returning ordered query logs.

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Django 6, Django REST Framework
- **HTTP & Config:** Requests, Python-Dotenv
- **Frontend:** JavaScript ES6 (`fetch`, DOM Manipulation), Chart.js, HTML5/CSS3
- **Database:** SQLite (Development)

---

## 📸 Project Screenshots

### 1. Main Dashboard & Weather Widget
Overview of live weather data in Brasília, multi-currency conversion status (USD, EUR, BTC), active cache indicator badge, and the interactive Chart.js line graph displaying exchange rate variation over time.

![Main Dashboard & Weather Widget](![alt text](image.png))

---

### 2. Query History Table
Historical conversion log table rendered asynchronously via `fetch('/api/historico/')` without reloading the page, displaying trading pairs, monetary values, and precise timestamps.

![Query History Table](![alt text](image-1.png))

---

## ⚠️ Troubleshooting & Lessons Learned

During the development and testing phases, several technical challenges were identified and resolved:

1. **DevTools Offline Mode (`ERR_INTERNET_DISCONNECTED`):**
   - *Issue:* Enabling "Offline" in Chrome DevTools before refreshing caused Chrome's native offline page ("dino game") to block the HTML document entirely.
   - *Fix:* Loaded the HTML document first under normal network conditions, then toggled "Offline" in DevTools to test asynchronous `.catch()` handling on isolated `fetch()` calls.

2. **`NameError: name 'os' is not defined` in `views.py`:**
   - *Issue:* Attempted to retrieve environment variables using `os.environ.get()` inside `consultar_cotacao` without importing the module.
   - *Fix:* Added `import os` at the top of `painel/views.py`.

3. **Persistent Test Environment Variables (`COTACAO_URL`):**
   - *Issue:* Setting an invalid test URL (`XXX-YYY`) in the terminal caused error messages to persist across server restarts.
   - *Fix:* Cleared the environment variable in the active shell using `unset COTACAO_URL` (macOS/Linux) or `Remove-Item Env:\COTACAO_URL` (PowerShell).

4. **`Unknown command: 'atualizar_cotacoes'`:**
   - *Issue:* Django command auto-discovery failed because the management directory was named `comands` instead of `commands`.
   - *Fix:* Renamed the directory to `painel/management/commands/` adhering strictly to Django naming conventions.

---

## 📦 Getting Started

### Prerequisites
Ensure Python 3 and `pip` are installed on your system.

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <YOUR_REPOSITORY_URL>
   cd painelapi

   ## 👩‍💻 Author

Developed by Nicole — IESB 2026