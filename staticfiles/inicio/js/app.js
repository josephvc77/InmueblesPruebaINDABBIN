function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  sidebar.classList.toggle("active");
}


// // Función para activar el modo oscuro
// function activarModoOscuro() {
//   // Agrega una clase al elemento body para aplicar estilos de modo oscuro
//   document.body.classList.add('dark-mode');
  
//   // Almacena la preferencia en el almacenamiento local del navegador
//   localStorage.setItem('modoOscuro', 'activado');
// }

// // Función para desactivar el modo oscuro
// function desactivarModoOscuro() {
//   // Remueve la clase dark-mode del elemento body
//   document.body.classList.remove('dark-mode');
  
//   // Almacena la preferencia en el almacenamiento local del navegador
//   localStorage.setItem('modoOscuro', 'desactivado');
// }

// // Verifica la preferencia almacenada en el almacenamiento local al cargar la página
// window.addEventListener('load', function() {
//   const modoOscuro = localStorage.getItem('modoOscuro');
//   if (modoOscuro === 'activado') {
//     activarModoOscuro();
//   }
// });

// // Maneja el clic en el botón para cambiar entre modo oscuro y modo claro
// const botonModoOscuro = document.getElementById('modoOscuroBtn');
// botonModoOscuro.addEventListener('click', function() {
//   if (document.body.classList.contains('dark-mode')) {
//     desactivarModoOscuro();
//   } else {
//     activarModoOscuro();
//   }
// });


// // Mostrar la animación de carga antes de cargar la página
// document.getElementById("loader-container").style.display = "block";

// // Ocultar la animación de carga después de que la página esté completamente cargada
// window.onload = function() {
// document.getElementById("loader-container").style.display = "none";
// };

