# CHANGELOG

Este documento registra los principales avances realizados durante el desarrollo de HospitalLearning.

---

## 2026-08-01

### Análisis y diseño

- Se finalizó la definición del Modelo Funcional.
- Se finalizó la definición del Modelo de Datos.
- Se definió la arquitectura para múltiples IPS.
- Se definió la entidad Institución (IPS).
- Se definió la entidad Usuario.
- Se definió la entidad Vinculación.
- Se definió la entidad Acción de Formación.
- Se creó la Biblioteca Documental Institucional.
- Se creó la Biblioteca Multimedia Institucional.
- Se creó el Banco Institucional de Preguntas.
- Se definió la entidad Evaluación.
- Se definió la entidad Intento de Evaluación.
- Se definió la entidad Certificado.
- Se definió la entidad Reporte.

### Arquitectura

- Se adoptó el principio de reutilización para documentos, recursos multimedia y preguntas.
- Se decidió permitir que un usuario pueda pertenecer a múltiples IPS.
- Se estableció el uso del término "Acción de Formación" en lugar de "Curso".
- Se alineó la plataforma con el concepto de formación continua del talento humano en salud.
---

## 2026-08-01

### Sprint 1 - Arquitectura e Instituciones

#### Arquitectura

- Se reorganizó la estructura de aplicaciones Django.
- Se crearon las aplicaciones: institutions, training, resources, assessments y reports.
- Se retiraron de la arquitectura activa las aplicaciones courses, lessons y quizzes.
- Se configuró el proyecto para múltiples IPS.

#### Instituciones

- Se creó el modelo Institution.
- Se configuró el administrador de Django para Instituciones.
- Se creó la primera migración.
- Se aplicó la migración a la base de datos.
- Se registró la primera institución desde Django Admin.

#### Configuración

- Se configuró el idioma del proyecto para Colombia (es-co).
- Se configuró la zona horaria America/Bogota.
- Se creó el primer superusuario.
- Se verificó el correcto funcionamiento del panel de administración.

#### Control de versiones

- Se realizó commit del Sprint 1.
- Se publicó el Sprint 1 en GitHub.
- Se creó la etiqueta Git: sprint-1.
---

## 2026-08-02

### Sprint 2 - Modelo de Usuario Personalizado

#### Usuarios

- Se creó el modelo `CustomUser` heredando de `AbstractUser`.
- Se agregaron los campos:
  - Tipo de documento.
  - Número de documento.
  - Profesión.
  - Teléfono.
- Se configuró `AUTH_USER_MODEL`.
- Se reconstruyó la base de datos para utilizar `CustomUser` desde el inicio del proyecto.
- Se registró `CustomUser` en Django Admin.
- Se verificó el acceso al panel de administración con el nuevo modelo de usuario.

#### Arquitectura

- Se confirmó que el usuario representa a una persona única.
- Se definió que las IPS y los tipos de vinculación serán administrados mediante un modelo independiente de Vinculación.