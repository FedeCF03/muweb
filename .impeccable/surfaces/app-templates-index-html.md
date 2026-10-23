---
version: 1
slug: "app-templates-index-html"
primary_target: "app/templates/index.html"
related_targets: ["app/templates/base.html"]
---

# Surface: sitio completo (shell de portal) + home

Scope: base.html es ahora un portal de tres columnas que envuelve todas las rutas; `/` llena la columna central. Mode: Persuade.
Audience: veteranos de MU de AR/LatAm que vuelven. Acción: descargar el cliente, crear cuenta, entrar.
Constraints: contenido en content/; sin datos inventados (rankings y castle siege vacíos y honestos hasta la v1); la red del server nunca se publica; arte = renders propios del usuario (~/Downloads/MU Renders), nunca arte ni marca de otros servers.
Reemplaza el mundo "tablero nocturno" (el usuario lo cambió por esta referencia).

## Direction contract

THESIS: El portal clásico de server de MU de los 2000, hecho con oficio: marco dorado tallado, arte de personajes en la cabecera, tres columnas como las que el veterano leía en el ciber. Rechaza la landing moderna de una columna con hero y filas de tarjetas.

OWN-WORLD: fondo casi negro con calor (#0c0907), marcos de oro viejo (#c9a14a, filete claro #f0d488, bronce #6b4a1f), cajas oscuras de cuero (#17110b), columna central de pergamino (#e9dcbc) con tinta marrón (#2b1d0e) y rojo lacre para enlaces (#8c1d12). Cinzel para títulos y logo (oro sólido, sin texto degradado; un logo raster tallado queda pendiente de arte del usuario); Alegreya Sans para el cuerpo (cambio desde Inter: humanista de pluma que se lee bien sobre pergamino, e Inter era el reflejo por defecto que marcó el detector). Esquinas de filigrana dorada en SVG propio sobre cajas y pergamino; botón principal de oro con brillo de metal. Títulos de bloque con alas doradas a los lados.

STORY: El visitante reconoce al instante "un server de MU", ve los renders, los rates y el próximo evento, y tiene a mano en la columna izquierda Descargar y Crear cuenta; la derecha le explica cómo jugar.

FIRST VIEWPORT: cabecera de arte de ~330px: caballero alado rojo a la izquierda, mago alado azul a la derecha, logo OPENMUARG al centro con "Season 6 · Episode 3"; el estado del server solo aparece si se mide en vivo (FEATURE_STATUS). En 390px queda un solo render (caballero alado) centrado detrás del logo al 40%. Debajo, barra de navegación de bronce con filetes dorados. Tres columnas: izquierda, fija al hacer scroll en escritorio (Panel de cuenta honesto + botón dorado DESCARGAR CLIENTE + menú), centro pergamino (bienvenida con rates y próximo evento con cuenta regresiva, luego novedades), derecha (Cómo jugar en 3 pasos, Castle Siege y Top personajes vacíos con "llega con la v1", Discord).

FORM: referencia fijada por el usuario (estilo de portal de infinitymu.net, solo como inspiración de forma; nada de su arte, nombre ni textos). seed:8dd7ea46eaaec272 (hand overridden by user-pinned reference). Signature: la cabecera con renders en capas que se separan apenas con el scroll (parallax suave, apagado con reduced motion); cuenta regresiva viva en la bienvenida.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
