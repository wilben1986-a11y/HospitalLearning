ROADMAP DEL PROYECTO

HospitalLearning

Sistema de Gestión de Acciones de Formación Continua para el Talento Humano en Salud

Convenciones de estado

✅ Completado: componente implementado, validado y funcional en su alcance actual.

🟡 En desarrollo: componente funcional en parte, pero con funcionalidades relevantes pendientes.

⏳ Pendiente: componente aún no desarrollado.

Estado general del proyecto

Fase

Estado

0. Configuración del proyecto Django

✅ Completado

1. Control de versiones (Git y GitHub)

✅ Completado

2. Estructura inicial del proyecto

✅ Completado

3. Visión y modelo funcional

✅ Completado

4. Modelo de datos

🟡 En desarrollo

5. Autenticación

✅ Completado

6. Gestión de usuarios e instituciones

🟡 En desarrollo

7. Acciones de formación

✅ Completado en su núcleo funcional

8. Asignación y seguimiento

✅ Completado en su núcleo funcional

9. Contenido interactivo

✅ Completado en su núcleo funcional

10. Evaluaciones y resultados

🟡 En desarrollo

11. Certificados

✅ Completado en su núcleo funcional

12. Biblioteca documental

⏳ Pendiente

13. Biblioteca multimedia

⏳ Pendiente

14. Banco institucional de preguntas

⏳ Pendiente

15. Dashboard e indicadores

✅ Completado en su alcance actual

16. Reportes institucionales

✅ Completado en su núcleo funcional

17. Navegación e interfaces por rol

✅ Completado en su núcleo funcional

18. Validación integral multi-IPS

🟡 En desarrollo

19. Despliegue en producción

⏳ Pendiente

1. Infraestructura del proyecto

Estado: ✅ COMPLETADO

Implementado:

Proyecto Django y entorno virtual de Python.

Base de datos de desarrollo SQLite.

Arquitectura modular mediante aplicaciones Django.

Git y repositorio remoto en GitHub.

Servidor local de desarrollo.

Templates y archivos del proyecto.

Archivos cargados por usuarios.

Autenticación integrada mediante Django.

2. Instituciones, servicios y usuarios

Estado: 🟡 EN DESARROLLO

Modelos existentes:

Institution.

Service.

CustomUser.

InstitutionalLink.

Implementado y validado:

Vinculación de usuarios con instituciones.

Vinculaciones activas e inactivas.

Asociación de usuarios con servicios.

Uso de la institución activa para limitar Dashboard, reportes e interfaces administrativas.

Interfaz institucional de usuarios.

Búsqueda, filtro por profesión y filtro por estado de vinculación.

Visualización de servicios asociados.

Página “Mi perfil” para participantes.

Visualización de la vinculación institucional activa.

Pendiente

Completar pruebas de administración de servicios.

Consolidar permisos y roles más allá de staff/superusuario y participante.

Validar escenarios con múltiples IPS.

Definir selección/cambio de IPS cuando existan varias vinculaciones activas.

Revisar permisos granulares por institución.

Completar operaciones internas que todavía dependan de Django Admin.

3. Acciones de formación continua

Estado: ✅ COMPLETADO EN SU NÚCLEO FUNCIONAL

Existen ActionType, TrainingAction, TrainingAssignment y TrainingResult.

El sistema permite crear y parametrizar acciones de formación; definir versión, estado y obligatoriedad; configurar pretest, evaluación final, revisión completa del contenido, puntaje mínimo, intentos, certificados y emisión automática; y asignar capacitaciones a participantes.

La interfaz administrativa propia permite consultar, buscar y filtrar capacitaciones por tipo, estado y condición activa/inactiva. Django Admin se conserva como herramienta técnica de respaldo.

4. Contenido interactivo de capacitación

Estado: ✅ COMPLETADO EN SU NÚCLEO FUNCIONAL

Flujo probado:

Pretest → Contenido por módulos → Postest → Finalización

Permite abrir contenido HTML dentro de HospitalLearning, registrar pretest, bloquear contenido cuando corresponde, registrar módulos y etapa actual, conservar y reanudar progreso, bloquear postest hasta completar los módulos requeridos, registrar postest y finalizar la capacitación.

Existe un prompt maestro para crear nuevos contenidos compatibles con HospitalLearning.

5. Evaluaciones y resultados

Estado: 🟡 EN DESARROLLO

Actualmente se registran:

Pretest.

Postest.

Mejor resultado.

Mejora.

