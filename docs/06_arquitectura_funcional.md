# ARQUITECTURA FUNCIONAL

## 1. PROPÓSITO

HospitalLearning es una plataforma para la gestión de acciones de formación continua del talento humano en salud.

Su propósito es planificar, asignar, desarrollar, evaluar, certificar y realizar seguimiento a las acciones de formación dirigidas al personal de una o varias Instituciones Prestadoras de Servicios de Salud (IPS).

La plataforma no reemplaza sistemas de talento humano, nómina o gestión laboral. Su responsabilidad se limita exclusivamente a la administración del proceso de formación continua.

## 2. PRINCIPIO RECTOR

Toda funcionalidad desarrollada en HospitalLearning deberá contribuir al ciclo de gestión de las acciones de formación continua:

- Planificación.
- Asignación.
- Desarrollo.
- Evaluación.
- Certificación.
- Seguimiento.

No se incorporarán funcionalidades propias de sistemas de historia laboral, nómina, contratación o gestión de talento humano, salvo aquellas estrictamente necesarias para administrar el proceso de formación.

## 3. ACTORES DEL SISTEMA

HospitalLearning contempla los siguientes actores principales:

### 3.1 Administrador institucional

Responsable de la configuración de la plataforma dentro de una IPS.

Funciones principales:

- Administrar la institución.
- Configurar servicios y subservicios.
- Administrar usuarios y vinculaciones.
- Gestionar acciones de formación.
- Consultar reportes institucionales.

### 3.2 Instructor

Responsable de diseñar y administrar las acciones de formación.

Funciones principales:

- Crear acciones de formación.
- Asociar recursos de aprendizaje.
- Crear evaluaciones.
- Consultar resultados.

### 3.3 Participante

Talento humano en salud que desarrolla las acciones de formación asignadas.

Funciones principales:

- Consultar acciones asignadas.
- Estudiar el material disponible.
- Presentar evaluaciones.
- Obtener certificados cuando cumpla los requisitos.

## 4. MÓDULOS FUNCIONALES

HospitalLearning está organizado en módulos independientes, cada uno con una responsabilidad claramente definida.

### 4.1 Instituciones

Administra la información de las IPS registradas en la plataforma.

### 4.2 Servicios

Administra la estructura de servicios y subservicios de cada institución.

### 4.3 Usuarios

Administra la información básica de las personas que utilizan la plataforma.

### 4.4 Vinculaciones

Relaciona los usuarios con una institución y con uno o varios servicios.

### 4.5 Acciones de formación

Administra las actividades de capacitación, sus destinatarios, vigencia y recursos asociados.

### 4.6 Biblioteca documental

Gestiona los documentos de apoyo utilizados en las acciones de formación.

### 4.7 Biblioteca multimedia

Gestiona videos, imágenes y demás recursos audiovisuales.

### 4.8 Banco institucional de preguntas

Administra las preguntas reutilizables para las evaluaciones.

### 4.9 Evaluaciones

Gestiona las evaluaciones, intentos, calificaciones y resultados.

### 4.10 Certificados

Gestiona la emisión y consulta de certificados.

### 4.11 Reportes

Genera indicadores e informes de cumplimiento.

### 4.12 Dashboard

Presenta indicadores consolidados para la toma de decisiones.

## 5. REGLAS DE NEGOCIO

Las siguientes reglas rigen el funcionamiento de HospitalLearning:

1. Un usuario representa a una persona única dentro de la plataforma.

2. Un usuario puede estar vinculado a una o varias instituciones.

3. Cada vinculación pertenece a una única institución.

4. Una vinculación puede estar asociada a uno o varios servicios de la institución.

5. Los servicios pertenecen exclusivamente a una institución.

6. Los servicios pueden organizarse jerárquicamente mediante servicios principales y subservicios.

7. Una acción de formación puede dirigirse a:
   - Todos los servicios.
   - Uno o varios servicios específicos.

