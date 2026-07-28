(function () {
  var crudModal = null;

  function getCrudModal() {
    var modalEl = document.getElementById("crudModal");
    if (!modalEl || !window.bootstrap) {
      return null;
    }
    crudModal = crudModal || bootstrap.Modal.getOrCreateInstance(modalEl);
    return crudModal;
  }

  function initSelect2(scope) {
    if (!window.jQuery || !jQuery.fn.select2) {
      return;
    }

    var $scope = scope ? jQuery(scope) : jQuery(document);
    $scope.find("select.select2").each(function () {
      var $select = jQuery(this);
      if ($select.data("select2")) {
        return;
      }
      $select.select2({
        width: "100%",
        dropdownParent: jQuery("#crudModal").length ? jQuery("#crudModal") : jQuery(document.body),
        placeholder: $select.attr("placeholder") || "Pilih data",
        allowClear: !$select.prop("required")
      });
    });
  }

  function initImageInputs(scope) {
    var root = scope || document;
    root.querySelectorAll('input[type="file"][accept*="image"]').forEach(function (input) {
      if (input.dataset.crudImagePreviewReady) {
        return;
      }
      input.dataset.crudImagePreviewReady = "1";

      input.addEventListener("change", function () {
        var file = input.files && input.files[0];
        if (!file || !file.type || file.type.indexOf("image/") !== 0) {
          return;
        }

        var preview = input.parentElement.querySelector(".crud-image-preview");
        if (!preview) {
          preview = document.createElement("div");
          preview.className = "crud-image-preview mt-2";
          input.insertAdjacentElement("beforebegin", preview);
        }
        preview.style.width = "56px";
        preview.style.height = "56px";
        preview.style.maxWidth = "56px";
        preview.style.maxHeight = "56px";
        preview.style.overflow = "hidden";

        preview.innerHTML = "";
        var image = document.createElement("img");
        image.alt = input.closest(".col-md-6")?.querySelector(".form-label")?.textContent || "Preview gambar";
        image.width = 56;
        image.height = 56;
        image.style.width = "56px";
        image.style.height = "56px";
        image.style.maxWidth = "56px";
        image.style.maxHeight = "56px";
        image.style.objectFit = "cover";
        image.src = URL.createObjectURL(file);
        image.onload = function () {
          URL.revokeObjectURL(image.src);
        };
        preview.appendChild(image);
      });
    });
  }

  function formatIndonesianNumber(value, integerOnly) {
    var cleaned = String(value || "")
      .replace(/[^0-9,.-]/g, "")
      .replace(/\s+/g, "");

    if (!cleaned) {
      return "";
    }

    var isNegative = cleaned.charAt(0) === "-";
    cleaned = cleaned.replace(/-/g, "");

    var decimalPart = "";
    if (!integerOnly && cleaned.indexOf(",") !== -1) {
      var parts = cleaned.split(",");
      cleaned = parts.shift();
      decimalPart = parts.join("").replace(/\D/g, "");
    }

    var wholePart = cleaned.replace(/\./g, "").replace(/\D/g, "");
    if (!wholePart) {
      wholePart = "0";
    }

    wholePart = wholePart.replace(/^0+(?=\d)/, "");
    wholePart = wholePart.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

    return (isNegative ? "-" : "") + wholePart + (decimalPart ? "," + decimalPart : "");
  }

  function initLocalizedNumbers(scope) {
    var root = scope || document;
    root.querySelectorAll('input[data-localized-number="true"]').forEach(function (input) {
      if (input.dataset.localizedNumberReady) {
        return;
      }
      input.dataset.localizedNumberReady = "1";

      var integerOnly = input.dataset.integerOnly === "true";
      if (input.value) {
        input.value = formatIndonesianNumber(input.value, integerOnly);
      }

      input.addEventListener("blur", function () {
        input.value = formatIndonesianNumber(input.value, integerOnly);
      });
    });
  }

  function initDatePickers(scope) {
    if (!window.flatpickr) {
      return;
    }

    var root = scope || document;
    root.querySelectorAll('input[data-date-picker="true"]').forEach(function (input) {
      if (input.dataset.datePickerReady) {
        return;
      }
      input.dataset.datePickerReady = "1";

      var wrapper = input.parentElement;
      if (!wrapper.classList.contains("crud-date-input")) {
        wrapper = document.createElement("div");
        wrapper.className = "input-group crud-date-input";
        input.insertAdjacentElement("beforebegin", wrapper);
        wrapper.appendChild(input);

        var button = document.createElement("button");
        button.type = "button";
        button.className = "btn btn-outline-secondary";
        button.setAttribute("aria-label", "Pilih tanggal");
        button.innerHTML = '<i class="ti ti-calendar"></i>';
        wrapper.appendChild(button);
      }

      var picker = flatpickr(input, {
        allowInput: true,
        dateFormat: "d/m/Y",
        clickOpens: true
      });

      var trigger = wrapper.querySelector("button");
      if (trigger) {
        trigger.addEventListener("click", function () {
          picker.open();
        });
      }
    });
  }

  function initCrudControls(scope) {
    initSelect2(scope);
    initImageInputs(scope);
    initLocalizedNumbers(scope);
    initDatePickers(scope);
  }

  document.addEventListener("show.bs.modal", function (event) {
    if (event.target.id !== "crudModal") {
      return;
    }

    var trigger = event.relatedTarget;
    var title = trigger ? trigger.getAttribute("data-crud-modal-title") : "";
    var titleEl = document.getElementById("crudModalLabel");
    var bodyEl = document.getElementById("crud-modal-body");

    if (title && titleEl) {
      titleEl.textContent = title;
    }

    if (bodyEl) {
      bodyEl.innerHTML = '<div class="crud-modal-loading"><div class="spinner-border text-primary" role="status"></div></div>';
    }
  });

  document.addEventListener("htmx:afterSwap", function (event) {
    initCrudControls(event.target);
  });

  document.body.addEventListener("crudSuccess", function (event) {
    var detail = event.detail || {};
    if (window.appToast) {
      window.appToast.show({
        level: detail.level || "success",
        title: detail.title || "Berhasil",
        message: detail.message || "Data berhasil disimpan."
      });
    }

    var modal = getCrudModal();
    if (modal) {
      modal.hide();
    }
    window.setTimeout(function () {
      window.location.reload();
    }, 900);
  });

  document.body.addEventListener("crudError", function (event) {
    var detail = event.detail || {};
    if (window.appToast) {
      window.appToast.show({
        level: detail.level || "error",
        title: detail.title || "Validasi gagal",
        message: detail.message || "Periksa kembali data yang diinput."
      });
    }

    initCrudControls(document.getElementById("crud-modal-body"));
  });

  document.addEventListener("DOMContentLoaded", function () {
    initCrudControls(document);
  });
})();
