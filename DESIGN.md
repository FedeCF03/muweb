---
name: OpenMuArg
description: Portal clásico de server privado de MU Online Season 6, con marco de oro viejo, cajas de cuero y columna de pergamino.
colors:
  panel: "#0c0907"
  panel-deep: "#070504"
  panel-night: "#050403"
  face: "#17110b"
  glass: "#0a0705"
  plate: "#221910"
  plate-hi: "#3a2a17"
  edge: "#6b4a1f"
  edge-soft: "#2e2212"
  bronze-bar: "#1c140b"
  wing-band: "#120d08"
  lum: "#efe4cc"
  muted: "#bdac8b"
  faint: "#958466"
  radium: "#e2b85a"
  radium-dim: "#a8843d"
  gold: "#c9a14a"
  gold-hi: "#f0d488"
  gold-deep: "#7a5a22"
  amber: "#d4a640"
  gold-ink: "#241606"
  parchment: "#e9dcbc"
  parchment-deep: "#d8c497"
  ink: "#2b1d0e"
  parchment-muted: "#574330"
  parchment-faint: "#6b553a"
  lacre: "#8c1d12"
  lamp-on: "#5fd37a"
  warn: "#c8321f"
  warn-bright: "#e5533f"
typography:
  display:
    fontFamily: "Cinzel, ui-serif, Georgia, serif"
    fontSize: "clamp(2.4rem, 6.2vw, 4.4rem)"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.06em"
  headline:
    fontFamily: "Cinzel, ui-serif, Georgia, serif"
    fontSize: "clamp(1.6rem, 3.2vw, 2.3rem)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "0.02em"
  title:
    fontFamily: "Cinzel, ui-serif, Georgia, serif"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "0.02em"
  title-sm:
    fontFamily: "Cinzel, ui-serif, Georgia, serif"
    fontSize: "1rem"
    fontWeight: 700
    lineHeight: 1.375
    letterSpacing: "0.02em"
  box-title:
    fontFamily: "Cinzel, ui-serif, Georgia, serif"
    fontSize: "0.8rem"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "0.08em"
  nav:
    fontFamily: "Cinzel, ui-serif, Georgia, serif"
    fontSize: "0.82rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.12em"
  button:
    fontFamily: "Cinzel, ui-serif, Georgia, serif"
    fontSize: "0.82rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.1em"
  body:
    fontFamily: "Alegreya Sans, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.625
  body-sm:
    fontFamily: "Alegreya Sans, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.625
  label:
    fontFamily: "Alegreya Sans, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.7rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.1em"
  mono:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "0.85em"
    fontWeight: 400
    lineHeight: 1.4
rounded:
  chip: "2px"
  readout: "3px"
  control: "4px"
  panel: "6px"
  round: "999px"
spacing:
  box-pad: "16px"
  gutter: "24px"
  parchment-pad-sm: "16px"
  parchment-pad: "32px"
  section: "48px"
  sticky-top: "64px"
  side-column: "248px"
  container: "1248px"
components:
  button-primary:
    backgroundColor: "{colors.amber}"
    textColor: "{colors.gold-ink}"
    typography: "{typography.button}"
    rounded: "{rounded.control}"
    padding: "10.4px 20px"
    height: "44px"
  button-primary-hover:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.gold-ink}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.lum}"
    typography: "{typography.button}"
    rounded: "{rounded.control}"
    padding: "10.4px 20px"
    height: "44px"
  button-secondary-hover:
    textColor: "{colors.radium}"
  field:
    backgroundColor: "{colors.glass}"
    textColor: "{colors.lum}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.control}"
    padding: "9.6px 12px"
  nav-link:
    backgroundColor: "{colors.bronze-bar}"
    textColor: "{colors.muted}"
    typography: "{typography.nav}"
    padding: "13.6px 16px"
  nav-link-active:
    textColor: "{colors.gold-hi}"
  box:
    backgroundColor: "{colors.face}"
    textColor: "{colors.lum}"
    rounded: "{rounded.panel}"
    padding: "{spacing.box-pad}"
    width: "{spacing.side-column}"
  wing-title:
    backgroundColor: "{colors.wing-band}"
    textColor: "{colors.gold-hi}"
    typography: "{typography.box-title}"
    padding: "11.2px 8px 8.8px"
  parchment:
    backgroundColor: "{colors.parchment}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "{spacing.parchment-pad}"
  readout:
    backgroundColor: "{colors.glass}"
    textColor: "{colors.radium}"
    rounded: "{rounded.readout}"
    padding: "4px 10px"
  chip:
    backgroundColor: "transparent"
    textColor: "{colors.muted}"
    typography: "{typography.label}"
    rounded: "{rounded.chip}"
    padding: "3.2px 8.8px"