8. El cambio de servicio de un usuario no elimina ni modifica su historial de formación.

9. El historial de formación pertenece al usuario y no al servicio.

10. Una acción de formación puede utilizar múltiples documentos, recursos multimedia y evaluaciones.

11. El banco institucional de preguntas podrá reutilizarse en diferentes evaluaciones.

12. Un certificado solo podrá emitirse cuando el usuario cumpla los criterios definidos para la acción de formación.

## 6. FILOSOFÍA DE DISEÑO

HospitalLearning se desarrollará siguiendo los siguientes principios:

### Simplicidad

Cada funcionalidad deberá aportar valor directo al proceso de formación continua. No se incorporarán características ajenas al propósito de la plataforma.

### Escalabilidad

La arquitectura deberá permitir el crecimiento de la plataforma sin requerir rediseños importantes, soportando múltiples instituciones y diferentes estructuras organizacionales.

### Configurabilidad

Las instituciones deberán poder configurar sus servicios, recursos y acciones de formación sin necesidad de modificar el código fuente.

### Reutilización

Los recursos educativos, preguntas, evaluaciones y documentos deberán poder reutilizarse en diferentes acciones de formación.

### Trazabilidad

La plataforma conservará el historial de formación, evaluaciones y certificaciones de cada usuario, garantizando la disponibilidad de la evidencia para consulta y seguimiento.

### Separación de responsabilidades

HospitalLearning administrará exclusivamente el ciclo de formación continua y no reemplazará sistemas de talento humano, contratación, nómina o historia laboral.

## 7. FLUJO GENERAL DE UNA ACCIÓN DE FORMACIÓN

Toda acción de formación seguirá el siguiente ciclo:

1. Creación de la acción de formación.
2. Definición de los servicios destinatarios.
3. Asociación de recursos de aprendizaje:
   - Documentos.
   - Recursos multimedia.
4. Asociación de la evaluación correspondiente.
5. Publicación de la acción de formación.
6. Asignación automática a los usuarios según su vinculación y servicios.
7. Desarrollo de la actividad por parte del participante.
8. Presentación de la evaluación.
9. Registro de los resultados.
10. Emisión del certificado cuando se cumplan los criterios establecidos.
11. Disponibilidad permanente del historial de formación para consulta y seguimiento.

## 8. FICHA FUNCIONAL: ACCIONES DE FORMACIÓN

### Responsabilidad

Administrar las acciones de formación continua virtual dirigidas al talento humano en salud.

### Tipos de acción

- Inducción.
- Reinducción.
- Capacitación.
- Actualización.
- Entrenamiento.
- Socialización.
- Otro tipo de acción definido por la institución.

### Comportamiento del tipo de acción

Cada tipo de acción definirá las reglas generales de cumplimiento de las acciones que pertenezcan a esa categoría.

Como mínimo deberá definir:

- Si requiere certificación.
- Si tiene vigencia.
- Si debe renovarse periódicamente.
- El período de renovación (cuando aplique).
- Si una nueva versión obliga a repetir la formación.

### Información principal

Cada acción de formación deberá registrar:

- Código.
- Nombre.
- Tipo de acción.
- Descripción.
- Objetivo de aprendizaje.
- Institución responsable.
- Estado.
- Fecha de creación.
- Fecha de actualización.
- Versión.

### Destinatarios

Una acción de formación podrá dirigirse a:

- Todos los servicios de la institución.
- Uno o varios servicios específicos.

### Recursos asociados

Cada acción de formación podrá asociar:

- Documentos de la biblioteca documental.
- Recursos de la biblioteca multimedia.
- Una evaluación.

### Estados

- Borrador.
- Publicada.
- Archivada.

### Reglas de negocio

1. Una acción en estado Borrador no será visible para los participantes.

2. Una acción Publicada podrá asignarse automáticamente según los servicios de las vinculaciones activas.

3. Una acción dirigida a Todos los servicios aplicará a todas las vinculaciones activas de la institución.

