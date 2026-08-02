# MODELO DE DATOS

# HospitalLearning

Sistema de Gestión de Acciones de Formación Continua para el Talento Humano en Salud

---

# Objetivo

Definir las entidades principales del sistema, la información que almacenará cada una y la relación existente entre ellas.

Este documento servirá como base para el desarrollo de los modelos de Django y de la base de datos.

---

# Entidades principales

La primera versión del sistema estará compuesta por las siguientes entidades:

1. Institución (IPS)

2. Usuario

3. Acción de formación

4. Biblioteca documental

5. Material multimedia

6. Evaluación

7. Pregunta

8. Intento de evaluación

9. Certificado

10. Reporte

---

Institución (IPS)
│
├── Usuarios
│
├── Vinculaciones
│
├── Biblioteca documental
│
├── Biblioteca multimedia
│
├── Acciones de formación
│      │
│      ├── utiliza documentos
│      ├── utiliza material multimedia
│      ├── Evaluaciones
│      │          │
│      │          ├── Preguntas
│      │          └── Intentos
│      │
│      └── Certificados
│
└── Reportes
---

# Entidad: Institución (IPS)

Representa una Institución Prestadora de Servicios de Salud que utiliza la plataforma.

## Información que almacenará

- Nombre de la institución.
- NIT.
- Código de habilitación (opcional).
- Dirección.
- Ciudad.
- Departamento.
- Teléfono.
- Correo electrónico institucional.
- Logo institucional.
- Estado (Activa / Inactiva).

## Relaciones

Una institución podrá tener:

- Muchos usuarios.
- Muchas acciones de formación.
- Muchos certificados.
- Muchos reportes.

En la versión 1.0 el sistema funcionará con una única institución, pero la arquitectura quedará preparada para soportar múltiples IPS en versiones futuras.
---

# Entidad: Usuario

Representa a una persona que puede acceder a la plataforma y participar en las acciones de formación continua.

## Información personal

- Tipo de documento.
- Número de documento.
- Nombres.
- Apellidos.
- Correo electrónico.
- Teléfono (opcional).

## Información profesional

- Profesión.

Si la profesión no se encuentra en el listado, podrá registrarse como "Otra" y especificar el nombre.

## Información del sistema

- Nombre de usuario.
- Contraseña.
- Estado (Activo / Inactivo).

## Relaciones

Un usuario podrá:

- Estar vinculado a una o varias IPS.
- Participar en múltiples acciones de formación.
- Presentar múltiples evaluaciones.
- Obtener múltiples certificados.

El historial de formación pertenecerá al usuario y se conservará aunque cambie de institución.
---

# Entidad: Vinculación

Representa la relación entre un usuario y una Institución Prestadora de Servicios de Salud (IPS).

Cada usuario podrá tener una o varias vinculaciones, una por cada institución en la que participe.

## Información que almacenará

- Institución (IPS).
- Usuario.
- Tipo de servicio.
- Nombre del servicio (cuando el tipo de servicio sea "Otros servicios").
- Rol dentro de la plataforma.
- Estado de la vinculación (Activa / Inactiva).
- Fecha de inicio de la vinculación.
- Fecha de finalización (opcional).

## Tipo de servicio

- Intrahospitalario
- Consulta externa
- Todos los servicios
- Otros servicios

Si se selecciona "Otros servicios", se podrá registrar el nombre correspondiente.

## Roles disponibles

- Administrador
- Profesional del Talento Humano en Salud

## Relaciones

Cada vinculación pertenece a:

- Un usuario.
- Una institución.

A través de esta vinculación se asignarán las acciones de formación correspondientes.
---

# Entidad: Acción de Formación

Representa una actividad virtual de formación continua dirigida al talento humano en salud.

Una acción de formación podrá ser asignada a uno o varios usuarios y conservará un único contenido, una única evaluación y un único certificado.

## Información general

- Código.
- Nombre.
- Tipo de acción de formación.
- Descripción.
- Objetivo de aprendizaje.
- Institución (IPS) responsable.
- Estado (Borrador, Publicada, Archivada).
- Fecha de creación.
- Fecha de actualización.