Número de intentos.

Estado de aprobación.

Fecha de finalización.

Estos datos alimentan seguimiento individual, Dashboard personal, Dashboard institucional, indicadores y reportes. La interfaz administrativa permite consultar resultados por participante y capacitación y filtrar por aprobación.

La ausencia de pretest o postest no se interpreta como calificación cero.

Pendiente

Evaluación como entidad independiente.

Banco institucional de preguntas.

Opciones de respuesta.

Intentos individuales de evaluación.

Reutilización de preguntas.

Evaluaciones nativas dentro de HospitalLearning.

Antes de implementarlo deberá definirse cómo coexistirá con las evaluaciones incluidas en los archivos HTML interactivos.

6. Seguimiento del participante

Estado: ✅ COMPLETADO EN SU NÚCLEO FUNCIONAL

El participante consulta capacitaciones pendientes, en progreso y realizadas; aprobación; pretest; mejor postest; mejora; intentos y fecha de finalización. El progreso se conserva y puede reanudarse.

El Dashboard personal muestra asignadas, pendientes, en progreso, realizadas, aprobadas, no aprobadas, promedios pretest/postest, mejora, certificados, próximas capacitaciones y últimas realizadas.

Navegación propia:

Mi inicio.

Mis capacitaciones.

Mis certificados.

Mi perfil.

7. Certificados

Estado: ✅ COMPLETADO EN SU NÚCLEO FUNCIONAL

Existe Certificate y se encuentra implementada la generación automática cuando corresponde, código único de verificación, fecha de emisión, estado activo, visualización, impresión, PDF, descarga, restricción de acceso, certificados recientes, página “Mis certificados” e interfaz administrativa institucional con búsqueda y filtro por estado.

Mejoras futuras

Logo y firma institucional parametrizables.

Cargo del responsable.

Personalización visual por IPS.

Verificación pública mediante código.

Vigencia, vencimiento o revocación cuando aplique.

8. Biblioteca documental

Estado: ⏳ PENDIENTE

Deberá administrar y reutilizar protocolos, guías de práctica clínica, procedimientos, manuales, instructivos, formatos, resoluciones y otros documentos de referencia, respetando la institución correspondiente.

Este componente forma parte del próximo bloque de desarrollo.

9. Biblioteca multimedia

Estado: ⏳ PENDIENTE

Deberá administrar y reutilizar videos, presentaciones, audios, imágenes, infografías, enlaces y otros recursos multimedia asociados a acciones de formación.

Este componente forma parte del próximo bloque de desarrollo.

10. Banco institucional de preguntas

Estado: ⏳ PENDIENTE

Deberá permitir registrar preguntas y opciones, clasificarlas, reutilizarlas, asociarlas a evaluaciones y mantener trazabilidad institucional.

Se desarrollará después de consolidar las bibliotecas y definir la convivencia entre evaluaciones nativas y evaluaciones HTML.

11. Dashboard e indicadores

Estado: ✅ COMPLETADO EN SU ALCANCE ACTUAL

HospitalLearning dispone de Dashboard institucional y Dashboard personal según el perfil autenticado.

11.1 Dashboard institucional

Utiliza la institución activa del administrador y restringe los datos a la IPS correspondiente.

Incluye indicadores de participantes, asignaciones, completadas, cumplimiento, pendientes, en progreso, aprobadas, no aprobadas, promedios pretest/postest, mejora y certificados.

Dispone de resumen por acción de formación y resumen individual de participantes.

Filtros institucionales

Implementados y validados en el alcance actual:

Acción de formación.

Tipo de acción.

Profesión.

Estado.

Período.

El filtro por servicio no se incorporó al Dashboard por decisión de alcance actual.

La institución continúa determinándose por la vinculación institucional activa. La selección manual de IPS se evaluará durante la validación multi-IPS.

11.2 Dashboard personal

Estado: ✅ COMPLETADO EN SU ALCANCE ACTUAL

Permite consultar indicadores personales, próximas capacitaciones, últimas capacitaciones, certificados recientes y acceder a las secciones personales.

12. Reportes institucionales

Estado: ✅ COMPLETADO EN SU NÚCLEO FUNCIONAL

La aplicación reports está implementada y funcional. Dispone de página propia integrada a HospitalLearning, siete bloques de reportes institucionales, filtros y exportación.

Exportación

Excel.

PDF.

Los reportes utilizan la información de HospitalLearning y respetan el contexto institucional del administrador.

Mejoras futuras

