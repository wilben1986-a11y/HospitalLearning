# MODELO FUNCIONAL DEL SISTEMA

# Sistema de Gestión de Acciones de Formación Continua para el Talento Humano en Salud

---

# 1. OBJETIVO DEL SISTEMA

Desarrollar una plataforma web para gestionar las acciones de formación continua dirigidas al talento humano en salud, permitiendo planificar, publicar, desarrollar, evaluar y certificar actividades de formación virtual, generando evidencia para los procesos de calidad, habilitación y mejoramiento continuo de las Instituciones Prestadoras de Servicios de Salud (IPS).

---

# 2. ALCANCE

La plataforma estará diseñada para ser utilizada por Instituciones Prestadoras de Servicios de Salud (IPS).

La primera versión será implementada para una única institución, dejando preparada la arquitectura para soportar múltiples IPS en futuras versiones.

La plataforma será exclusivamente virtual.

No incluirá actividades presenciales como simulacros, entrenamientos o jornadas académicas.

No existirá registro público de usuarios.

Todos los usuarios serán creados por el administrador.

El acceso se realizará mediante usuario y contraseña.

---

# 3. TIPOS DE USUARIO

## Administrador

Será responsable de administrar la plataforma.

Podrá:

- Administrar usuarios.
- Crear acciones de formación.
- Editar acciones de formación.
- Publicar acciones de formación.
- Asignar acciones de formación.
- Administrar la biblioteca documental.
- Crear evaluaciones.
- Consultar indicadores.
- Generar reportes.
- Generar certificados.

---

## Profesional del Talento Humano en Salud

Podrá:

- Iniciar sesión.
- Consultar las acciones de formación asignadas.
- Consultar el catálogo institucional de acciones de formación.
- Desarrollar las acciones de formación.
- Presentar evaluaciones.
- Descargar certificados.
- Consultar su historial de formación.

---

# 4. ¿QUÉ ES UNA ACCIÓN DE FORMACIÓN CONTINUA?

Una acción de formación continua corresponde a una actividad virtual orientada al fortalecimiento, actualización y desarrollo de las competencias del talento humano en salud mediante contenidos educativos estructurados.

Para efectos de esta plataforma las acciones de formación serán:

- Capacitaciones.
- Inducciones.
- Reinducciones.

Cada acción de formación podrá contener contenido educativo, material de apoyo, documentos de referencia, evaluación y certificado.

---

# 5. BIBLIOTECA DOCUMENTAL

Cada acción de formación contará con un espacio destinado al almacenamiento y consulta de la documentación que fundamenta técnicamente su contenido.

La biblioteca documental permitirá asociar uno o varios documentos de referencia a cada acción de formación.

Entre ellos podrán incluirse:

- Leyes.
- Decretos.
- Resoluciones.
- Circulares.
- Guías de Práctica Clínica.
- Protocolos institucionales.
- Manuales.
- Procedimientos.
- Guías institucionales.
- Lineamientos del Ministerio de Salud y Protección Social.
- Documentos científicos.
- Otros documentos de referencia.

Cada documento almacenará como mínimo:

- Nombre.
- Tipo de documento.
- Entidad emisora.
- Año de publicación.
- Versión (cuando aplique).
- Archivo.
- Descripción u observaciones.

La biblioteca documental será reutilizable, permitiendo que un mismo documento pueda asociarse a múltiples acciones de formación sin necesidad de duplicarlo.

---

# 6. ASIGNACIÓN DE LAS ACCIONES DE FORMACIÓN

Cada acción de formación podrá dirigirse a una población objetivo.

Las opciones iniciales serán:

- Todos los servicios.
- Intrahospitalario.
- Consulta externa.
- Otros servicios.

Cuando el administrador seleccione "Otros servicios", podrá registrar el nombre del servicio correspondiente.

Cada profesional visualizará únicamente las acciones de formación que le hayan sido asignadas.

Adicionalmente podrá consultar el catálogo completo de acciones de formación disponibles en la institución.

---

# 7. EVALUACIONES

Cada acción de formación podrá tener una evaluación asociada.

Las evaluaciones estarán conformadas por preguntas definidas por el administrador.

El sistema registrará:

- Fecha de presentación.
- Puntaje obtenido.
- Estado (Aprobado o No aprobado).
- Número de intentos.

---

# 8. CERTIFICADOS

Una vez el participante cumpla los requisitos establecidos para la acción de formación, el sistema generará automáticamente el certificado correspondiente.

Cada certificado quedará almacenado en el historial del usuario.

---

# 9. INDICADORES

El sistema permitirá consultar indicadores como:

- Número de acciones de formación publicadas.
- Acciones de formación activas.
- Acciones pendientes.
- Acciones finalizadas.
- Acciones vencidas.
- Porcentaje de cumplimiento.
- Certificados emitidos.
- Resultados de las evaluaciones.

---

# 10. REPORTES

El sistema permitirá generar reportes por:

- Institución.
- Profesional.
- Acción de formación.
- Estado.
- Periodo.
- Población objetivo.

---

# 11. PRINCIPIOS DEL SISTEMA

El desarrollo del sistema estará basado en los siguientes principios:

- Utilizar terminología propia del sector salud colombiano.
- Adaptarse a diferentes IPS.
- Mantener una arquitectura escalable.
- Priorizar la simplicidad para el usuario.
- Centralizar la evidencia documental de las acciones de formación.
- Facilitar los procesos de calidad, auditoría y habilitación.
- Permitir el crecimiento del sistema sin afectar su funcionamiento.