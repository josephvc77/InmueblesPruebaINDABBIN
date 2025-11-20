# 📁 Estructura del Módulo CONDIA - Repositorio de Documentos

## 🎯 Descripción General

CONDIA es un módulo del sistema SIISEP diseñado como un **repositorio de documentos** para gestionar la documentación de inmuebles. El sistema está organizado en una estructura jerárquica de 3 niveles:

1. **Inmueble CONDIA** (Nivel Superior)
2. **Carpetas** (3 carpetas por inmueble)
3. **Documentos** (dentro de cada carpeta)

---

## 🏗️ Estructura de Datos

### 1. InmuebleCondia (Alta de Inmueble)

**Campos:**
- `nombre` (CharField): Nombre identificador del inmueble
- `descripcion` (TextField): Descripción detallada (opcional)
- `fecha_creacion` (DateTimeField): Fecha de creación automática
- `fecha_actualizacion` (DateTimeField): Última actualización automática
- `usuario_creador` (ForeignKey): Usuario que creó el inmueble
- `activo` (BooleanField): Estado del inmueble (True/False)

**Características:**
- Al crear un inmueble, se crean automáticamente las 3 carpetas
- Permite desactivar inmuebles sin eliminar los documentos

---

### 2. CarpetaCondia (Carpetas de Documentos)

**Tipos de Carpetas:**
1. **CARPETA_1**: Proceso de Arrendamiento
2. **CARPETA_2**: Documentación Legal y Técnica
3. **CARPETA_3**: Fundamento Legal

**Campos:**
- `inmueble` (ForeignKey): Inmueble al que pertenece
- `tipo_carpeta` (CharField): Tipo de carpeta (CARPETA_1, CARPETA_2, CARPETA_3)
- `fecha_creacion` (DateTimeField): Fecha de creación automática

**Características:**
- Cada inmueble tiene exactamente 3 carpetas (una de cada tipo)
- Las carpetas se crean automáticamente al crear el inmueble

---

### 3. DocumentoCondia (Documentos Individuales)

**Campos:**
- `carpeta` (ForeignKey): Carpeta a la que pertenece
- `codigo` (CharField): Código identificador (A, B, C, T.I, U.II, etc.)
- `nombre` (CharField): Nombre completo del documento
- `archivo` (FileField): Archivo del documento (PDF, DOC, etc.)
- `descripcion` (TextField): Descripción adicional (opcional)
- `fecha_subida` (DateTimeField): Fecha de subida automática
- `fecha_actualizacion` (DateTimeField): Última actualización automática
- `usuario_subio` (ForeignKey): Usuario que subió el documento

**Códigos por Carpeta:**

#### CARPETA 1 - Proceso de Arrendamiento:
- A: Solicitud de espacio o notificación a la UR
- B: Tabla de superficie máxima a ocupar por institución (SMOI)
- C: Justificación y autorización del arrendamiento ante el INDAABIN
- D: Solicitud de disponibilidad de inmuebles de propiedad federal y respuesta del INDAABIN
- E: Solicitud y/o autorización del arrendamiento (Oficialía Mayor)
- F: Notificación al propietario para arrendar el inmueble
- G: Solicitud de justipreciación de renta
- H: Notificación de pago de derechos del INDAABIN
- I: Dictamen de justipreciación de renta
- J: Oficio de revisión jurídica y respuesta
- K: Justificación plurianual
- L: Oficio de solicitud y registro obligacional (UAJ)
- M: Registro de contrato en página del INDAABIN
- N: Contrato de arrendamiento y convenios
- O: Notificación a la UR y Subdirección de Obras para la elaboración de los planos de adecuación de oficinas
- P: Anexo 1 al contrato de arrendamiento, acta-recepción del inmueble
- I_1: Inventario y las condiciones de instalaciones y equipos propios del inmueble, validado por la Subdirección de Obras
- II: Dictamen de seguridad estructural emitido por un Director Responsable del inmueble
- III: Usos permitidos y en general todas las limitaciones derivadas de las características del inmueble
- IV: Acta-Entrega de los trabajos de adecuación de oficinas a cargo de la Subdirección de obras
- Q: Anexo 2 al contrato de arrendamiento plano de distribución de personal (adecuación de oficinas autorizado)
- R: Oficio de notificación de disponibilidad del inmueble a la UR
- S: Actas-entrega de asignación de espacio a las Unidades Administrativas

#### CARPETA 2 - Documentación Legal y Técnica:
- T: Documentación legal
- T.I: Escritura del inmueble a arrendar (título de propiedad)
- T.II: Testimonio de la escritura pública que contenga el acta constitutiva de la empresa que tenga carácter de arrendador, tratándose de personas morales y Registro Público de la Propiedad y el Comercio
- T.III: Escritura de cambio de régimen (si es el caso)
- T.IV: Escritura pública que contenga el poder notarial de la persona que pretenda suscribir el contrato en representación del arrendado
- T.V: Cedula de identificación fiscal del arrendador, Registro Federal de Contribuyentes (RFC)
- T.VI: Identificación oficial vigente con fotografía y firma del arrendador o representante legal, credencial de elector (INE)
- T.VII: Comprobante de domicilio fiscal del arrendador
- U: Documentación técnica
- U.I: Planos Arquitectónicos
- U.II: Registro de la constancia de seguridad estructural expedida por el GCDMX
- U.III: Visto bueno de seguridad y operación expedida por el GCDMX
- U.IV: Última boleta por concepto de pago del inmueble predial
- U.V: Última boleta por concepto de suministro de agua potable
- U.VI: Último recibo por concepto de pago de servicio de energía eléctrica

