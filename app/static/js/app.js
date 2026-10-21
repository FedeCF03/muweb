/* ---------------------------------------------------------------------------
   muweb - JavaScript mínimo (sin dependencias).
   - Menú móvil
   - Revelado de bloques al hacer scroll
   - Copiar al portapapeles
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

  /* --- Revelado al hacer scroll ----------------------------------------- */
  var revealables = document.querySelectorAll(".reveal");

  if (revealables.length) {
    var revealAll = function () {
      revealables.forEach(function (el) {
        el.classList.add("is-visible");
      });
    };

    if (!("IntersectionObserver" in window)) {
      // Sin IntersectionObserver mostramos todo: el contenido nunca queda invisible.
      revealAll();
    } else {
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              observer.unobserve(entry.target);
            }
          });
        },
        { rootMargin: "0px 0px -10% 0px", threshold: 0.08 }
      );

      revealables.forEach(function (el) {
        observer.observe(el);
      });

      // Red de seguridad: si el navegador restaura el scroll o algo falla,
      // todo lo que ya está en pantalla se muestra igual.
      var sweep = function () {
        revealables.forEach(function (el) {
          if (el.classList.contains("is-visible")) {
            return;
          }
          var rect = el.getBoundingClientRect();
          if (rect.top < window.innerHeight * 0.95 && rect.bottom > 0) {
            el.classList.add("is-visible");
            observer.unobserve(el);
          }
        });
      };

      window.addEventListener("scroll", sweep, { passive: true });
      window.addEventListener("resize", sweep);
      window.addEventListener("load", sweep);
      window.addEventListener("pageshow", sweep);
    }
  }

  /* --- Copiar al portapapeles ------------------------------------------- */
  document.querySelectorAll("[data-copy]").forEach(function (button) {
    button.addEventListener("click", function () {
      var value = button.getAttribute("data-copy") || "";
      var done = function () {
        var original = button.getAttribute("title");
        button.setAttribute("title", "¡Copiado!");
        button.classList.add("text-gold");
        setTimeout(function () {
          button.removeAttribute("title");
          button.classList.remove("text-gold");
          if (original) {
            button.setAttribute("title", original);
          }
        }, 1600);
      };

      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(value).then(done).catch(function () {});
      } else {
        var helper = document.createElement("textarea");
        helper.value = value;
        helper.setAttribute("readonly", "");
        helper.style.position = "absolute";
        helper.style.left = "-9999px";
        document.body.appendChild(helper);
        helper.select();
        try {
          document.execCommand("copy");
          done();
        } catch (err) {
          /* sin portapapeles: no pasa nada */
        }
        document.body.removeChild(helper);
      }
    });
  });
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
})();
