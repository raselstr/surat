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
    initSelect2(event.target);
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

    initSelect2(document.getElementById("crud-modal-body"));
  });

  document.addEventListener("DOMContentLoaded", function () {
    initSelect2(document);
  });
})();
