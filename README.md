<div align="center">

<img src="https://upload.wikimedia.org/wikipedia/en/thumb/a/ae/Los_Pollos_Hermanos_logo.png/220px-Los_Pollos_Hermanos_logo.png" width="500" />

# Sistema Los Pollos Hermanos

</div>

## Para empezar

### ¿Que es?
Los Pollos Hermanos es una aplicación diseñada para simplificar el proceso de generación de órdenes de compra en cualquier tipo de negocio. Con una interfaz intuitiva y fácil de usar, esta aplicación permite a los usuarios crear órdenes de compra de manera rápida y eficiente mediante la cumplimentación de un formulario personalizable

### Justificación
Muchas empresas todavía dependen de métodos manuales o sistemas desactualizados para generar órdenes de compra, lo que puede ser lento, propenso a errores y poco eficiente. Nuestro sistema ofrece una solución automatizada y digital que agiliza todo el proceso

### Instalación

1. Abre una terminal o CMD:

   Inicia una terminal en tu sistema operativo. Puedes usar Terminal en macOS/Linux o CMD/Powershell en Windows.

2. Clona el repositorio

   ```sh
   git clone https://github.com/jorojasj/sistema-facturacion.git
   ```

3. Navega a la carpeta del proyecto:
   ```sh
   cd sistema-facturación
   ```

4. Instala los requerimientos

   ```sh
   pip install -r requirements.txt
   ```

5. Ejecuta el servidor de desarrollo

   ```sh
   python manage.py runserver
   ```
6. Accede a la aplicación:
   Abre tu navegador de preferencia y visita http://127.0.0.1:8000 para ver la aplicación en funcionamiento.

## Uso
    - Accede a la aplicación en tu navegador web en http://127.0.0.1:8000
    - Inicia sesión con las credenciales Usuario: admin, Contraseña: admin .
    - Navega a la sección de órdenes de compra.
    - Completa el formulario para crear una nueva orden de compra.
    - Guarda y revisa tus órdenes de compra en la sección correspondiente.

## Tecnologias Utilizadas

    -Django: Framework

    -Bootstrap: Para estilos

    -SQLite: Base de Datos

## Contribución
    -Haz un fork del proyecto.
    -Crea una nueva rama (git checkout -b nombre-rama).
    -Realiza tus cambios y haz commits (git commit -m 'Añadir nueva funcionalidad').
    -Sube tu rama (git push origin nombre-rama).
    -Abre un Pull Request.