## Tipos de acción de formación

- Capacitación.
- Inducción.
- Reinducción.

## Público objetivo

La acción de formación podrá dirigirse a:

- Una o varias profesiones.
- Uno o varios tipos de servicio.
- Todos los colaboradores de la institución.

## Recursos asociados

Cada acción de formación podrá asociar recursos existentes de la institución:

- Documentos de la biblioteca documental institucional.
- Recursos de la biblioteca multimedia institucional.
- Una evaluación.
- Un certificado.

## Relaciones

Una acción de formación:

- Pertenece a una institución.
- Puede ser asignada a múltiples usuarios.
- Puede tener múltiples documentos.
- Puede tener múltiples recursos multimedia.
- Tendrá una evaluación.
- Permitirá generar certificados.
---

# Entidad: Biblioteca Documental

Representa el repositorio institucional de documentos que pueden utilizarse como soporte de una o varias acciones de formación.

Los documentos se almacenan una única vez y pueden asociarse a diferentes acciones de formación.

## Información general

- Código.
- Título del documento.
- Tipo de documento.
- Descripción.
- Versión.
- Fecha de publicación.
- Estado (Vigente / Obsoleto).
- Archivo.
- Institución (IPS).

## Tipos de documento

- Protocolo.
- Guía de práctica clínica.
- Procedimiento.
- Manual.
- Instructivo.
- Formato.
- Resolución interna.
- Otro.

Si se selecciona "Otro", podrá registrarse el tipo correspondiente.

## Relaciones

Un documento:

- Pertenece a una institución.
- Puede asociarse a una o varias acciones de formación.
---

# Entidad: Biblioteca Multimedia

Representa el repositorio institucional de recursos multimedia que pueden utilizarse en una o varias acciones de formación.

Los recursos se almacenan una única vez y pueden asociarse a diferentes acciones de formación.

## Información general

- Código.
- Título.
- Tipo de recurso.
- Descripción.
- Archivo o enlace.
- Duración (opcional).
- Estado (Activo / Inactivo).
- Institución (IPS).

## Tipos de recurso

- Video.
- Presentación.
- Audio.
- Imagen.
- Infografía.
- Enlace externo.
- Otro.

Si se selecciona "Otro", podrá registrarse el tipo correspondiente.

## Relaciones

Un recurso multimedia:

- Pertenece a una institución.
- Puede asociarse a una o varias acciones de formación.
---

# Entidad: Evaluación

Representa el instrumento utilizado para verificar el aprendizaje adquirido en una acción de formación.

Cada acción de formación tendrá una única evaluación, compuesta por una o varias preguntas.

## Información general

- Título.
- Descripción.
- Acción de formación.
- Puntaje mínimo para aprobar.
- Número máximo de intentos permitidos (un valor de 0 indicará intentos ilimitados).
- Tiempo máximo para responder (opcional).
- Estado (Activa / Inactiva).
## Reglas de aprobación

Cada evaluación definirá:

- Puntaje mínimo para aprobar.
- Número máximo de intentos permitidos.
- Si el usuario aprueba, podrá obtener el certificado de la acción de formación, siempre que se cumplan los demás requisitos establecidos.
## Relaciones

Una evaluación:

- Pertenece a una acción de formación.
- Contiene múltiples preguntas.
- Puede ser presentada por múltiples usuarios mediante intentos de evaluación.
---

# Entidad: Banco Institucional de Preguntas

Representa el repositorio institucional de preguntas que pueden utilizarse en una o varias evaluaciones.

Cada pregunta se registra una única vez y podrá reutilizarse en diferentes acciones de formación.

## Información general

- Código.
- Enunciado de la pregunta.
- Tipo de pregunta.
- Nivel de dificultad (opcional).
- Explicación de la respuesta (opcional).
- Estado (Activa / Inactiva).
- Institución (IPS).

## Tipos de pregunta

- Selección única.
- Selección múltiple.
- Verdadero / Falso.

## Opciones de respuesta

Cada pregunta podrá tener dos o más opciones de respuesta.

Cada opción indicará si es correcta o incorrecta.

