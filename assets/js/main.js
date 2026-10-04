// Mobile nav toggle
document.addEventListener("DOMContentLoaded", function () {
  var btn = document.querySelector(".menu-btn");
  var nav = document.querySelector(".nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      nav.classList.toggle("open");
    });
  }

  // Email capture -> Substack subscribe
  var forms = document.querySelectorAll("[data-capture-form]");
  forms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var email = form.querySelector('input[type="email"]').value.trim();
      var url = "https://alexisbendickson.substack.com/subscribe";
      // Substack's subscribe page accepts the email via its own form;
      // open it in a new tab so the reader finishes subscribing there.
      window.open(url, "_blank", "noopener");
      var note = form.parentElement.querySelector("[data-capture-note]");
      if (note) {
        note.textContent = email
          ? "Opening the subscription page — finish subscribing there and you're in."
          : "Opening the subscription page now.";
      }
    });
  });

  // Footer year
  var y = document.querySelector("[data-year]");
  if (y) y.textContent = new Date().getFullYear();
});
