# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Python3 학습용 Flask 웹 애플리케이션. MariaDB 연동 및 세션 기반 로그인 기능을 포함한 간단한 학습 프로젝트입니다.

## Commands

### Setup & Run

```bash
# Activate virtual environment (PowerShell)
.venv\Scripts\Activate.ps1

# Activate virtual environment (bash)
source .venv/Scripts/activate

# Install dependencies
pip install flask mysql-connector-python

# Run development server (http://localhost:5000)
python app.py
```

### Install new packages

```bash
pip install <package-name>
```

## Architecture

All application logic lives in a single file, `app.py`:

- Flask app with `secret_key` for session management
- `db_config` / `get_db_connection()` — MariaDB connection to `192.168.57.81:3301`, database `test`
- Routes: `/` (index), `/about`, `/login` (GET/POST), `/logout`, `/test`
- Login uses MariaDB's `PASSWORD()` function to verify `tb_users.user_pw`
- Session stores `user_id` and `user_nm` after successful login
- Flash messages use categories `success`, `error`, `info` styled in templates

Templates in `templates/` use Jinja2. Inline CSS only — no separate stylesheet. Flash messages and session state are rendered directly in `index.html`.

## Database

MariaDB at `192.168.57.81:3301`, user `test1`, database `test`.  
Required table: `tb_users(user_id, user_nm, user_pw)` where `user_pw` is stored via `PASSWORD()`.
