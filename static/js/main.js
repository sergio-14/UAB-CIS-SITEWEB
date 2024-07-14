(function ($) {
  "use strict";

  // Spinner
  var spinner = function () {
    setTimeout(function () {
      if ($("#spinner").length > 0) {
        $("#spinner").removeClass("show");
      }
    }, 1);
  };
  spinner();

  // Sidebar Toggler
  $(".sidebar-toggler").click(function () {
    $(".sidebar, .content").toggleClass("open");
    return false;
  });
})(jQuery);

/*
 Sirve para probar si se esta cargando el js.
(function ($) {
    "use strict";

    alert("main.js esta siendo cargado!");

})(jQuery);
*/

window.sr = ScrollReveal();
sr.reveal(".navbar", {
  duration: 3000,
  origin: "bottom",
  distance: "-100px",
});

window.sr = ScrollReveal();
sr.reveal(".imgtransision ", {
  duration: 3000,
  origin: "bottom",
  distance: "-100px",
});

window.sr = ScrollReveal();
sr.reveal(".logomujer", {
  duration: 3000,
  origin: "left",
  distance: "-100px",
});

window.sr = ScrollReveal();
sr.reveal(".p1 ", {
  duration: 3000,
  origin: "right",
  distance: "-100px",
});

window.sr = ScrollReveal();
sr.reveal(".fila", {
  duration: 3000,
  origin: "top",
  distance: "-100px",
});

window.sr = ScrollReveal();
sr.reveal(".topics", {
  duration: 3000,
  origin: "left",
  distance: "-100px",
});

window.sr = ScrollReveal();
sr.reveal(".izquierda", {
  duration: 3000,
  origin: "right",
  distance: "-100px",
});

window.sr = ScrollReveal();
sr.reveal(".derecha", {
  duration: 3000,
  origin: "left",
  distance: "-100px",
});

window.sr = ScrollReveal();
sr.reveal(".rueda", {
  duration: 4000,
  rotate: {
    x: 1,
    y: 180,
  },
});
window.sr = ScrollReveal();
sr.reveal(".info-wrap", {
  duration: 3000,
  origin: "left",
  distance: "-100px",
});

window.sr = ScrollReveal();
sr.reveal(".anime", {
  duration: 4000,
  rotate: {
    x: 1,
    y: 180,
  },
});