---

# Design System: OpenMuArg

## Overview

**Creative North Star: "El portal clásico"**

El sitio es el portal de server de MU de los 2000 que el veterano leía en el ciber, hecho con oficio: una cabecera de arte con renders de personajes alados, un logo de oro tallado, una barra de navegación de bronce con filetes dorados y, debajo, tres columnas. A los costados, cajas oscuras de cuero con esquinas de filigrana y títulos con alas; al centro, una hoja de pergamino con tinta marrón y enlaces en rojo lacre. La forma está tomada como inspiración de los portales de la época (referencia fijada por el usuario: infinitymu.net, solo forma); el arte, el nombre y los textos son propios.

La densidad es la de un portal, no la de una landing: mucha información a la vista, en cajas con título, y la acción principal (Descargar cliente, Crear cuenta) siempre a mano en la columna izquierda. El material manda: oro viejo, cuero oscuro con calor, pergamino con grano. El rechazo confirmado es la landing moderna de una sola columna con hero y filas de tarjetas.

El movimiento es mínimo y está atado al mundo: los renders de la cabecera se separan apenas con el scroll (parallax por `data-depth`), la cuenta regresiva del próximo evento late en la bienvenida, y todo se apaga con `prefers-reduced-motion`.

**Key Characteristics:**
- Cabecera de arte de ~330px con renders del usuario en capas y logo de oro sólido tallado con bisel.
- Barra de bronce sticky con filetes dorados dobles y rombos como separadores.
- Portal de tres columnas: cajas de cuero a los lados (sticky en escritorio), pergamino al centro.
- Esquinas de filigrana dorada en SVG propio sobre cada caja y sobre el pergamino.
- Dos superficies con tokens propios: el pergamino re-mapea la paleta oscura para que todo componente sea legible encima.
- Honestidad visible: los bloques sin datos reales dicen "Sin datos" en lugar de inventar.

## Colors

Oscuro con calor (casi negro tostado) para el marco, oro viejo para todo lo que es metal, y un pergamino claro como única superficie de lectura larga.

### Primary
- **Oro Viejo** (`gold`): el metal del sistema. Filetes de la barra de navegación, alas de los títulos, rombos separadores, selección de texto, relleno de las esquinas de filigrana.
- **Filete Claro** (`gold-hi`): el brillo del oro. Logo tallado, texto de los títulos de caja, enlace de navegación activo y en hover, anillo de foco (2px, offset 3px).
- **Bronce Hondo** (`gold-deep`): el oro en sombra. Bordes de cajas y del pergamino, línea bajo los títulos con alas, filetes de los títulos de sección del pergamino (al 60%), punteado de los rates.
- **Oro de Botón** (`amber`, con `gold-ink` como texto): la base del botón principal; el degradado metálico va por encima (ver Components).

### Secondary
- **Rojo Lacre** (`lacre`): el acento del pergamino. Enlaces dentro del pergamino, valores de los rates, cuenta regresiva, día de hoy en la agenda, rombos de las features, pestaña de clase elegida y relleno de las barras de atributo.

### Tertiary
- **Acento remapeable** (`radium`, `radium-dim`): oro brillante sobre fondo oscuro; dentro de `.parchment` se re-mapea a lacre (`#8c1d12`) y a un marrón tostado (`#7a4a1c`). Es el acento que usan los componentes compartidos (readout, chip, hover de botón secundario, viñetas de prosa) para tomar el color correcto según la superficie.
- **Lámpara encendida** (`lamp-on`): verde solo para la lámpara de estado "disponible" o "server online", con halo `0 0 6px 1px` al 55%. Nunca como color de texto ni de superficie.
- **Alerta** (`warn`, `warn-bright`): errores, lámpara de server caído, código 500.

### Neutral
- **Cuero Nocturno** (`panel`): fondo del body. `panel-deep` para la cabecera y el pie; `panel-night` para el `html`.
- **Cuero de Caja** (`face`): fondo de las cajas laterales. `glass` para campos y readouts; `plate` / `plate-hi` para lámparas apagadas y superficies elevadas; `edge` y `edge-soft` para bordes de controles y divisores de listas.
- **Barra de Bronce** (`bronze-bar`): fondo de la barra de navegación y anillo intermedio del marco del pergamino. `wing-band`, un paso más oscuro, es la banda de los títulos con alas.
- **Texto sobre oscuro** (`lum`, `muted`, `faint`): crema para títulos y texto fuerte, arena para cuerpo y enlaces de navegación en reposo, arena apagada para notas y estados vacíos.
- **Pergamino** (`parchment`, `parchment-deep`): la hoja central y sus bandas (próximo evento al 40%, fila de hoy al 50%).
- **Tinta** (`ink`, `parchment-muted`, `parchment-faint`): el texto sobre pergamino; son los valores que `lum`, `muted` y `faint` toman dentro de `.parchment`.