#### CARPETA 3 - Fundamento Legal:
- FUNDAMENTO_LEGAL: Fundamento Legal

---

## 📂 Estructura de Archivos

```
condia/
├── models.py              # Modelos: InmuebleCondia, CarpetaCondia, DocumentoCondia
├── views.py               # Vistas para CRUD de inmuebles y documentos
├── forms.py               # Formularios para crear/editar
├── admin.py               # Configuración del admin de Django
├── urls.py                # (En djangocrud/urls.py)
└── templates/
    └── condia/
        ├── inicio.html                    # Pantalla principal (lista de inmuebles)
        ├── inmueble_create.html          # Crear nuevo inmueble
        ├── inmueble_detail.html          # Ver documentos de un inmueble
        ├── inmueble_edit.html            # Editar inmueble
        ├── inmueble_delete.html          # Eliminar inmueble
        ├── documento_create.html         # Agregar documento
        ├── documento_edit.html           # Editar documento
        └── documento_delete.html         # Eliminar documento
```

---

## 🔗 URLs del Sistema

### Autenticación:
- `/signinCondia/` - Inicio de sesión
- `/signupCondia/` - Registro de usuario
- `/logout_condia/` - Cerrar sesión

### Inmuebles:
- `/condia/` - Lista de inmuebles (Pantalla de inicio)
- `/condia/inmueble/nuevo/` - Crear nuevo inmueble
- `/condia/inmueble/<id>/` - Ver documentos de un inmueble
- `/condia/inmueble/<id>/editar/` - Editar inmueble
- `/condia/inmueble/<id>/eliminar/` - Eliminar inmueble

### Documentos:
- `/condia/carpeta/<carpeta_id>/documento/nuevo/` - Agregar documento
- `/condia/documento/<documento_id>/editar/` - Editar documento
- `/condia/documento/<documento_id>/eliminar/` - Eliminar documento

---

## 🚀 Flujo de Uso

### 1. Crear un Inmueble
1. Ir a `/condia/` (pantalla de inicio)
2. Clic en "Nuevo Inmueble"
3. Llenar nombre y descripción (opcional)
4. Guardar
5. **Automáticamente se crean las 3 carpetas**

### 2. Agregar Documentos
1. Seleccionar un inmueble de la lista
2. Se muestran 3 tabs (una por carpeta)
3. Seleccionar la carpeta deseada
4. Clic en "Agregar Documento"
5. Seleccionar código, nombre, archivo y descripción
6. Guardar

### 3. Gestionar Documentos
- **Ver**: Clic en el botón "Ver" del archivo
- **Editar**: Clic en el ícono de editar
- **Eliminar**: Clic en el ícono de eliminar (con confirmación)

---

## 🎨 Características de la Interfaz

### Pantalla de Inicio (`inicio.html`):
- Lista de tarjetas con todos los inmuebles activos
- Búsqueda por nombre o descripción
- Muestra: nombre, descripción, número de carpetas, número de documentos, fecha de creación
- Botones: Ver Documentos, Editar

### Detalle de Inmueble (`inmueble_detail.html`):
- Tabs para las 3 carpetas
- Tabla de documentos por carpeta
- Muestra: código, nombre, archivo, descripción
- Acciones: Ver archivo, Editar, Eliminar
- Botón para agregar nuevo documento

---

## 🔧 Configuración Técnica

### Permisos:
El sistema incluye permisos personalizados:
- `add_inmueble_condia`
- `change_inmueble_condia`
- `delete_inmueble_condia`
- `view_inmueble_condia`

### Archivos:
Los archivos se guardan en:
- `media/condia/documentos/` - Todos los documentos

### Base de Datos:
- **InmuebleCondia**: Tabla principal
- **CarpetaCondia**: Tabla de carpetas (relación 1:N con InmuebleCondia)
- **DocumentoCondia**: Tabla de documentos (relación 1:N con CarpetaCondia)

---

## 📝 Próximos Pasos

1. **Ejecutar migraciones:**
   ```bash
   python manage.py makemigrations condia
   python manage.py migrate
   ```

2. **Crear superusuario** (si no existe):
   ```bash
   python manage.py createsuperuser
   ```

3. **Acceder al sistema:**
   - Ir a `/signinCondia/`
   - Iniciar sesión
   - Ir a `/condia/` para ver la pantalla de inicio

---

## ✅ Ventajas de esta Estructura

1. **Normalizada**: Estructura de base de datos profesional
2. **Escalable**: Fácil agregar nuevos tipos de documentos
3. **Organizada**: Separación clara por carpetas
4. **Flexible**: Permite múltiples documentos del mismo tipo si es necesario
5. **Auditable**: Registra quién y cuándo se crearon/modificaron los documentos
6. **Mantenible**: Código limpio y bien organizado

---

## 📞 Soporte

Para cualquier duda o problema, revisar:
- Los modelos en `condia/models.py`
- Las vistas en `condia/views.py`
- Los templates en `condia/templates/condia/`

¡El sistema está listo para usar! 🚀

