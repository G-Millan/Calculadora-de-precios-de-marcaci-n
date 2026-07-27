"""
Wrapper para compatibilidad con Streamlit Cloud.

Este archivo existe para mantener la compatibilidad con Streamlit Cloud
que estaba configurado para ejecutar appSima.py.

La lógica real está en app.py
"""

from app import main

if __name__ == "__main__":
    main()