4. Una acción dirigida a servicios específicos aplicará únicamente a usuarios vinculados con al menos uno de esos servicios.

5. El cambio posterior de servicio de un usuario no eliminará las acciones ya completadas, evaluaciones presentadas ni certificados obtenidos.

6. Los recursos institucionales podrán reutilizarse en varias acciones de formación.

7. Una acción archivada conservará su historial y evidencia, pero no recibirá nuevas asignaciones.

8. Toda acción de formación deberá tener una versión identificable.

9. La publicación de una nueva versión no eliminará el historial de las versiones anteriores.

## 9. ESTRUCTURA FUNCIONAL DEL PROCESO FORMATIVO

El proceso formativo se organiza en tres niveles independientes:

### 9.1 Tipo de acción

Define el comportamiento general de una categoría de formación.

Ejemplos:

- Inducción.
- Reinducción.
- Capacitación.
- Actualización.
- Entrenamiento.
- Socialización.

Cada tipo de acción podrá definir:

- Si requiere certificado.
- Si tiene vigencia.
- Si debe renovarse.
- El período de renovación.
- Si una nueva versión obliga a repetir la formación.

### 9.2 Acción de formación

Representa el contenido formativo específico creado por una institución.

Cada acción podrá registrar:

- Código.
- Nombre.
- Descripción.
- Objetivo.
- Tipo de acción.
- Versión.
- Institución responsable.
- Servicios destinatarios.
- Recursos documentales.
- Recursos multimedia.
- Evaluación.
- Estado.

### 9.3 Proceso Formativo del Participante

Representa la participación individual de un usuario en una acción de formación.

Cada ejecución permitirá registrar:

- Usuario.
- Acción de formación.
- Versión realizada.
- Fecha de asignación.
- Fecha de inicio.
- Fecha de finalización.
- Estado.
- Resultado de la evaluación.
- Certificado emitido, cuando corresponda.

La ejecución conservará el historial individual del usuario, aunque cambie de servicio o de vinculación dentro de la institución.

### Estados de la ejecución

Una ejecución podrá encontrarse en uno de los siguientes estados:

- Asignada.
- En progreso.
- Pendiente de evaluación.
- Aprobada.
- No aprobada.
- Completada.
- Vencida.
- Cancelada.

### Reglas de negocio de la ejecución

1. La ejecución pertenece al usuario y a una versión específica de la acción de formación.

2. Cambiar de servicio o de vinculación no elimina la ejecución ni su historial.

3. Una acción transversal podrá mantenerse vigente aunque el usuario cambie de servicio.

4. La aprobación dependerá del cumplimiento de los requisitos definidos para la acción.

5. El certificado solo podrá emitirse cuando la ejecución cumpla las condiciones establecidas.

6. Una ejecución vencida conservará su historial y evidencia.

7. La cancelación no eliminará los registros previos de actividad del usuario.

### Reglas del Proceso Formativo

1. Cada Proceso Formativo corresponde a un participante y a una versión específica de una acción de formación.

2. Un participante podrá tener varios Procesos Formativos a lo largo del tiempo, incluso sobre una misma acción cuando exista renovación, repetición o una nueva versión obligatoria.

3. El cambio de servicio o de vinculación no eliminará ni modificará los Procesos Formativos ya registrados.

4. Los resultados de evaluación, certificados y evidencias permanecerán asociados al Proceso Formativo correspondiente.

5. Una acción transversal podrá continuar siendo válida aunque el participante cambie de servicio dentro de la institución.

6. Cuando una nueva versión obligue a repetir la formación, se creará un nuevo Proceso Formativo sin eliminar el anterior.

7. Un Proceso Formativo archivado o vencido conservará toda su información para consulta, auditoría y seguimiento.

## 10. HISTORIAL FORMATIVO DEL PARTICIPANTE

El Historial Formativo corresponde a la consulta consolidada de todos los Procesos Formativos registrados para un participante.

