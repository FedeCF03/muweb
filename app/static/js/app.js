/* ---------------------------------------------------------------------------
   muweb - JavaScript mínimo (sin dependencias).
   - Menú móvil
   - Cuenta regresiva del próximo evento
   - Parallax suave de la cabecera
   --------------------------------------------------------------------------- */

(function () {
  "use strict";

  /* --- Menú móvil ------------------------------------------------------- */
  var toggle = document.getElementById("nav-toggle");
  var menu = document.getElementById("nav-mobile");

  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("hidden") === false;
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
    });
  }

  /* --- Lightbox de la galería -------------------------------------------- */
  var lightbox = document.getElementById("lightbox");

  if (lightbox) {
    var content = lightbox.querySelector("[data-lightbox-content]");
    var title = lightbox.querySelector("[data-lightbox-title]");
    var closeBtn = lightbox.querySelector("[data-lightbox-close]");
    var lastFocus = null;

    var openLightbox = function (tile) {
      var clone = tile.cloneNode(true);
      clone.removeAttribute("data-lightbox");
      clone.setAttribute("aria-hidden", "true");
      clone.className = "relative aspect-video w-full overflow-hidden rounded-lg p-0";
      content.replaceChildren(clone);

      var name = tile.querySelector("[data-map]");
      if (name && title) {
        title.textContent = name.getAttribute("data-map");
      }

      lastFocus = document.activeElement;
      lightbox.hidden = false;
      document.body.style.overflow = "hidden";
      closeBtn.focus();
    };

    var closeLightbox = function () {
      if (lightbox.hidden) {
        return;
      }
      lightbox.hidden = true;
      document.body.style.overflow = "";
      content.replaceChildren();
      if (lastFocus && document.contains(lastFocus)) {
        lastFocus.focus();
      }
    };

    document.addEventListener("click", function (event) {
      if (event.target.closest("[data-lightbox]")) {
        event.preventDefault();
        openLightbox(event.target.closest("[data-lightbox]"));
      } else if (lightbox.hidden === false) {
        if (event.target === lightbox || event.target.closest("[data-lightbox-close]")) {
          closeLightbox();
        }
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closeLightbox();
      }
    });
  }

  /* --- Cuenta regresiva del próximo evento ------------------------------- */
  var countdowns = document.querySelectorAll("[data-countdown]");

  var pad = function (n) {
    return String(n).padStart(2, "0");
  };

  var renderCountdowns = function () {
    countdowns.forEach(function (el) {
      var target = new Date(el.getAttribute("data-countdown"));
      if (isNaN(target.getTime())) {
        el.textContent = "";
        return;
      }
      var diff = target.getTime() - Date.now();
      if (diff <= 0) {
        el.textContent = "¡Ya empezó!";
        return;
      }
      var total = Math.floor(diff / 1000);
      var days = Math.floor(total / 86400);
      var hours = Math.floor((total % 86400) / 3600);
      var minutes = Math.floor((total % 3600) / 60);
      var seconds = total % 60;
      el.textContent = (days > 0 ? days + "d " : "") + pad(hours) + ":" + pad(minutes) + ":" + pad(seconds);
    });
  };

  if (countdowns.length) {
    renderCountdowns();
    setInterval(renderCountdowns, 1000);
  }

  /* --- Cabecera: los renders se separan apenas con el scroll ----------- */
  var masthead = document.querySelector("[data-masthead]");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (masthead && !reduce && "requestAnimationFrame" in window) {
    var layers = masthead.querySelectorAll("[data-depth]");
    var ticking = false;
    var update = function () {
      var y = Math.min(window.scrollY, masthead.offsetHeight);
      layers.forEach(function (layer) {
        var depth = parseFloat(layer.getAttribute("data-depth")) || 0;
        layer.style.transform = "translate3d(0," + (y * depth).toFixed(1) + "px,0)";
      });
      ticking = false;
    };
    window.addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          ticking = true;
          requestAnimationFrame(update);
        }
      },
      { passive: true }
    );
  }
})();
