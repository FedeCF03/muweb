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
})();