No constituye un módulo independiente ni una entidad propia de almacenamiento, sino una vista funcional construida a partir de la información registrada en los Procesos Formativos.

El Historial Formativo permitirá consultar, entre otros:

- Acciones de formación realizadas.
- Versiones cursadas.
- Estados.
- Resultados de evaluación.
- Certificados emitidos.
- Fechas de asignación, inicio y finalización.
- Vigencias y renovaciones.
- Evidencias del proceso.

### Reglas de negocio

1. El Historial Formativo conservará toda la trayectoria de formación del participante.

2. Ningún cambio de servicio, vinculación o estructura institucional eliminará la información histórica.

3. Cada registro del historial corresponderá a un Proceso Formativo específico.

4. El historial podrá utilizarse para reportes, auditorías, seguimiento institucional y consulta por parte del participante.

## 11. ASIGNACIÓN DE ACCIONES DE FORMACIÓN

La asignación corresponde al proceso mediante el cual una acción de formación se vincula con los participantes que deben desarrollarla.

### Formas de asignación

Una acción de formación podrá asignarse:

- A todos los participantes con vinculación activa en una institución.
- A participantes vinculados con uno o varios servicios específicos.
- De forma individual a uno o varios participantes.

### Reglas de negocio

1. La asignación automática se realizará según la institución y los servicios asociados a la vinculación activa del participante.

2. Una acción dirigida a todos los servicios se asignará a todos los participantes activos de la institución.

3. Una acción dirigida a servicios específicos se asignará a quienes estén vinculados con al menos uno de esos servicios.

4. La asignación individual permitirá incluir participantes específicos sin depender de su servicio.

5. Cada asignación generará un Proceso Formativo para el participante y la versión correspondiente de la acción.

6. No se crearán Procesos Formativos duplicados para el mismo participante, acción y versión.

7. Un cambio posterior de servicio no eliminará los Procesos Formativos ya generados.

8. Las nuevas asignaciones se calcularán usando la vinculación y los servicios vigentes en ese momento.

## 12. MOTOR DE ASIGNACIÓN

El Motor de Asignación será el componente responsable de determinar cuándo, cómo y a quién se asignará una acción de formación.

### Responsabilidades

El Motor de Asignación deberá:

- Identificar los participantes destinatarios.
- Validar la institución.
- Validar los servicios asociados.
- Identificar la versión vigente de la acción.
- Evitar asignaciones duplicadas.
- Crear automáticamente el Proceso Formativo cuando corresponda.

### Tipos de asignación

El motor deberá soportar los siguientes mecanismos:

- Asignación por institución.
- Asignación por servicios.
- Asignación individual.
- Asignación por ingreso de un nuevo participante.
- Asignación por cambio de servicio.
- Asignación por publicación de una nueva versión obligatoria.

### Reglas de negocio

1. El Motor de Asignación nunca modificará Procesos Formativos históricos.

2. Toda nueva asignación generará un nuevo Proceso Formativo cuando sea necesario.

3. El motor verificará previamente la existencia de un Proceso Formativo equivalente para evitar duplicados.

4. Toda asignación deberá quedar registrada para efectos de auditoría y seguimiento.

## 13. FICHA FUNCIONAL: INSTITUCIONES

### Responsabilidad

Administrar las Instituciones Prestadoras de Servicios de Salud (IPS) que utilizan HospitalLearning.

### Información principal

Cada institución deberá registrar:

- Nombre.
- Número de Identificación Tributaria (NIT).
- Código institucional.
- Estado activo o inactivo.

### Funciones

El módulo permitirá:

- Crear instituciones.
- Editar su información.
- Activar o inactivar instituciones.
- Consultar sus servicios.
- Consultar sus usuarios vinculados.
- Consultar sus acciones de formación.

### Reglas de negocio

1. Cada institución deberá tener un NIT único.

2. Cada institución deberá tener un código único dentro de la plataforma.

