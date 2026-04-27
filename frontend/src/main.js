import './style.css'

// URL Dinámica para producción vs local
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
  ? 'http://127.0.0.1:8000/api' 
  : '/api';
// Elementos del DOM
const tablaLibros = document.querySelector('#tabla-libros tbody');
const tablaUsuarios = document.querySelector('#tabla-usuarios tbody');
const tablaPrestamos = document.querySelector('#tabla-prestamos tbody');

// Inicializar data
document.addEventListener('DOMContentLoaded', () => {
  cargarLibros();
  cargarUsuarios();
  cargarPrestamos();
});

// ========================
// 📚 GESTIÓN DE LIBROS
// ========================
async function cargarLibros() {
  try {
    const res = await fetch(`${API_URL}/libros`);
    const data = await res.json();
    renderLibros(data.libros);
  } catch (error) {
    console.error('Error cargando libros:', error);
  }
}

let currentLibros = [];
let showingAllBooks = false;

function renderLibros(libros) {
  currentLibros = libros;
  tablaLibros.innerHTML = '';
  let displayBooks = libros;
  const btnVerMas = document.getElementById('btn-ver-mas-libros');

  if (!showingAllBooks && libros.length > 5) {
    displayBooks = libros.slice(0, 5);
    if(btnVerMas) {
        btnVerMas.style.display = 'inline-block';
        btnVerMas.textContent = 'Ver más libros';
    }
  } else {
    if(btnVerMas) {
        if (libros.length > 5) {
            btnVerMas.style.display = 'inline-block';
            btnVerMas.textContent = 'Ver menos libros';
        } else {
            btnVerMas.style.display = 'none';
        }
    }
  }

  displayBooks.forEach(lib => {
    const autores = lib.autores.map(a => a.nombre_aut).join(', ');
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${lib.codigo_lib}</td>
      <td><strong>${lib.nombre_lib}</strong></td>
      <td>${lib.editorial?.nombre_edi || 'N/A'}</td>
      <td>${autores || 'N/A'}</td>
      <td><button class="accion-btn" onclick="abrirModalEdicionLibro(${lib.codigo_lib}, '${lib.nombre_lib.replace(/'/g, "\\'")}', '${(lib.editorial?.nombre_edi || '').replace(/'/g, "\\'")}', '${autores.replace(/'/g, "\\'")}')">Editar</button></td>
    `;
    tablaLibros.appendChild(tr);
  });
}

document.getElementById('btn-ver-mas-libros')?.addEventListener('click', () => {
  showingAllBooks = !showingAllBooks;
  renderLibros(currentLibros);
});

document.getElementById('form-libro').addEventListener('submit', async (e) => {
  e.preventDefault();
  const libro = {
    codigo: parseInt(document.getElementById('lib-cod').value),
    titulo: document.getElementById('lib-tit').value,
    editorial_nombre: document.getElementById('lib-edi').value,
    autores_nombres: [document.getElementById('lib-aut').value]
  };

  try {
    await fetch(`${API_URL}/libros`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(libro)
    });
    cargarLibros();
    e.target.reset();
  } catch (error) {
    alert('Error al registrar libro');
  }
});

// Búsqueda en BST
document.getElementById('btn-buscar-lib').addEventListener('click', async () => {
  const cod = document.getElementById('buscar-lib-cod').value;
  if (!cod) return cargarLibros(); // Mostrar todos si está vacío

  try {
    const res = await fetch(`${API_URL}/buscar?codigo=${cod}`);
    if (!res.ok) throw new Error();
    const data = await res.json();
    renderLibros([data.libro]);
  } catch (error) {
    alert('Libro no encontrado en el BST');
    tablaLibros.innerHTML = '<tr><td colspan="4">No se encontraron resultados</td></tr>';
  }
});

// ========================
// 👤 GESTIÓN DE USUARIOS
// ========================
async function cargarUsuarios() {
  try {
    const res = await fetch(`${API_URL}/usuarios`);
    const data = await res.json();
    tablaUsuarios.innerHTML = '';
    data.usuarios.forEach(usu => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${usu.codigo_usu}</td>
        <td><strong>${usu.nombre_usu}</strong></td>
        <td>${usu.direccion_usu}</td>
        <td>${usu.telefono_usu}</td>
        <td><button class="accion-btn" onclick="abrirModalEdicionUsuario(${usu.codigo_usu}, '${usu.nombre_usu.replace(/'/g, "\\'")}', '${usu.direccion_usu.replace(/'/g, "\\'")}', '${usu.telefono_usu.replace(/'/g, "\\'")}')">Editar</button></td>
      `;
      tablaUsuarios.appendChild(tr);
    });
  } catch (error) {
    console.error('Error cargando usuarios:', error);
  }
}

document.getElementById('form-usuario').addEventListener('submit', async (e) => {
  e.preventDefault();
  const usuario = {
    codigo: parseInt(document.getElementById('usu-cod').value),
    nombre: document.getElementById('usu-nom').value,
    direccion: document.getElementById('usu-dir').value,
    telefono: document.getElementById('usu-tel').value
  };

  try {
    await fetch(`${API_URL}/usuarios`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(usuario)
    });
    cargarUsuarios();
    e.target.reset();
  } catch (error) {
    alert('Error al registrar usuario');
  }
});

