# Guía de Contribución

¡Gracias por tu interés en contribuir a este proyecto! Este documento proporciona
directrices para ayudarte a colaborar de manera efectiva.

## Código de Conducta

Este proyecto se adhiere al [Código de Conducta](CODE_OF_CONDUCT.md).
Por favor, lee y respeta estas directrices al participar.

## ¿Cómo contribuir?

### Reportando Bugs

1. Verifica que el bug no haya sido reportado en Issues
2. Si no existe, crea un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs. actual
   - Tu entorno (Python version, OS, etc.)

### Sugerencias de Features

1. Describe claramente la feature y su caso de uso
2. Proporciona ejemplos si es posible
3. Explica por qué crees que sería útil

### Pull Requests

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código

- Usa `black` para formateo
- Ejecuta `ruff check` antes de hacer commit
- Agrega type hints
- Escribe docstrings descriptivos
- Los tests son obligatorios para new features

### Running Tests

```bash
pytest tests/ -v
```

## Preguntas

Abre una issue con la etiqueta `question` para hacer preguntas.

¡Gracias por contribuir! 🚀
