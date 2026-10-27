# Presentación LiceoMap: 11 minutos

Las intervenciones se pueden repartir entre integrantes; los bloques siguientes son
turnos sugeridos, no una atribución de trabajo o responsabilidades. Antes de empezar,
reemplazar cada afirmación sobre pruebas por el resultado real de la sesión de ensayo.

| Diapositiva | Tiempo | Texto breve en pantalla | Guion oral sugerido |
|---|---|---|---|
| 1. LiceoMap | 0:00–0:40 | Orientación y comunicación escolar en una aplicación | «LiceoMap reúne el mapa del liceo, horarios y comunicados para facilitar la jornada escolar». Presentar al equipo sin adjudicar funciones no confirmadas. |
| 2. El problema | 0:40–1:30 | Encontrar espacios · Consultar el horario · Recibir información | Explicar situaciones cotidianas: buscar una sala, revisar la próxima clase y saber si hay un aviso vigente. No inventar estadísticas ni encuestas. |
| 3. Nuestra solución | 1:30–2:20 | Android + mapa local + información centralizada | Mostrar las pantallas existentes. Aclarar que el mapa puede abrirse sin conexión y que los datos de sesión y comunicados necesitan el servidor local. |
| 4. Cómo se conecta | 2:20–3:20 | Web → FastAPI → MariaDB ← FastAPI ← Android | Explicar que web y Android consultan la misma fuente. La API valida las credenciales y permisos; el teléfono no se conecta directamente a MariaDB. |
| 5. Qué implementamos | 3:20–4:20 | Kotlin/Compose · SVG y respaldo PNG · FastAPI · MariaDB | Resumir navegación, acceso, horarios, mapa y panel de comunicados. Distinguir datos demo de datos reales y avisar qué flujos se probaron hoy. |
| 6. Demostración guiada | 4:20–7:20 | Entrar → horario → mapa → publicar → actualizar | Ejecutar el recorrido de tres minutos de `DEMO_MINIMA.md`. Una persona controla Android y otra la web. Mostrar la publicación y su retiro, si la prueba real está autorizada y disponible. |
| 7. Validación y límites | 7:20–8:40 | Lo comprobado · Lo pendiente · Lo que falló | Mostrar resultados reales de compilación, recursos y ensayo. Decir explícitamente si el mapa solo se verificó en el notebook o si no se completó la sincronización en el teléfono. |
| 8. Próximos pasos | 8:40–10:00 | Horarios individuales · Salas confirmadas · Accesibilidad | Explicar que grupos, electivos, permisos adicionales y unificación visual completa son tareas posteriores. No presentar rutas automáticas, GPS interior o notificaciones push como funciones terminadas. |
| 9. Cierre | 10:00–11:00 | Una base común para orientar e informar | Recapitular el recorrido realmente mostrado, el aprendizaje de integración y las limitaciones actuales. Dejar un minuto de margen para preguntas o pequeños retrasos. |

## Plan de emergencia

- **Mapa:** usar el respaldo PNG local y mostrar zoom en el notebook. Aclarar si
  el visor Android todavía falla; no atribuir al teléfono una prueba hecha en PC.
- **USB/red:** reconectar, aceptar la depuración y ejecutar `demo_local.py usb`.
  Si no vuelve, mostrar capturas del ensayo con su contexto y distinguirlas de una prueba en vivo.
- **MariaDB/API:** mostrar `/health` y el error de conexión si corresponde. Cambiar
  al modo demostración para explicar la interfaz. No simular una publicación real.
- **Tiempo:** priorizar mapa y un solo comunicado; omitir edición y comprobaciones
  secundarias durante la exposición, después de haberlas ensayado si fue posible.

## Preparación y capturas

- Cargar notebook y teléfono; llevar cable USB de datos y dejar la pantalla activa.
- Ejecutar `check-db`, iniciar API/web, ejecutar `check` y `usb`; abrir las pantallas
  necesarias antes de entrar. Cerrar aplicaciones pesadas del notebook.
- Confirmar en privado las cuentas de estudiante y administrador, y el curso de destino.
- Tomar capturas reales de: Inicio con curso, Horarios, Mapa ampliado, formulario de
  comunicado sin credenciales y Anuncios con el mismo título publicado. Ocultar RUT,
  correo, tokens, contraseñas y cualquier dato de personas no autorizado para mostrar.
- Guardar una captura de la retirada y de un estado de error, si se verificaron.
- Llevar la APK final y el PNG de respaldo. Registrar qué ensayo pasó y cuál quedó pendiente.
- No modificar la base, las credenciales ni la configuración durante la presentación
  para resolver un fallo improvisadamente.