// ========================
// 🔄 GESTIÓN DE PRÉSTAMOS
// ========================
async function cargarPrestamos() {
  try {
    const res = await fetch(`${API_URL}/prestamos`);
    const data = await res.json();
    tablaPrestamos.innerHTML = '';
    data.prestamos.forEach(p => {
      const tr = document.createElement('tr');
      const f1 = new Date(p.fecha_pres).toLocaleDateString();
      const f3 = p.fecha_ent_real ? new Date(p.fecha_ent_real).toLocaleDateString() : '-';

      const isActivo = p.estado === 'ACTIVO';
      const estadoClase = isActivo ? 'estado-activo' : 'estado-devuelto';

      // Días en mora viene del backend
      let diasMora = p.dias_en_mora || 0;

      const librosText = p.libros.map(l => l.nombre_lib).join(' | ');

      tr.innerHTML = `
        <td>#${p.numero_pres}</td>
        <td>Usu ${p.codigo_usu}</td>
        <td>${f1}</td>
        <td>${f3}</td>
        <td class="${estadoClase}">${p.estado}</td>
        <td>$${p.valor_multa}</td>
        <td>${diasMora}</td>
        <td style="font-size: 0.8rem">${librosText}</td>
        <td>
          ${isActivo ? `<button class="accion-btn btn-devolver" onclick="devolver(${p.numero_pres})">Devolver</button>` : '✔️'}
          <button class="accion-btn" onclick="abrirModalEdicionPrestamo(${p.numero_pres}, ${diasMora})">Editar</button>
        </td>
      `;
      tablaPrestamos.appendChild(tr);
    });
  } catch (error) {
    console.error('Error cargando préstamos:', error);
  }
}

document.getElementById('form-prestamo').addEventListener('submit', async (e) => {
  e.preventDefault();
  // Validar formato libros
  const codigosRaw = document.getElementById('pres-libs').value;
  const arr = codigosRaw.split(',').map(v => parseInt(v.trim()));

  const pres = {
    codigo_usuario: parseInt(document.getElementById('pres-usu').value),
    codigos_libros: arr,
    fecha_pres: document.getElementById('pres-fecha').value
  };

  try {
    const res = await fetch(`${API_URL}/prestamos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(pres)
    });
    if (!res.ok) throw new Error(await res.text());
    cargarPrestamos();
    e.target.reset();
  } catch (error) {
    alert('Error: ' + error.message);
  }
});

// Función global para devolver 
window.devolver = async function (id) {
  try {
    const res = await fetch(`${API_URL}/prestamos/devolver/${id}`, { method: 'POST' });
    if (!res.ok) {
      const data = await res.json();
      throw new Error(data.detail);
    }
    cargarPrestamos();
  } catch (error) {
    alert('Error al devolver: ' + error.message);
  }
}

// ========================
// ✏️ LÓGICA DE EDICIÓN
// ========================

window.cerrarModal = function(id) {
  document.getElementById(id).classList.add('hidden');
}

window.abrirModalEdicionLibro = function(cod, tit, edi, aut) {
  document.getElementById('edit-lib-cod').value = cod;
  document.getElementById('edit-lib-tit').value = tit;
  document.getElementById('edit-lib-edi').value = edi;
  document.getElementById('edit-lib-aut').value = aut;
  document.getElementById('modal-editar-libro').classList.remove('hidden');
}

document.getElementById('form-edit-libro').addEventListener('submit', async (e) => {
  e.preventDefault();
  const cod = document.getElementById('edit-lib-cod').value;
  const libroData = {
    titulo: document.getElementById('edit-lib-tit').value,
    editorial_nombre: document.getElementById('edit-lib-edi').value,
    autores_nombres: document.getElementById('edit-lib-aut').value.split(',').map(a => a.trim())
  };
  try {
    const res = await fetch(`${API_URL}/libros/${cod}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(libroData)
    });
    if (!res.ok) throw new Error();
    cerrarModal('modal-editar-libro');
    cargarLibros();
  } catch (err) {
    alert('Error al editar libro');
  }
});

window.abrirModalEdicionUsuario = function(cod, nom, dir, tel) {
  document.getElementById('edit-usu-cod').value = cod;
  document.getElementById('edit-usu-nom').value = nom;
  document.getElementById('edit-usu-dir').value = dir;
  document.getElementById('edit-usu-tel').value = tel;
  document.getElementById('modal-editar-usuario').classList.remove('hidden');
}

document.getElementById('form-edit-usuario').addEventListener('submit', async (e) => {
  e.preventDefault();
  const cod = document.getElementById('edit-usu-cod').value;
  const usuData = {
    nombre: document.getElementById('edit-usu-nom').value,
    direccion: document.getElementById('edit-usu-dir').value,
    telefono: document.getElementById('edit-usu-tel').value
  };
  try {
    const res = await fetch(`${API_URL}/usuarios/${cod}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(usuData)
    });
    if (!res.ok) throw new Error();
    cerrarModal('modal-editar-usuario');
    cargarUsuarios();
  } catch (err) {
    alert('Error al editar usuario');
  }
});

window.abrirModalEdicionPrestamo = function(num, mora) {
  document.getElementById('edit-pres-num').value = num;
  document.getElementById('edit-pres-mora').value = mora;
  document.getElementById('modal-editar-prestamo').classList.remove('hidden');
}

document.getElementById('form-edit-prestamo').addEventListener('submit', async (e) => {
  e.preventDefault();
  const num = document.getElementById('edit-pres-num').value;
  const presData = {
    dias_en_mora: parseInt(document.getElementById('edit-pres-mora').value)
  };
  try {
    const res = await fetch(`${API_URL}/prestamos/${num}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(presData)
    });
    if (!res.ok) throw new Error();
    cerrarModal('modal-editar-prestamo');
    cargarPrestamos();
  } catch (err) {
    alert('Error al editar préstamo');
  }
});
