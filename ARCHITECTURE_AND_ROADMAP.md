Personal Finance Tracker - Desktop Edition

1. Project Overview

This application is a local-first, offline-capable Desktop Application designed to help users track personal finances, manage accounts, and visualize spending habits.

Unlike traditional web apps, this runs entirely on the user's machine as a standalone executable (.exe), ensuring data privacy and zero latency.

2. Technical Architecture

The application uses a Hybrid Sidecar Architecture:

The Backend (Python/FastAPI)

Role: Acts as the local data engine and business logic handler.

Database: Uses SQLite (finances.db) stored locally alongside the executable.

ORM: SQLAlchemy is used for data modeling.

Server: Uses Uvicorn to run a local web server on a dynamically allocated free port.

Static Serving: Serves the compiled React frontend as static assets.

The Frontend (React/Vite)

Role: Provides the user interface.

Framework: React 18 with TypeScript.

Build Tool: Vite (for high-performance building).

Routing: React Router (SPA behavior).

API Communication: connects to the backend via relative paths (e.g., /api/v1/...).

The Wrapper (PyWebView)

Role: Wraps the local web server in a native Windows window.

Benefit: The user feels like they are using a native app, not a browser tab.

The Build System (PyInstaller)

Bundles the Python interpreter, all dependencies, and the compiled React assets into a single file (FinanceTracker.exe).

3. Current Features

🔐 Authentication (Local)

JWT Implementation: The app issues access and refresh tokens.

Demo Mode: Currently configured to allow local login without external validation for offline usage.

📊 Dashboard

Financial Overview: Visual summary of Total Balance, Income, and Expenses.

Interactive Cards: Quick view of monthly financial health.

💰 Account Management

Bank Connections: Integrated react-plaid-link frontend component to initiate bank connections.

Manual Accounts: Infrastructure to support manual entry of cash or offline accounts.

📈 Analytics & Reports

Spending Analysis: dedicated pages for visualizing transaction data.

Statements: Capability to upload CSV/PDF statements for parsing.

4. How to Build & Run

Prerequisites

Python 3.10+

Node.js 18+

Development Mode (Hot Reload)

Run Backend: cd backend && uvicorn app.main:app --reload

Run Frontend: cd frontend && npm run dev

Production Build (Executable)

Run the automated build script:

python build_exe.py


This will:

Install backend deps.

Install frontend deps.

Compile React to backend/app/static.

Freeze Python to backend/dist/FinanceTracker.exe.

5. Future Roadmap & Missing Features

The following features are planned for upcoming releases:

🚀 Phase 1: Core Functionality Completion

[ ] Real Plaid Integration: Connect the backend PlaidService to the frontend Link component to actually fetch live bank data.

[ ] Transaction Categorization: Implement the Categorizer service to auto-tag transactions based on keywords (e.g., "Uber" -> "Transport").

[ ] Data Persistence: Ensure the SQLite database migrates correctly when updating the .exe version.

🛡️ Phase 2: Security & Settings

[ ] Database Encryption: Use SQLCipher to encrypt finances.db at rest so files cannot be read if stolen.

[ ] PIN/Biometric Login: Add a Windows Hello or simple PIN screen before the main Dashboard loads.

[ ] Export/Import: Allow users to export their data to JSON/CSV for backup.

🎨 Phase 3: Advanced Analytics

[ ] Budgeting: Add a feature to set monthly limits per category.

[ ] Forecasting: Use the ai_advisor service to predict next month's spending based on history.

[ ] Dark Mode: Fully implement the ThemeContext toggling across all Tailwind components.

6. Troubleshooting Known Issues

Windows Path Issues: The build script uses os.path.join to ensure compatibility, but ensure you run build_exe.py from the root.

Port Conflicts: The app automatically scans for a free port, but firewall software may block the local server loopback (127.0.0.1).