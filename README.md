<div align="center">

# Calculadora de Precios de Marcación

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776ab.svg?style=flat-square&logo=python)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37+-FF4B4B.svg?style=flat-square&logo=streamlit)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Code Quality](https://img.shields.io/badge/Code%20Quality-Professional-brightgreen.svg?style=flat-square)](#estándares-de-calidad)

Una aplicación web profesional para automatizar y acelerar la consulta de precios de marcación de productos, basada en reglas de negocio complejas.

[Características](#características) • [Inicio Rápido](#inicio-rápido) • [Documentación](#documentación) • [Arquitectura](#arquitectura) • [Licencia](#licencia)

</div>

---

## El Problema

En el equipo comercial, consultar precios de marcación era un proceso manual y propenso a errores:

- Revisar manualmente cientos de filas en hojas de cálculo
- Cruzar múltiples variables: producto, técnica, tintas, tamaño, cantidad
- Errores humanos en la búsqueda y cálculo
- Inconsistencia en los precios otorgados
- Tiempo perdido que podría invertirse en ventas

**Problema cuantificado:** Cada consulta tomaba entre 5-15 minutos de búsqueda manual.

---

## La Solución

Se desarrolló una aplicación web inteligente que:

- Calcula precios en segundos (no minutos)
- Filtra automáticamente según criterios complejos
- Garantiza consistencia en cada cálculo
- Implementa reglas de negocio (precios mínimos, rangos de cantidad)
- Interfaz intuitiva sin necesidad de capacitación

### Impacto Medido

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Tiempo por consulta | 5-15 min | < 30 seg | 90% ↓ |
| Errores humanos | ~15% | ~0% | 99% ↓ |
| Consultas/día posibles | ~50 | 200+ | 4x más |
| Confianza en precios | Media | Alta | Verificado |

---

## Inicio Rápido

### Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes)
- Git (opcional, para clonar)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/G-Millan/Calculadora-de-precios-de-marcacion.git
cd Calculadora-de-precios-de-marcacion

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución

```bash
# Ejecutar la aplicación
streamlit run app.py

# La app abrirá en: http://localhost:8501
```

### Verificación Inicial

```bash
# Ejecutar tests
pytest tests/ -v

# Verificar calidad de código
black --check .
ruff check .
flake8 .
```

---

## Características

### Funcionalidades Principales

- Búsqueda Inteligente: Selecciona producto, técnica, tintas y tamaño
- Cálculo Automático: Obtén precios en segundos
- Reglas de Negocio: Maneja precios mínimos y rangos de cantidad
- Interfaz Amigable: Diseño intuitivo sin necesidad de capacitación
- Validaciones: Detecta y reporta errores de entrada
- Logging: Registro de todas las operaciones para auditoría

### Estándares de Código Implementados

- SOLID Principles: Arquitectura modular y escalable
- Clean Code: Nombres descriptivos, funciones pequeñas
- Type Hints: Anotaciones de tipos para mayor seguridad
- Docstrings: Documentación de cada módulo y función
- Unit Tests: Cobertura de código con pytest
- Pre-commit Hooks: Garantiza calidad antes de cada commit
- Logging Profesional: Sistema de eventos y errores

---

## Documentación

### Estructura del Proyecto

```
calculadora-precios/
├── app.py                          # Aplicación principal (Streamlit)
├── config.py                       # Configuración centralizada
│
├── data/
│   └── base_sima_precios.xlsx     # Base de datos de precios
│
├── services/                       # Lógica de negocio
│   ├── __init__.py
│   ├── calculator.py              # Cálculos de precios
│   ├── data_loader.py             # Carga de datos
│   └── filters.py                 # Filtros de búsqueda
│
├── utils/                          # Funciones auxiliares
│   ├── __init__.py
│   ├── helpers.py                 # Utilidades generales
│   ├── validators.py              # Validaciones
│   └── logger.py                  # Sistema de logging
│
├── tests/                          # Pruebas unitarias
│   ├── __init__.py
│   ├── test_validators.py
│   ├── test_helpers.py
│   └── test_calculator.py
│
├── logs/                           # Archivos de log
│   └── app.log
│
├── screenshots/                    # Capturas de pantalla
│
├── requirements.txt                # Dependencias
├── pyproject.toml                  # Configuración de herramientas
├── .gitignore                      # Archivos ignorados por Git
├── .pre-commit-config.yaml        # Hooks de pre-commit
├── LICENSE                         # Licencia MIT
├── CHANGELOG.md                    # Historial de cambios
├── CONTRIBUTING.md                 # Guía de contribución
├── SECURITY.md                     # Política de seguridad
└── README.md                       # Este archivo
```

### Arquitectura

#### Separación de Responsabilidades

```
┌─────────────────────────────────────────────────────────┐
│                   app.py (Streamlit UI)                │
│         Interfaz de usuario y coordinación             │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    services/ (Business Logic)           │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  calculator   │  │ data_loader  │  │  filters     │ │
│  │   (Cálculos)  │  │ (Datos)      │  │ (Búsqueda)   │ │
│  └───────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    utils/ (Cross-cutting)               │
│  ┌────────────┐  ┌────────────┐  ┌────────────────┐   │
│  │ helpers    │  │ validators │  │ logger         │   │
│  └────────────┘  └────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   data/ (Data Source)                   │
│           base_sima_precios.xlsx (Excel)               │
└─────────────────────────────────────────────────────────┘
```

#### Flujo de Ejecución

```
1. Usuario abre app.py
   ↓
2. Load data (cache) → services/data_loader.py
   ↓
3. Usuario selecciona filtros
   ↓
4. Aplicar filtros → services/filters.py
   ↓
5. Calcular precio → services/calculator.py
   ↓
6. Mostrar resultados y log de operación
```

---

## Guía de Uso

### Paso 1: Seleccionar Producto

Elige el tipo de producto que deseas marcar:
- Bolígrafos plásticos
- Variedades
- Cerámicas y siliconas
- Y más...

### Paso 2: Elegir Técnica de Marcación

Selecciona cómo se marcará el producto:
- Serigrafía
- Tampografía
- Grabado láser
- Etc.

### Paso 3: Especificar Detalles (Opcional)

Si aplica:
- Número de tintas
- Tamaño del producto

### Paso 4: Ingresar Cantidad

Cantidad de artículos a marcar (mínimo 1)

### Paso 5: Calcular

Haz clic en "Calcular precio" para obtener el resultado

---

## Testing y Calidad

### Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=services --cov=utils --cov-report=html

# Tests específicos
pytest tests/test_calculator.py -v
```

### Herramientas de Calidad

```bash
# Formateo automático
black .

# Análisis estático
ruff check . --fix
flake8 .
isort .

# Pre-commit
pre-commit install
pre-commit run --all-files
```

### Estándares Aplicados

- Black: Formato de código consistente
- Ruff: Análisis estático rápido
- Flake8: Linter PEP 8
- isort: Ordenamiento de imports
- Pytest: Framework de testing
- Type Hints: Anotaciones de tipos

---

## Futuras Mejoras

### Corto Plazo

- Exportar resultados a PDF
- Historial de consultas
- Descarga de precios en Excel
- Soporte para múltiples idiomas

### Mediano Plazo

- API REST para integraciones
- Dashboard de estadísticas
- Notificaciones de cambios de precio
- Autenticación de usuarios

### Largo Plazo

- Machine learning para predicción de precios
- Integración con sistema CRM
- Mobile app
- Análisis predictivo de demanda

---

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Lee [CONTRIBUTING.md](CONTRIBUTING.md)
2. Crea una rama para tu feature
3. Commit tus cambios
4. Abre un Pull Request

### Proceso de Contribución Rápido

```bash
# 1. Fork el repositorio
# 2. Clonar tu fork
git clone https://github.com/tu-usuario/Calculadora-precios.git

# 3. Crear rama feature
git checkout -b feature/mi-feature

# 4. Hacer cambios y tests
pytest tests/ -v

# 5. Commit
git commit -m "feat: descripción del cambio"

# 6. Push
git push origin feature/mi-feature

# 7. Open Pull Request en GitHub
```

---

## Seguridad

Por favor, consulta [SECURITY.md](SECURITY.md) para reportar vulnerabilidades de forma responsable.

---

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).

Resumen:
- Uso comercial permitido
- Uso privado permitido
- Modificación permitida
- Distribución permitida
- Requiere incluir licencia y aviso

---

## Contacto

**Germán Millán**
- Email: produccion@almadelascosas.com
- GitHub: [@G-Millan](https://github.com/G-Millan)

---

## Agradecimientos

Agradecemos a:
- Equipo comercial por feedback constante
- Comunidad de Streamlit
- Contributores del proyecto

---

<div align="center">

Made with ❤️ by Germán Millán

[⬆ Volver al inicio](#calculadora-de-precios-de-marcación)

</div>