### Named Rules
**The Parchment Remap Rule.** El pergamino no recibe colores a mano: `.parchment` redefine `--color-lum`, `--color-muted`, `--color-faint`, `--color-radium`, `--color-face`, `--color-glass`, `--color-edge` y familia, y los componentes compartidos se leen bien en las dos superficies sin variantes. Un componente nuevo usa los tokens semánticos, nunca hex fijos.

**The Solid Gold Rule.** El oro es sólido. El logo es `gold-hi` con bisel hecho de sombras de texto; no hay texto con degradado (`background-clip: text`). El único degradado metálico del sistema es el relleno del botón principal.

**The Green Lamp Rule.** El verde existe solo como lámpara encendida de un estado medido. Si no hay medición, la lámpara no se prende.

## Typography

**Display Font:** Cinzel 600/700 (con ui-serif, Georgia, serif)
**Body Font:** Alegreya Sans 400/500/700 (con ui-sans-serif, system-ui, sans-serif)
**Label/Mono Font:** ui-monospace del sistema, solo para `code` en la prosa

**Character:** Cinzel trae las mayúsculas lapidarias del MU clásico: logo, títulos, navegación y botones. Alegreya Sans es una humanista de pluma que se lee bien sobre pergamino y en tamaños chicos sobre cuero. Ambas self-hosted (SIL OFL) en `app/static/fonts/`.

### Hierarchy
- **Display** (700, `clamp(2.4rem, 6.2vw, 4.4rem)`, 1, tracking 0.06em): solo el logo tallado de la cabecera (es el `h1` en la home) y su versión de 1.5rem en el pie.
- **Headline** (700, `clamp(1.6rem, 3.2vw, 2.3rem)`, 1.1): la bienvenida del pergamino.
- **Title** (700, 1.5rem, 1.1): títulos de sección del pergamino con filetes a los lados (`scroll-title`).
- **Title small** (700, 1rem a 1.125rem): títulos de noticia, nombre del evento, términos de los rates y features, nombres de mapa. Siempre Cinzel.
- **Box title** (700, 0.8rem, tracking 0.08em, mayúsculas): títulos de caja con alas.
- **Nav / Button** (700, 0.82rem, tracking 0.12em / 0.1em, mayúsculas): enlaces de la barra y botones.
- **Body** (400, 1rem / 0.875rem, 1.625): cuerpo; la prosa markdown va a 1.75 de interlínea y 68ch de ancho máximo, los resúmenes a 62ch.
- **Label** (700, 0.7rem, tracking 0.1em a 0.18em, mayúsculas): chips, estado de descarga ("Disponible", "Próximamente"), rótulo "Empieza en" de la cuenta regresiva.

### Named Rules
**The Carved Caps Rule.** Todo lo que es nombre, título o acción va en Cinzel; todo lo que se lee de corrido va en Alegreya Sans. Los números que cambian o se comparan (rates, cuenta regresiva, niveles, versiones) usan `tabular-nums`.

## Layout

Portal centrado de `container` (78rem) con tres columnas en escritorio (`lg`, 1024px): `side-column` (15.5rem) a cada lado y el pergamino en `minmax(0, 1fr)`, separadas por `gutter` (24px). Las dos columnas laterales son `sticky` a `sticky-top` (64px, debajo de la barra) en escritorio. Debajo de `lg` todo se apila: primero el pergamino, después la columna de cuenta/descarga/menú, después la de información; por eso la bienvenida repite Descargar y Crear cuenta en celular.

La cabecera mide 13rem en celular, 19rem en `sm` y 21rem en `lg`. En escritorio hay dos renders (caballero alado a la izquierda, mago alado a la derecha); en 390px queda solo el caballero, centrado detrás del logo al 40%. La barra de navegación es sticky arriba; en celular se colapsa a un botón de menú que despliega la lista.

Ritmo: las secciones del pergamino se separan por `section` (48px), las cajas laterales por 24px, el interior de las cajas por `box-pad` (16px, 17.6px a los lados). El pergamino tiene `parchment-pad-sm` en celular y `parchment-pad` desde `sm`. Las listas dentro del pergamino se dividen con filetes de 1px (`edge-soft`), no con tarjetas.