3. Una institución inactiva conservará toda su información histórica.

4. Inactivar una institución no eliminará usuarios, vinculaciones, procesos formativos, evaluaciones ni certificados.

5. Los servicios, acciones de formación y recursos institucionales deberán pertenecer a una institución.

6. La información de una institución no deberá mezclarse con la información de otras IPS.

### Límites del módulo

El módulo de Instituciones no administrará:

- Contratos laborales.
- Nómina.
- Historia laboral.
- Procesos de selección.
- Información clínica de pacientes.

## 14. FICHA FUNCIONAL: SERVICIOS

### Responsabilidad

Administrar los servicios y subservicios de cada institución para orientar la asignación de acciones de formación.

### Información principal

Cada servicio deberá registrar:

- Institución a la que pertenece.
- Nombre.
- Servicio principal, cuando corresponda.
- Estado activo o inactivo.

### Funciones

El módulo permitirá:

- Crear servicios.
- Editar servicios.
- Crear subservicios.
- Activar o inactivar servicios.
- Asociar uno o varios servicios a una vinculación.
- Utilizar los servicios como criterio de asignación de acciones de formación.

### Reglas de negocio

1. Cada servicio pertenece a una única institución.

2. Un servicio podrá depender de otro servicio de la misma institución.

3. Una vinculación podrá estar asociada a uno o varios servicios.

4. Inactivar un servicio no eliminará procesos formativos, evaluaciones ni certificados históricos.

5. Los servicios se utilizarán para definir los destinatarios de nuevas acciones de formación.

6. El cambio de servicios asociados a una vinculación no modificará el historial formativo del participante.

### Límites del módulo

El módulo de Servicios no administrará:

- Turnos.
- Horarios.
- Plantas de personal.
- Cargos laborales.
- Información clínica.

## 15. FICHA FUNCIONAL: USUARIOS

### Responsabilidad

Administrar la identidad de las personas que utilizan HospitalLearning.

### Información principal

Cada usuario deberá registrar como mínimo:

- Tipo de documento.
- Número de documento.
- Nombres.
- Apellidos.
- Correo electrónico.
- Profesión.
- Teléfono (opcional).
- Estado activo o inactivo.

### Funciones

El módulo permitirá:

- Registrar usuarios.
- Editar información básica.
- Activar o inactivar usuarios.
- Consultar sus vinculaciones.
- Consultar su Historial Formativo consolidado.

### Reglas de negocio

1. Cada persona deberá existir una sola vez en la plataforma.

2. El número de documento será único.

3. Un usuario podrá estar vinculado a una o varias instituciones.

4. La inactivación de un usuario no eliminará su Historial Formativo.

5. Toda la evidencia de formación permanecerá asociada al usuario.

6. El Historial Formativo consolidado corresponderá a la trayectoria completa del participante y podrá consultarse de forma global o filtrarse por institución cuando sea necesario.

### Límites del módulo

El módulo de Usuarios no administrará:

- Información contractual.
- Salarios.
- Horarios.
- Turnos.
- Evaluaciones de desempeño laboral.

## 16. MAPA MAESTRO DE RELACIONES FUNCIONALES

HospitalLearning organiza su funcionamiento a partir de las siguientes relaciones:

