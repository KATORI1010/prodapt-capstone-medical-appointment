#!/bin/bash
set -e

# Backend
pip install -r requirements.txt
alembic upgrade head

# Frontend
cd frontend
npm install
npm run build