## Elevation & Depth

Profundidad de objeto físico, no de interfaz flotante: cada pieza es un marco con anillos y bisel. Las sombras son estructurales (anillos de borde que dibujan el marco) más una caída oscura debajo; no hay sombras de color ni resplandores salvo la lámpara encendida. El pergamino suma una viñeta interior tostada y grano (`noise.svg`, multiply al 55%).

### Shadow Vocabulary
- **Marco de caja** (`box-shadow: 0 0 0 1px #000, inset 0 0 0 1px rgb(240 212 136 / 0.08), 0 12px 24px -14px rgb(0 0 0 / 0.95)`): cajas laterales y lightbox.
- **Marco de pergamino** (`box-shadow: 0 0 0 1px #000, 0 0 0 4px #1c140b, 0 0 0 5px var(--color-gold-deep), inset 0 0 60px 0 rgb(122 82 30 / 0.35), inset 0 0 0 1px rgb(255 248 225 / 0.6)`): la hoja central; triple anillo negro, bronce y oro, viñeta y luz de borde.
- **Barra de bronce** (`box-shadow: 0 ±3px 0 0 #2a1d0e, 0 ±4px 0 0 var(--color-gold-deep), 0 10px 20px -6px rgb(0 0 0 / 0.9)`): filete doble arriba y abajo de la navegación.
- **Botón de oro** (`box-shadow: 0 0 0 1px var(--color-gold-deep), 0 6px 14px -6px rgb(0 0 0 / 0.9)` más `border-bottom: 3px solid #8a6424`): el canto del botón principal.
- **Bisel del logo** (`text-shadow: 0 1px 0 #fff3c4, 0 -1px 0 #5a3d12, 0 2px 0 #8a6424, 0 3px 0 #5a3d12, 0 8px 18px rgb(0 0 0 / 0.85)`): solo el logo tallado.

### Named Rules
**The Framed Object Rule.** Una superficie nueva se enmarca como caja o se escribe dentro del pergamino; no flota con una sombra suave genérica.

**The Flat Inside Rule.** Dentro del pergamino un panel no es una tarjeta: pierde fondo, radio y sombra, y queda como un tramo separado por un filete superior, como en un libro.

## Shapes

Esquinas apenas suavizadas: `panel` (6px) en cajas y pergamino, `control` (4px) en botones, campos y pestañas, `readout` (3px), `chip` (2px). Lo redondo es solo para lámparas, barras de atributo y los números de paso (`round`). El ornamento hace el trabajo de la forma: esquinas de filigrana SVG (`corner-tl/tr/bl/br.svg`, 28px sobre cajas a -5px, 44px sobre el pergamino a -9px), alas doradas a los costados de los títulos de caja y del subtítulo de la temporada, y rombos (cuadrados rotados 45°) como separadores de navegación, viñetas de menú, viñetas de features y viñetas de prosa.

## Components

### Buttons
Metal tallado para la acción principal, filete fino para el resto.
- **Shape:** esquinas suaves (`control`, 4px), alto mínimo de 44px; el de Descargar cliente de la columna izquierda sube a 56px y 0.95rem.
- **Primary:** degradado metálico vertical de oro (`#f6dc92` → `#d4a640` 46% → `#b4862c` 54% → `#e2bc62`) sobre `amber`, texto `gold-ink` con luz de texto, borde `#3a2608` con canto inferior de 3px `#8a6424`. Uno por vista: la descarga del cliente.
- **Hover / Focus:** el degradado se aclara un paso; `:active` baja 1px; foco con el anillo global `gold-hi`.
- **Secondary:** transparente, borde `edge`, texto `lum`; en hover borde y texto pasan a `radium` (oro en cuero, lacre en pergamino). Deshabilitado al 50%.

### Chips
- **Style:** borde `edge`, radio `chip`, etiqueta en mayúsculas 0.7rem, texto `muted`; en el detalle de noticia lleva el color `radium`.

### Cards / Containers
- **Caja lateral (`box`):** fondo `face`, borde `gold-deep`, radio `panel`, marco de caja, esquinas de filigrana. Siempre abre con un título con alas y sigue con `box-body`.
- **Pergamino (`parchment`):** la columna central de todas las rutas. Fondo `parchment`, tinta `ink`, enlaces `lacre`, marco de pergamino, grano y esquinas grandes.
- **Panel (`panel`):** contenedor genérico de subpáginas sobre `face` con borde `edge`; dentro del pergamino se aplana (Flat Inside Rule).
- **Readout:** valor numérico en caja chica, fondo `glass`, borde `edge`, `tabular-nums`, color `radium`. Niveles de mapa, 404/500.

