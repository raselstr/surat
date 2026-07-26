(function () {
  function ensureContainer() {
    var container = document.querySelector(".app-toast-container");

    if (container) {
      return container;
    }

    container = document.createElement("div");
    container.className = "app-toast-container";
    container.setAttribute("aria-live", "polite");
    container.setAttribute("aria-atomic", "true");
    document.body.appendChild(container);
    return container;
  }

  function normalizeLevel(level) {
    var tags = String(level || "").split(/\s+/);

    if (tags.indexOf("danger") >= 0) {
      return "error";
    }

    for (var index = 0; index < tags.length; index += 1) {
      if (["success", "error", "warning", "info"].indexOf(tags[index]) >= 0) {
        return tags[index];
      }
    }

    return "info";
  }

  function iconFor(level) {
    var icons = {
      success: "ti ti-circle-check",
      error: "ti ti-alert-circle",
      warning: "ti ti-alert-triangle",
      info: "ti ti-info-circle"
    };

    return icons[level] || icons.info;
  }

  function defaultTitle(level) {
    var titles = {
      success: "Berhasil",
      error: "Gagal",
      warning: "Perhatian",
      info: "Informasi"
    };

    return titles[level] || titles.info;
  }

  function showToast(options) {
    var config = options || {};
    var level = normalizeLevel(config.level || "info");
    var title = config.title || defaultTitle(level);
    var message = config.message || "";
    var container = ensureContainer();
    var toastEl = document.createElement("div");

    toastEl.className = "toast app-toast app-toast-" + level;
    toastEl.setAttribute("role", "alert");
    toastEl.setAttribute("aria-live", "assertive");
    toastEl.setAttribute("aria-atomic", "true");

    toastEl.innerHTML = [
      '<div class="toast-body">',
      '<span class="app-toast-icon"><i class="' + iconFor(level) + '"></i></span>',
      '<div class="flex-grow-1">',
      '<div class="app-toast-title"></div>',
      '<div class="app-toast-message"></div>',
      '</div>',
      '<button type="button" class="btn-close ms-2 mt-1" data-bs-dismiss="toast" aria-label="Tutup"></button>',
      '</div>'
    ].join("");

    toastEl.querySelector(".app-toast-title").textContent = title;
    toastEl.querySelector(".app-toast-message").textContent = message;
    container.appendChild(toastEl);

    if (!window.bootstrap || !window.bootstrap.Toast) {
      window.setTimeout(function () {
        toastEl.remove();
      }, config.delay || 4500);
      return;
    }

    var toast = bootstrap.Toast.getOrCreateInstance(toastEl, {
      autohide: config.autohide !== false,
      delay: config.delay || 4500
    });

    toastEl.addEventListener("hidden.bs.toast", function () {
      toastEl.remove();
    });

    toast.show();
  }

  window.appToast = {
    show: showToast,
    success: function (message, title) {
      showToast({ level: "success", title: title, message: message });
    },
    error: function (message, title) {
      showToast({ level: "error", title: title, message: message, delay: 6500 });
    }
  };
})();
