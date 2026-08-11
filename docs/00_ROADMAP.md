# ROADMAP DEL PROYECTO

# HospitalLearning

Sistema de Gestión de Acciones de Formación Continua para el Talento Humano en Salud

---

## Convenciones de estado

- ✅ Completado: componente implementado y funcional.
- 🟡 En desarrollo: componente implementado parcialmente o pendiente de completar/validar.
- ⏳ Pendiente: componente aún no desarrollado.

---

# Estado general del proyecto

| Fase | Estado |
| --- | --- |
| 0. Configuración del proyecto Django | ✅ Completado |
| 1. Control de versiones (Git y GitHub) | ✅ Completado |
| 2. Estructura inicial del proyecto | ✅ Completado |
| 3. Visión del proyecto | ✅ Completado |
| 4. Modelo funcional | ✅ Completado |
| 5. Modelo de datos | 🟡 En desarrollo |
| 6. Autenticación | ✅ Completado |
| 7. Gestión de usuarios e instituciones | 🟡 En desarrollo |
| 8. Acciones de formación | ✅ Completado |
| 9. Asignación y seguimiento de capacitaciones | ✅ Completado |
| 10. Ejecución de contenido interactivo | ✅ Completado |
| 11. Evaluaciones y resultados | 🟡 En desarrollo |
| 12. Certificados | ✅ Completado |
| 13. Biblioteca documental | ⏳ Pendiente |
| 14. Biblioteca multimedia | ⏳ Pendiente |
| 15. Banco institucional de preguntas | ⏳ Pendiente |
| 16. Dashboard e indicadores | 🟡 En desarrollo |
| 17. Reportes | ⏳ Pendiente |
| 18. Despliegue en producción | ⏳ Pendiente |

---

# 1. Infraestructura del proyecto

## Estado: ✅ COMPLETADO

Se encuentra implementado:

- Proyecto Django.
- Entorno virtual de Python.
- Base de datos de desarrollo.
- Estructura modular mediante aplicaciones Django.
- Control de versiones mediante Git.
- Repositorio remoto en GitHub.
- Servidor local de desarrollo.
- Organización de templates y archivos del proyecto.

---

# 2. Instituciones, servicios y usuarios

## Estado: 🟡 EN DESARROLLO

Actualmente existen los modelos:

- Institution.
- Service.
- CustomUser.
- InstitutionalLink.

La arquitectura permite relacionar usuarios con instituciones y gestionar su vinculación institucional.

## Pendiente

- Completar pruebas funcionales de administración de servicios.
- Revisar permisos y roles.
- Validar completamente el comportamiento multi-IPS.
- Completar interfaces de administración cuando sea necesario.

---

# 3. Acciones de formación continua

## Estado: ✅ COMPLETADO EN SU NÚCLEO FUNCIONAL

Actualmente existen:

- ActionType.
- TrainingAction.
- TrainingAssignment.
- TrainingResult.

El sistema permite:

- Crear tipos de acción.
- Crear y parametrizar acciones de formación.
- Definir versión.
- Definir estado.
- Configurar obligatoriedad.
- Configurar pretest.
- Configurar evaluación final.
- Configurar requisito de revisión completa del contenido.
- Configurar puntaje mínimo.
- Configurar número máximo de intentos.
- Configurar generación de certificado.
- Configurar emisión automática del certificado.
- Asignar capacitaciones a participantes.

---

# 4. Contenido interactivo de capacitación

## Estado: ✅ COMPLETADO EN SU NÚCLEO FUNCIONAL

HospitalLearning permite utilizar archivos HTML como contenido principal de una acción de formación.

Se encuentra probado el flujo:

Pretest → Contenido por módulos → Postest → Finalización

El sistema permite:

- Abrir contenido HTML dentro de HospitalLearning.
- Registrar el pretest.
- Bloquear inicialmente el contenido cuando corresponde.
- Registrar módulos completados.
- Registrar el módulo actual.
- Registrar la etapa actual.
- Salir de una capacitación sin perder el progreso.
- Reanudar desde el punto registrado.
- Bloquear el postest hasta revisar todos los módulos requeridos.
- Registrar resultados del postest.
- Finalizar la capacitación.

