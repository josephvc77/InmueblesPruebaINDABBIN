// Función para cargar las entidades federativas en el campo select
function loadEntidadesFederativas() {
    $.getJSON('/get_entidades_federativas/', function(data) {
      var selectEntidades = $('#{{ form.entidad_federativa.auto_id }}');
      selectEntidades.empty();
      $.each(data.entidades_federativas, function(index, value) {
        // Verificar si el valor de entidad_federativa coincide con el valor actual del campo
        var selected = value === '{{ form.instance.entidad_federativa }}' ? 'selected' : '';
        selectEntidades.append($('<option>').text(value).attr('value', value).prop('selected', selected));
      });
      loadMunicipios(selectEntidades.val()); // Cargamos los municipios correspondientes a la entidad seleccionada
    });
  }

  // Función para cargar los municipios en el campo select
  function loadMunicipios(entidadFederativa) {
    $.getJSON('/get_municipios/' + entidadFederativa + '/', function(data) {
      var selectMunicipios = $('#{{ form.municipio_alcaldia.auto_id }}');
      selectMunicipios.empty();
      $.each(data.municipios, function(index, value) {
        // Verificar si el valor de municipio_alcaldia coincide con el valor actual del campo
        var selected = value === '{{ form.instance.municipio_alcaldia }}' ? 'selected' : '';
        selectMunicipios.append($('<option>').text(value).attr('value', value).prop('selected', selected));
      });
    });
  }

  // Función para cargar los datos al cargar la página
  $(document).ready(function() {
    loadEntidadesFederativas(); // Cargamos las entidades federativas
    $('#{{ form.entidad_federativa.auto_id }}').change(function() {
      loadMunicipios($(this).val()); // Cargamos los municipios al cambiar la entidad federativa seleccionada
    });
  });