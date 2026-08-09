# PROMPT MAESTRO PARA CREAR CAPACITACIONES COMPATIBLES CON HOSPITALLEARNING

Necesito crear una capacitación virtual interactiva para ser utilizada
dentro de la plataforma **HospitalLearning**.

**Tema de la capacitación:** \[ESCRIBIR TEMA\]

**Público objetivo:** \[ESCRIBIR PÚBLICO\]

**Documento(s) fuente:** \[ADJUNTAR DOCUMENTOS O INDICAR FUENTES\]

La capacitación debe basarse prioritariamente en los documentos
proporcionados. No inventes información que no esté respaldada por las
fuentes. Si se requiere información adicional, indícala claramente antes
de incorporarla.

## 1. FORMATO DE ENTREGA

Genera **un único archivo HTML autocontenido**, listo para cargarse como
contenido de aprendizaje en HospitalLearning.

El archivo debe funcionar localmente y **sin conexión a internet**.

No debe depender de CDN, Bootstrap externo, Google Fonts, JavaScript
externo, imágenes remotas ni otros recursos de internet.

CSS y JavaScript deben estar incluidos dentro del mismo archivo HTML.

## 2. ESTRUCTURA DE LA CAPACITACIÓN

Debe contener:

**Pretest → Contenido por módulos → Postest → Finalización**

El pretest debe aparecer antes del contenido.

El participante no debe poder acceder a los módulos hasta completar el
pretest.

El contenido debe dividirse en módulos claramente identificados.

El postest debe permanecer bloqueado hasta que el participante haya
revisado **todos los módulos obligatorios**.

No debe bastar con hacer clic rápidamente en los módulos para
considerarlos completados; cada módulo debe tener una interacción o
mecanismo razonable de confirmación de revisión.

## 3. PRETEST

Crear \[NÚMERO\] preguntas.

Utilizar preguntas de selección múltiple con una sola respuesta
correcta.

Mostrar todas las opciones de manera clara.

Registrar el resultado porcentual del pretest.

El pretest es diagnóstico y **no debe impedir continuar la capacitación
por obtener un puntaje bajo**.

Una vez enviado correctamente, debe quedar bloqueado para evitar
modificar posteriormente la línea base.

## 4. CONTENIDO

Organizar el contenido en aproximadamente \[NÚMERO\] módulos.

Cada módulo debe tener:

-   título;
-   objetivo o idea central;
-   contenido educativo;
-   elementos visuales;
-   cuadros destacados;
-   conceptos clave;
-   actividades o interacciones cuando sean útiles;
-   navegación anterior/siguiente.

Evitar páginas saturadas de texto. Priorizar tarjetas, esquemas, líneas
de tiempo, tablas, diagramas, ilustraciones y elementos interactivos.

Las imágenes o ilustraciones necesarias deben estar incorporadas
localmente o construidas mediante HTML/CSS/SVG, de manera que la
capacitación continúe funcionando sin internet.

## 5. POSTEST

Crear \[NÚMERO\] preguntas de evaluación final.

Deben evaluar los objetivos de aprendizaje y no limitarse a repetir
literalmente el pretest.

Utilizar selección múltiple con una sola respuesta correcta.

Calcular el resultado porcentual.

HospitalLearning será responsable de determinar la aprobación de acuerdo
con el puntaje mínimo y número máximo de intentos configurados en la
plataforma.

El HTML no debe inventar reglas distintas de aprobación.

## 6. INTEGRACIÓN CON HOSPITALLEARNING

La capacitación debe estar preparada para integrarse con el sistema
padre de HospitalLearning.

HospitalLearning controla externamente:

-   estado de la asignación;
-   resultado inicial del pretest;
-   mejor resultado del postest;
-   número de intentos;
-   módulos completados;
-   módulo actual;
-   etapa actual de la capacitación;
-   aprobación;
-   finalización;
-   emisión del certificado.

El HTML debe **informar los eventos y resultados al sistema padre**,
pero no debe considerarse a sí mismo la fuente definitiva de estos
datos.

Debe permitir restaurar el progreso recibido desde HospitalLearning
cuando el participante salga y posteriormente vuelva a ingresar.

El progreso debe diferenciar como mínimo las etapas:

`PRETEST`, `CONTENT`, `POSTTEST` y `COMPLETED`.

## 7. REANUDACIÓN

Si el participante abandona la capacitación durante un módulo y
posteriormente vuelve, debe poder continuar desde el punto registrado
por HospitalLearning.

Los módulos previamente completados deben mostrarse como completados.

No desbloquear el postest mientras HospitalLearning no indique que todos
los módulos requeridos han sido completados.

## 8. FINALIZACIÓN

Después de completar el postest y cumplir las reglas establecidas por
HospitalLearning, mostrar el botón:

**TERMINAR CAPACITACIÓN**

La capacitación solamente debe considerarse finalizada después de que
HospitalLearning confirme la operación.

No generar certificados dentro del HTML. Los certificados son
responsabilidad exclusiva de HospitalLearning.

## 9. DISEÑO

Utilizar un diseño profesional orientado a capacitación del talento
humano en salud.

Debe ser responsive y funcionar correctamente en computador y tablet.

Utilizar buena jerarquía visual, contraste adecuado, tipografía legible,
botones claros y navegación sencilla.

Evitar animaciones innecesarias o elementos decorativos que dificulten
el aprendizaje.

## 10. ACCESIBILIDAD

Utilizar HTML semántico, etiquetas apropiadas, contraste suficiente,
navegación comprensible y textos alternativos cuando correspondan.

No depender exclusivamente del color para comunicar estados de
aprobación, progreso o navegación.

## 11. CONTROL DE CALIDAD

Antes de entregar el archivo, verifica:

-   funcionamiento sin internet;
-   ausencia de enlaces o dependencias externas;
-   pretest bloqueando inicialmente el contenido;
-   registro correcto del pretest;
-   navegación entre módulos;
-   registro del progreso;
-   restauración del progreso;
-   bloqueo del postest hasta completar todos los módulos;
-   cálculo correcto de resultados;
-   control de intentos por HospitalLearning;
-   finalización;
-   ausencia de errores JavaScript;
-   compatibilidad con HospitalLearning.

**No cambies el protocolo de comunicación con HospitalLearning ni
inventes nombres de eventos, funciones o estructuras de datos. Si no se
proporciona la especificación técnica de integración, solicita el
archivo HTML de referencia o la especificación antes de programar esa
parte.**

Entrega finalmente el archivo `.html` completo listo para realizar
pruebas en HospitalLearning.

## INSTRUCCIÓN CUANDO SE ADJUNTE UNA CAPACITACIÓN DE REFERENCIA

Usa el archivo HTML de referencia adjunto exclusivamente como
especificación técnica de integración con HospitalLearning. Conserva el
protocolo de comunicación, registro de progreso, restauración, pretest,
postest y finalización. Cambia el contenido educativo, preguntas,
módulos y diseño según el nuevo tema.