Existe además un prompt maestro documentado para facilitar la creación de nuevos contenidos compatibles con HospitalLearning.

---

# 5. Evaluaciones y resultados

## Estado: 🟡 EN DESARROLLO

Actualmente HospitalLearning recibe y almacena los resultados generados desde el contenido interactivo de la capacitación.

El sistema permite registrar:

- Resultado inicial del pretest.
- Resultado del postest.
- Mejor resultado obtenido.
- Mejora entre pretest y postest.
- Número de intentos.
- Estado de aprobación.
- Fecha de finalización.

## Pendiente

El modelo de datos contempla una arquitectura más amplia que todavía no está implementada completamente:

- Evaluación como entidad independiente.
- Banco institucional de preguntas.
- Opciones de respuesta.
- Intentos individuales de evaluación.
- Reutilización de preguntas entre capacitaciones.

Antes de implementar esta arquitectura deberá definirse cómo coexistirá con las evaluaciones incluidas dentro de los archivos HTML interactivos.

---

# 6. Seguimiento del participante

## Estado: ✅ COMPLETADO EN SU NÚCLEO FUNCIONAL

El participante puede consultar:

- Capacitaciones pendientes.
- Capacitaciones en progreso.
- Capacitaciones realizadas.
- Estado de aprobación.
- Resultado del pretest.
- Mejor resultado del postest.
- Mejora obtenida.
- Intentos utilizados.
- Fecha de finalización.

El sistema conserva el progreso cuando el participante abandona una capacitación y permite retomarla posteriormente.

---

# 7. Certificados

## Estado: ✅ COMPLETADO EN SU NÚCLEO FUNCIONAL

Actualmente existe el modelo:

- Certificate.

El sistema permite:

- Generación automática del certificado cuando corresponde.
- Relación del certificado con la asignación del participante.
- Código único de verificación.
- Fecha de emisión.
- Estado activo.
- Visualización del certificado desde HospitalLearning.
- Impresión desde navegador.
- Generación de certificado en PDF.
- Descarga directa del PDF.
- Restricción de acceso al certificado al usuario correspondiente.

## Mejoras futuras

- Logo institucional parametrizable.
- Firma institucional.
- Cargo del responsable.
- Personalización visual por IPS.
- Verificación pública mediante código.
- Manejo de vigencia, vencimiento o revocación cuando aplique.

---

# 8. Biblioteca documental

## Estado: ⏳ PENDIENTE

El componente está definido en el modelo de datos, pero todavía no se encuentra implementado como modelo funcional de Django.

Deberá permitir administrar documentos institucionales como:

- Protocolos.
- Guías de práctica clínica.
- Procedimientos.
- Manuales.
- Instructivos.
- Formatos.
- Resoluciones.
- Otros documentos de referencia.

Los documentos podrán reutilizarse en diferentes acciones de formación.

---

# 9. Biblioteca multimedia

## Estado: ⏳ PENDIENTE

El componente está definido conceptualmente pero aún no se encuentra implementado completamente.

Deberá permitir administrar recursos como:

- Videos.
- Presentaciones.
- Audios.
- Imágenes.
- Infografías.
- Enlaces.
- Otros recursos multimedia.

---

# 10. Banco institucional de preguntas

## Estado: ⏳ PENDIENTE

Está definido en el modelo de datos, pero todavía no existe como modelo funcional de Django.

Deberá permitir:

- Registrar preguntas.
- Registrar opciones de respuesta.
- Clasificar preguntas.
- Reutilizar preguntas.
- Asociarlas a evaluaciones.
- Mantener trazabilidad institucional.

---

# 11. Dashboard e indicadores

## Estado: 🟡 EN DESARROLLO

Existe estructura inicial para el dashboard.

El siguiente desarrollo deberá aprovechar los datos que HospitalLearning ya genera para presentar indicadores institucionales.

Indicadores iniciales propuestos:

