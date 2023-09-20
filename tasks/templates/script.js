$(document).ready(function () {
    initializeFormFields();
    initializeDeleteButtons('.delete-expediente-cedoc-btn', 'expediente cedoc');
    initializeDeleteButtons('.delete-folio-real-btn', 'Folio');
    initializeDeleteButtons('.delete-numero-plano-btn', 'No. Plano');
    initializeTabs();
  });
  
  function initializeFormFields() {
    $('#{{ form.entidad_federativa.auto_id }}').change(function () {
      loadMunicipios($(this).val());
    });
  }
  
  function initializeDeleteButtons(buttonSelector, entityName) {
    $(buttonSelector).click(function () {
      const url = $(this).data('url');
      const confirmationMessage = `¿Estás seguro de que deseas eliminar este ${entityName}?`;
  
      showConfirmationDialog(confirmationMessage, () => {
        fetch(url, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': '{{ csrf_token }}',
          },
        })
          .then(response => response.json())
          .then(data => {
            if (data.success) {
              const row = $(this).closest('tr');
              row.remove();
            } else {
              console.error(`Error al eliminar ${entityName}`);
            }
          })
          .catch(error => {
            console.error(`Error al eliminar el ${entityName}:`, error);
          });
      });
    });
  }
  
  function initializeTabs() {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
  
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetTab = tab.dataset.tab;
        tabs.forEach(tab => tab.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(targetTab).classList.add('active');
      });
    });
  }
  
  function showConfirmationDialog(message, callback) {
    Swal.fire({
      title: '¿Estás seguro?',
      text: message,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#dc3545',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Sí',
      cancelButtonText: 'Cancelar',
    }).then(result => {
      if (result.isConfirmed) {
        callback();
      }
    });
  }
  
  function showNotification(title, text, icon) {
    Swal.fire({
      title: title,
      text: text,
      icon: icon,
      timer: 3000,
      showConfirmButton: false,
    });
  }
  