```text
Usuario
  │
  └── Vinculación institucional
          │
          ├── Institución
          └── Uno o varios servicios
                    │
                    ▼
           Motor de Asignación
                    │
                    ▼
          Acción de Formación
                    │
          ┌─────────┼─────────┐
          │         │         │
      Documentos  Multimedia  Evaluación
                    │
                    ▼
     Proceso Formativo del Participante
                    │
          ┌─────────┼─────────┐
          │         │         │
      Resultados  Certificado  Evidencias
                    │
                    ▼
       Historial Formativo Consolidado

       ## 17. FICHA FUNCIONAL: VINCULACIONES

### Responsabilidad

Administrar la relación entre un participante y una institución, definiendo los servicios en los que participa para efectos de asignación de acciones de formación.

### Información principal

Cada vinculación deberá registrar:

- Participante.
- Institución.
- Uno o varios servicios.
- Estado (activa o inactiva).
- Fecha de inicio de la vinculación.
- Fecha de finalización (opcional).

### Funciones

El módulo permitirá:

- Crear vinculaciones.
- Actualizar los servicios asociados.
- Activar o inactivar vinculaciones.
- Consultar el historial de vinculaciones de un participante.
- Servir como base para el Motor de Asignación.

### Reglas de negocio

1. Un participante podrá tener una sola vinculación activa por institución.

2. Una vinculación podrá estar asociada a uno o varios servicios.

3. La fecha de inicio será obligatoria.

4. La fecha de finalización será opcional y solo se registrará cuando la vinculación termine.

5. Una vinculación finalizada conservará todos los Procesos Formativos asociados.

6. Cambiar los servicios de una vinculación no modificará el Historial Formativo del participante.

7. El Motor de Asignación utilizará únicamente vinculaciones activas y vigentes para generar nuevas asignaciones.

### Límites del módulo

El módulo de Vinculaciones no administrará:

- Contratos laborales.
- Salarios.
- Tipo de contratación.
- Horarios.
- Turnos.
- Información de nómina.

## 18. FICHA FUNCIONAL: TIPOS DE ACCIÓN

### Responsabilidad

Administrar las categorías utilizadas por cada institución para clasificar sus acciones de formación continua.

### Información principal

Cada Tipo de Acción deberá registrar:

- Institución.
- Nombre.
- Código.
- Descripción (opcional).
- Estado activo o inactivo.
- Si requiere certificado.
- Si tiene vigencia.
- Si debe renovarse periódicamente.
- Período de renovación, cuando corresponda.
- Si una nueva versión obliga a repetir la formación.
- Objetivo del tipo de acción.

### Funciones

El módulo permitirá:

- Crear Tipos de Acción.
- Editarlos.
- Activarlos.
- Inactivarlos.
- Consultar Tipos de Acción activos e inactivos.
- Utilizarlos para clasificar Acciones de Formación.
- Definir reglas generales de cumplimiento.
- Orientar la clasificación de las Acciones de Formación mediante un objetivo claramente definido.

### Reglas de negocio

1. Cada Tipo de Acción pertenecerá a una única institución.

2. El nombre y el código deberán ser únicos dentro de la institución.

3. Un Tipo de Acción inactivo no podrá utilizarse en nuevas Acciones de Formación.

4. Inactivar un Tipo de Acción no modificará las Acciones de Formación históricas.

5. El período de renovación solo será obligatorio cuando el tipo requiera renovación periódica.

6. Las reglas del Tipo de Acción servirán como configuración inicial para las Acciones de Formación asociadas.

7. Las políticas específicas de una Acción de Formación podrán ajustarse cuando la institución lo autorice.

8. Una Acción de Formación solo podrá cambiar de Tipo mientras permanezca en estado Borrador. Una vez publicada, el Tipo de Acción quedará bloqueado.

9. Los Tipos de Acción no podrán eliminarse físicamente. Solo podrán inactivarse para preservar la integridad del historial institucional y de las Acciones de Formación asociadas.

## 19. FICHA FUNCIONAL: ACCIONES DE FORMACIÓN
### Responsabilidad

Administrar las acciones de formación continua virtuales creadas por cada institución, incluyendo su clasificación, contenido, destinatarios, versión, estado y reglas de cumplimiento.
### Información principal

### Configuración pedagógica

Al crear o editar una Acción de Formación en estado Borrador, el administrador definirá:

- Si requiere pretest.
- Si requiere evaluación final.
- Si el participante debe completar todo el contenido.
- Puntaje mínimo de aprobación, cuando exista evaluación final.
- Número máximo de intentos, cuando aplique.
- Si genera certificado.
- Si el certificado se emite automáticamente al cumplir los requisitos.

El pretest y la evaluación final serán componentes opcionales e independientes del contenido educativo principal.

Cada Acción de Formación deberá registrar:

- Institución.
- Tipo de Acción.
- Nombre.
- Código.
- Objetivo.
- Descripción.
- Versión.
- Estado.
- Responsable de la creación.
- Fecha de creación.
- Fecha de publicación (cuando aplique).

### Funciones

El módulo permitirá:

- Crear Acciones de Formación.
- Editarlas mientras permanezcan en estado Borrador.
- Publicarlas.
- Archivarlas.
- Asociarlas a un Tipo de Acción.
- Asociar documentos y recursos multimedia.
- Definir la población objetivo.
- Configurar las reglas específicas de cumplimiento cuando la institución lo autorice.

### Reglas de negocio

1. Toda Acción de Formación pertenecerá a una única institución.

2. Toda Acción de Formación deberá estar asociada a un único Tipo de Acción.

3. El código deberá ser único dentro de la institución.

4. La versión inicial será la 1.0.

5. Una Acción de Formación solo podrá cambiar de Tipo mientras permanezca en estado Borrador.

6. Una Acción de Formación publicada conservará su historial y no podrá eliminarse físicamente.

7. Las nuevas versiones no modificarán los Procesos Formativos ya finalizados.

8. Las reglas del Tipo de Acción se utilizarán como configuración inicial y podrán personalizarse cuando la institución lo autorice.

9. La obligatoriedad del pretest y de la evaluación final será definida por el administrador para cada Acción de Formación.

10. El contenido educativo principal será independiente de las evaluaciones.

11. Los parámetros pedagógicos podrán modificarse mientras la Acción de Formación permanezca en estado Borrador.

12. Una vez publicada la Acción de Formación, los parámetros que afecten el cumplimiento, la aprobación o la certificación quedarán bloqueados.

### Estados

Una Acción de Formación podrá encontrarse en uno de los siguientes estados:

- **Borrador:** puede modificarse libremente.
- **Publicada:** disponible para asignación y ejecución.
- **Archivada:** conserva su historial, pero ya no podrá asignarse a nuevos participantes.

### Relaciones

Una Acción de Formación:

- Pertenece a una única institución.
- Pertenece a un único Tipo de Acción.
- Puede tener múltiples documentos de apoyo.
- Puede tener múltiples recursos multimedia.
- Puede tener múltiples evaluaciones.
- Puede generar múltiples Procesos Formativos.
- Puede generar múltiples certificados.

### Resultado esperado

Cada Acción de Formación será la unidad académica central de HospitalLearning y concentrará toda la información necesaria para su ejecución, seguimiento, evaluación, certificación y trazabilidad, manteniendo la integridad del historial institucional.

## 20. FICHA FUNCIONAL: CONTENIDO DE LA CAPACITACIÓN

### Responsabilidad

Administrar todos los recursos de aprendizaje asociados a una Acción de Formación, permitiendo que los participantes accedan al contenido académico necesario para completar satisfactoriamente la capacitación.

---

### Objetivo

Centralizar el material educativo de cada capacitación, garantizando su organización, disponibilidad, control de versiones y reutilización institucional.

---

### Información principal

Cada contenido deberá registrar como mínimo:

- Acción de Formación.
- Tipo de contenido.
- Título.
- Descripción.
- Orden de visualización.
- Archivo o enlace.
- Estado (Activo/Inactivo).
- Fecha de creación.
- Responsable de creación.

---

### Tipos de contenido

El sistema permitirá registrar diferentes recursos, entre ellos:

- Documento PDF.
- Documento Word.
- Presentación.
- Hoja de cálculo.
- Imagen.
- Video.
- Audio.
- Enlace externo.
- Archivo comprimido.
- Otro recurso autorizado por la institución.

---

### Funciones

El módulo permitirá:

- Agregar contenido a una Acción de Formación.
- Editar información del contenido.
- Cambiar el orden de visualización.
- Activar o inactivar recursos.
- Reemplazar archivos conservando la trazabilidad.
- Eliminar contenidos que aún no hayan sido utilizados.
- Consultar todos los recursos asociados a una capacitación.

---

### Reglas de negocio

1. Todo contenido pertenecerá a una única Acción de Formación.

2. Una Acción de Formación podrá tener múltiples contenidos.

3. El orden de visualización deberá ser configurable.

4. Los contenidos inactivos no serán visibles para los participantes.

5. No podrá eliminarse un contenido que haga parte de un proceso formativo en ejecución.

6. La institución podrá definir qué tipos de archivos están permitidos.

7. Los archivos deberán cumplir las políticas institucionales de seguridad.

---

### Relaciones

Cada Contenido de Capacitación:

- Pertenece a una única Acción de Formación.
- Puede estar asociado a uno o varios documentos físicos.
- Puede utilizar recursos almacenados en la Biblioteca Documental.
- Puede utilizar recursos almacenados en la Biblioteca Multimedia.

---

### Resultado esperado

Cada Acción de Formación contará con un conjunto organizado de recursos educativos, facilitando el acceso al material de estudio y garantizando la trazabilidad de los contenidos utilizados durante el proceso de capacitación.

## 21. FICHA FUNCIONAL: ASIGNACIÓN DE CAPACITACIONES

### Responsabilidad

Determinar qué participantes deben desarrollar una Acción de Formación y generar el Proceso Formativo correspondiente para cada uno.

### Objetivo

Permitir que el administrador asigne capacitaciones de forma controlada, evitando duplicados y utilizando criterios institucionales claros.

### Formas de asignación

Una Acción de Formación podrá asignarse:

- A todos los participantes con vinculación activa en la institución.
- A participantes vinculados con uno o varios servicios específicos.
- De forma individual a uno o varios participantes.

### Información principal

Cada asignación deberá registrar:

- Acción de Formación.
- Institución.
- Forma de asignación.
- Servicios destinatarios, cuando aplique.
- Participantes seleccionados, cuando aplique.
- Responsable de la asignación.
- Fecha de asignación.
- Estado de la asignación.

### Funciones

El módulo permitirá:

- Seleccionar la Acción de Formación que será asignada.
- Definir la población destinataria.
- Asignar por institución.
- Asignar por servicios.
- Asignar individualmente.
- Consultar las asignaciones realizadas.
- Evitar asignaciones duplicadas.
- Generar automáticamente un Proceso Formativo para cada participante destinatario.

### Reglas de negocio

1. Solo podrán asignarse Acciones de Formación activas y publicadas.

2. La asignación por institución incluirá a todos los participantes con vinculación activa y vigente.

3. La asignación por servicios incluirá a los participantes vinculados con al menos uno de los servicios seleccionados.

4. La asignación individual permitirá seleccionar participantes específicos.

5. Cada asignación generará un Proceso Formativo para el participante y la versión correspondiente de la Acción de Formación.

6. No se crearán Procesos Formativos duplicados para el mismo participante, Acción de Formación y versión.

7. Los cambios posteriores de servicio o vinculación no eliminarán los Procesos Formativos ya generados.

8. Toda asignación deberá conservar el responsable y la fecha de creación para efectos de trazabilidad.

9. Una asignación no eliminará ni modificará Procesos Formativos históricos.

### Relaciones

Una Asignación de Capacitación:

- Pertenece a una Acción de Formación.
- Pertenece a una institución.
- Puede relacionarse con uno o varios servicios.
- Puede relacionarse con uno o varios participantes.
- Puede generar múltiples Procesos Formativos.

### Resultado esperado

El administrador podrá definir claramente a quién corresponde cada capacitación y el sistema generará los Procesos Formativos necesarios sin duplicar registros ni alterar el historial de los participantes.