Refinar formatos Excel/PDF.

Incorporar nuevos reportes según necesidades institucionales.

Validar escenarios multi-IPS.

Incorporar nuevas dimensiones cuando el modelo lo requiera.

13. Navegación e interfaces por rol

Estado: ✅ COMPLETADO EN SU NÚCLEO FUNCIONAL

Administrador

Dashboard institucional.

Capacitaciones.

Usuarios.

Evaluaciones.

Certificados.

Reportes institucionales.

Configuración.

Las secciones principales utilizan páginas propias de HospitalLearning y conservan el menú lateral. Django Admin permanece como respaldo técnico.

Participante

Mi inicio.

Mis capacitaciones.

Mis certificados.

Mi perfil.

Las páginas conservan la navegación del participante.

14. Configuración institucional

Estado: 🟡 EN DESARROLLO

Existe una página propia que permite consultar institución activa, tipos de acción, servicios, estados y requisitos de certificado.

Pendiente

Definir parámetros editables.

Formularios internos.

Permisos de modificación.

Personalización institucional.

Validación multi-IPS.

15. Validación multi-IPS

Estado: 🟡 EN DESARROLLO

Actualmente los usuarios pueden tener vinculaciones institucionales; las acciones pertenecen a una institución; y Dashboard, reportes e interfaces administrativas usan el contexto de la institución activa.

Pendiente

Probar usuarios vinculados a varias IPS.

Definir comportamiento con varias vinculaciones activas.

Implementar, si corresponde, selector de institución.

Revisar aislamiento de datos en todos los módulos.

Revisar permisos administrativos por institución.

Realizar pruebas integrales de multi-tenancy lógico.

16. Despliegue en producción

Estado: ⏳ PENDIENTE

Actualmente HospitalLearning funciona en entorno local.

Antes de producción deberán revisarse configuración de producción, base de datos, seguridad, SECRET_KEY mediante variable de entorno, DEBUG = False, ALLOWED_HOSTS, archivos estáticos y multimedia, copias de seguridad, servidor WSGI/ASGI, dominio, HTTPS, estrategia de despliegue, multi-IPS y pruebas funcionales y de seguridad.

Documentación del proyecto

Documento

Estado

00_ROADMAP.md

✅ Actualizado al estado funcional actual

01_vision_del_proyecto.md

✅ Elaborado

02_modelo_funcional.md

✅ Elaborado

03_modelo_de_datos.md

🟡 Requiere depuración y actualización

99_ideas_futuras.md

✅ Disponible

PROMPT_MAESTRO_HOSPITALLEARNING.md

✅ Disponible

Observación sobre el modelo de datos

03_modelo_de_datos.md deberá depurarse y actualizarse según los modelos Django realmente implementados, TrainingAssignment, TrainingResult, Certificate, las interfaces actuales, la futura relación entre evaluaciones HTML y nativas, las bibliotecas institucionales y el alcance multi-IPS.

Objetivo de la versión 1.0

Desarrollar una plataforma web para gestionar acciones de formación continua dirigidas al talento humano en salud, incluyendo instituciones y usuarios, acciones de formación, asignaciones, contenido interactivo, seguimiento, evaluación, certificación, bibliotecas institucionales, Dashboard, indicadores, reportes, navegación diferenciada por rol y administración institucional integrada.

La arquitectura deberá permitir el uso de HospitalLearning por múltiples Instituciones Prestadoras de Servicios de Salud.

PRÓXIMO OBJETIVO

Bibliotecas institucionales

El siguiente bloque será implementar conjuntamente:

Biblioteca Documental

Biblioteca Multimedia

Las bibliotecas deberán:

Respetar el aislamiento por institución.

Permitir reutilización de recursos.

Permitir asociación con acciones de formación.

Integrarse con la navegación administrativa.

Mantener trazabilidad básica.

Evitar duplicación innecesaria de recursos.

Preparar la arquitectura para futuras mejoras de versionamiento y vigencia documental.

La Biblioteca Documental gestionará protocolos, guías, procedimientos, manuales, instructivos, formatos, resoluciones y otros documentos institucionales.

La Biblioteca Multimedia gestionará videos, presentaciones, audios, imágenes, infografías, enlaces y otros recursos multimedia.

Una vez implementadas y validadas ambas bibliotecas, el siguiente bloque será definir e implementar el Banco Institucional de Preguntas y las evaluaciones nativas, preservando la compatibilidad con las evaluaciones actualmente incorporadas en contenidos HTML.