### Inputs / Fields
- **Style:** fondo `glass`, borde `edge`, radio `control`, 0.875rem, placeholder `faint`, cursor de texto `gold`.
- **Focus:** anillo global de 2px `gold-hi` con offset 3px.
- **Disabled:** al 60% con cursor bloqueado; el panel de cuenta queda así hasta que la web hable con OpenMU, con una nota que lo explica.

### Navigation
- **Barra de bronce:** sticky, fondo `bronze-bar`, filetes dorados dobles. Enlaces en Cinzel mayúsculas `muted`, separados por rombos `gold-deep`; hover `gold-hi`; activo `gold-hi` con subrayado interior de 2px `gold`. En celular, nombre del sitio más botón de menú secundario que despliega la lista con divisores `edge-soft`.
- **Menú lateral:** lista en la caja Menú, viñeta rombo `gold`, texto `muted`, hover y actual `gold-hi`.

### Cabecera de arte (signature)
Fondo `panel-deep` con tres resplandores radiales (lacre abajo a la izquierda, azul abajo a la derecha, oro tenue al centro) y fundido a `panel-deep` en el 45% inferior. Renders del usuario como capas absolutas al 112% del alto, con `data-depth` (0.18 y 0.12) para el parallax. Al centro, logo tallado y subtítulo de temporada entre dos alas. La línea de estado del server aparece solo cuando `server_status.source == "live"`.

### Títulos con alas y títulos de pergamino
- **Wing title:** banda `wing-band` arriba de cada caja, borde inferior `gold-deep`, texto `gold-hi` en Cinzel mayúsculas, un ala dorada SVG a cada lado (la derecha espejada).
- **Scroll title:** título de sección del pergamino en `ink`, con un filete `gold-deep` al 60% que se estira a cada lado.

### Selector de clase y barra de atributo
Pestañas de radio puro en CSS (funciona sin JS): borde `edge`, Cinzel 0.78rem; la elegida en `lacre` con fondo lacre al 8%. Cada clase muestra sus atributos como barras redondas de 0.5rem rellenas de `lacre`.

### Próximo evento y rates
Rates como lista de términos Cinzel `ink` con punteado `gold-deep` hasta el valor `lacre`, como un menú de taberna. El próximo evento va en una banda de doble filete `gold-deep` sobre `parchment-deep` al 40%, con la cuenta regresiva en Cinzel 1.5rem `lacre` tabular.

### Lightbox
Velo `panel-night` al 94%, panel tipo caja de hasta 56rem, cierre con botón secundario y Esc; el foco vuelve al disparador.

## Do's and Don'ts

### Do:
- **Do** poner todo contenido de ruta dentro del pergamino central y todo bloque lateral en una caja con título con alas y esquinas de filigrana.
- **Do** usar los tokens semánticos (`lum`, `muted`, `faint`, `radium`, `face`, `glass`, `edge`) para que el componente funcione en cuero y en pergamino sin variantes.
- **Do** mantener Descargar cliente como el único botón de oro de la vista y a un paso desde cualquier ruta (columna izquierda en escritorio, bienvenida en celular).
- **Do** usar solo arte provisto por el usuario (renders en `app/static/img/renders/`), cada raster con su sidecar `.json` de procedencia.
- **Do** dejar Castle Siege y Top personajes honestamente vacíos ("Sin datos", "llega cuando conectemos la web con OpenMU") hasta que existan datos reales de OpenMU.
- **Do** mostrar la línea de estado del server y su lámpara solo cuando el estado se mide en vivo (`FEATURE_STATUS`).
- **Do** apagar el parallax y las transiciones con `prefers-reduced-motion`.

### Don't:
- **Don't** mostrar la dirección de red ni el puerto del server en ninguna parte del sitio.
- **Don't** usar arte, nombres ni textos de otros servers; la referencia de portal es solo de forma.
- **Don't** usar texto con degradado; el oro del logo es sólido con bisel de sombras.
- **Don't** volver a la landing de una sola columna con hero y filas de tarjetas.
- **Don't** meter tarjetas con fondo y sombra dentro del pergamino; ahí se separa con filetes.
- **Don't** prender el verde de lámpara para un estado que no se midió.

Pendiente (no es regla): el logo raster de oro tallado y las placas de marco esperan arte del usuario; hasta entonces el logo es Cinzel `gold-hi` con bisel CSS y los marcos son CSS más esquinas SVG.