- Usuarios registrados.
- Usuarios activos.
- Capacitaciones publicadas.
- Capacitaciones asignadas.
- Capacitaciones pendientes.
- Capacitaciones en progreso.
- Capacitaciones completadas.
- Capacitaciones aprobadas.
- Capacitaciones no aprobadas.
- Porcentaje de cumplimiento.
- Resultados de evaluaciones.
- Certificados emitidos.

Posteriormente podrán incorporarse filtros por:

- Institución.
- Acción de formación.
- Tipo de acción.
- Profesión.
- Servicio.
- Estado.
- Período.

---

# 12. Reportes

## Estado: ⏳ PENDIENTE

La aplicación `reports` se encuentra creada, pero el componente funcional aún debe desarrollarse.

Los reportes deberán generarse a partir de la información existente en HospitalLearning.

Reportes previstos:

- Cumplimiento de capacitaciones.
- Capacitaciones pendientes.
- Historial de formación por usuario.
- Resultados de evaluaciones.
- Certificados emitidos.
- Cumplimiento por profesión.
- Cumplimiento por servicio.
- Cumplimiento por institución.
- Seguimiento por acción de formación.

## Exportación prevista

- Excel.
- PDF.

---

# 13. Despliegue en producción

## Estado: ⏳ PENDIENTE

Actualmente HospitalLearning funciona en entorno local de desarrollo mediante Django.

Antes del despliegue deberán revisarse:

- Configuración de producción.
- Base de datos.
- Seguridad.
- Variables de entorno.
- Archivos estáticos.
- Archivos cargados por usuarios.
- Copias de seguridad.
- Servidor WSGI o ASGI.
- Dominio.
- HTTPS.
- Estrategia de despliegue.
- Administración de múltiples IPS.

---

# Documentación del proyecto

| Documento | Estado |
| --- | --- |
| 00 roadmap.md | 🟡 Requiere actualización periódica |
| 01_vision_del_proyecto.md | ✅ Elaborado |
| 02_modelo_funcional.md | ✅ Elaborado |
| 03_modelo_de_datos.md | 🟡 Requiere depuración y actualización |
| 99_ideas_futuras.md | ✅ Disponible |
| PROMPT_MAESTRO_HOSPITALLEARNING.md | ✅ Disponible |

---

# Observación sobre el modelo de datos

El documento `03_modelo_de_datos.md` contiene definiciones correspondientes a diferentes momentos de evolución del proyecto.

Antes de considerarlo definitivo se deberá:

- Eliminar definiciones duplicadas.
- Actualizar las entidades según los modelos Django realmente implementados.
- Incorporar TrainingAssignment.
- Incorporar TrainingResult.
- Actualizar Certificate.
- Definir la relación entre evaluaciones HTML y evaluaciones nativas de HospitalLearning.
- Revisar el alcance multi-IPS.
- Mantener la trazabilidad de las decisiones arquitectónicas.

---

# Objetivo de la versión 1.0

Desarrollar una plataforma web para gestionar acciones de formación continua dirigidas al talento humano en salud, incluyendo:

- Instituciones y usuarios.
- Acciones de formación.
- Asignación de participantes.
- Contenido educativo interactivo.
- Seguimiento del progreso.
- Evaluación del aprendizaje.
- Certificación.
- Bibliotecas institucionales.
- Dashboard.
- Indicadores.
- Reportes.

La arquitectura deberá permitir el uso de HospitalLearning por múltiples Instituciones Prestadoras de Servicios de Salud.

---

# PRÓXIMO OBJETIVO

## Dashboard institucional e indicadores

Construir el primer dashboard funcional utilizando los datos que HospitalLearning ya registra.

El dashboard deberá permitir inicialmente visualizar:

1. Total de participantes.
2. Capacitaciones asignadas.
3. Capacitaciones pendientes.
4. Capacitaciones en progreso.
5. Capacitaciones completadas.
6. Capacitaciones aprobadas.
7. Capacitaciones no aprobadas.
8. Porcentaje de cumplimiento.
9. Resultados de evaluación.
10. Certificados emitidos.

Una vez construido y validado el dashboard inicial, se continuará con los reportes institucionales.