## Relaciones

Una pregunta:

- Pertenece a una institución.
- Puede utilizarse en múltiples evaluaciones.
---

# Entidad: Intento de Evaluación

Representa cada oportunidad en la que un usuario presenta una evaluación.

Cada intento conserva el resultado obtenido y permite llevar el historial de las evaluaciones realizadas.

## Información general

- Usuario.
- Evaluación.
- Número de intento.
- Fecha y hora de inicio.
- Fecha y hora de finalización.
- Puntaje obtenido.
- Porcentaje obtenido.
- Resultado (Aprobado / No aprobado).

## Relaciones

Un intento:

- Pertenece a un usuario.
- Corresponde a una evaluación.

Un usuario podrá tener múltiples intentos sobre una misma evaluación, de acuerdo con las reglas definidas para la acción de formación.
---

# Entidad: Certificado

Representa la constancia de aprobación de una acción de formación por parte de un usuario.

El certificado se generará automáticamente cuando el usuario cumpla los requisitos establecidos para la acción de formación.

## Información general

- Código único del certificado.
- Usuario.
- Acción de formación.
- Fecha de aprobación.
- Fecha de emisión.
- Fecha de vencimiento (opcional).
- Estado (Vigente / Vencido / Revocado).
- Código de verificación.
- Archivo PDF.

## Requisitos para generar el certificado

El certificado podrá emitirse cuando:

- El usuario haya aprobado la evaluación.
- Se hayan completado todos los recursos obligatorios de la acción de formación.
- Se cumplan las demás reglas definidas por la institución.

## Relaciones

Un certificado:

- Pertenece a un usuario.
- Corresponde a una acción de formación.
- Puede verificarse mediante un código único.
---

# Entidad: Reporte

Representa la información consolidada que permite realizar seguimiento al cumplimiento de las acciones de formación continua y apoyar los procesos de gestión, auditoría y mejoramiento institucional.

Los reportes se generan a partir de la información registrada en la plataforma y no almacenan datos independientes.

## Información disponible

La plataforma permitirá generar reportes como:

- Usuarios registrados.
- Usuarios activos e inactivos.
- Acciones de formación publicadas.
- Acciones de formación por tipo.
- Acciones de formación por institución.
- Acciones de formación asignadas.
- Acciones de formación completadas.
- Acciones de formación pendientes.
- Resultados de evaluaciones.
- Certificados emitidos.
- Certificados vigentes.
- Certificados vencidos.
- Historial de formación por usuario.
- Cumplimiento por profesión.
- Cumplimiento por tipo de servicio.
- Cumplimiento por institución.

## Exportación

Los reportes podrán exportarse en formatos como:

- PDF.
- Excel.

## Observación

Los reportes se construirán utilizando la información existente en las demás entidades del sistema, por lo que no requerirán almacenamiento propio.

---

# Entidad: Tipo de Acción

Representa una categoría institucional utilizada para clasificar las acciones de formación continua y definir sus reglas generales de cumplimiento.

## Información general

- Institución.
- Nombre.
- Código.
- Objetivo.
- Descripción (opcional).
- Estado activo o inactivo.
- Requiere certificado.
- Tiene vigencia.
- Requiere renovación periódica.
- Período de renovación, cuando aplique.
- Una nueva versión obliga a repetir la formación.

## Relaciones

Un Tipo de Acción:

- Pertenece a una única institución.
- Puede estar asociado a múltiples Acciones de Formación.

## Restricciones

- El nombre debe ser único dentro de la institución.
- El código debe ser único dentro de la institución.
- El período de renovación será obligatorio cuando el tipo requiera renovación periódica.
- No podrá eliminarse físicamente cuando tenga Acciones de Formación asociadas.
- Un Tipo de Acción inactivo no podrá utilizarse en nuevas Acciones de Formación.

## Reglas funcionales

- El Tipo de Acción define la configuración por defecto de las Acciones de Formación asociadas.
- Una Acción de Formación podrá personalizar estas reglas cuando la institución lo autorice.
- Una Acción de Formación solo podrá cambiar de Tipo mientras permanezca en estado Borrador.