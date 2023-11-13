<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Informe de novedades de procesos para la Unidad de Investigaciones Especiales Contra la Corrupción y el Grupo Interno de Trabajo para la Responsabilidad Fiscal de los Recursos del Sistema General de Regalías.">
    <meta name="keywords" content="Novedades, Corrupción, Regalías, Responsabilidad Fiscal, Procesos">
    <meta name="robots" content="index, follow">

    <!-- Canonical Tag (replace 'canonical-url' with the actual URL) -->
    <link rel="canonical" href="canonical-url">

    <title>Informe de Novedades de Procesos</title>
</head>
<body>

<header>
    <h1>Informe de Novedades de Procesos</h1>
    <p>El reporte de Estados inicia desde el viernes 10 de noviembre de 2023.</p>
</header>

<section>
    <article>
        <h2>Novedades Unidad Investigaciones Especiales Contra la Corrupción</h2>
        <?php
        // Reemplace con sus credenciales reales de la base de datos
        require_once 'config/config.php';

        // Función para obtener el nombre del mes en español
        function getSpanishMonthName($numeroMes) {
            $nombresMes = [
                'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
            ];
            return $nombresMes[$numeroMes - 1]; // Ajustar el índice ya que los meses son 1-based
        }

        try {
            $conn = new PDO("mysql:host=" . DB_HOST . ";dbname=" . DB_NAME, DB_USER, DB_PASSWORD);
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

            // Reemplace 'NovedadesCGR' con el nombre real de su tabla
            $stmt = $conn->prepare("SELECT * FROM NovedadesCGR WHERE CONTRALORIA = 1");
            $stmt->execute();
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

            foreach ($result as $row) {
                $nombreMes = getSpanishMonthName($row['MONTH']);
                echo "<strong>Estado:</strong> {$row['Estado_ID']} del {$row['DAY']} de $nombreMes de {$row['YEAR']}<br>";
                echo "<strong>Los siguientes procesos presentaron Novedades:</strong><br>";

                // Utilice nl2br para reemplazar saltos de línea con etiquetas <br>
                $novedadesFormateadas = nl2br($row['Novedades']);
                echo $novedadesFormateadas;

                echo "<br>";

                // Agregar el enlace "Consultar Estado" con el link de la entrada en la base de datos
                echo "<a href='{$row['Link']}' target='_blank'>Consultar Estado</a>";

                echo "<br><br>"; // Agregar un salto de línea adicional después de cada entrada
            }
        } catch (PDOException $e) {
            echo "Error: " . $e->getMessage();
        }
        ?>
    </article>

    <article>
        <h2>Novedades Grupo Interno de Trabajo para la Responsabilidad Fiscal de los Recursos del Sistema General de Regalías</h2>
        <?php
        // Reemplace 'NovedadesCGR' con el nombre real de su tabla
        try {
            $stmt = $conn->prepare("SELECT * FROM NovedadesCGR WHERE CONTRALORIA = 2");
            $stmt->execute();
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

            foreach ($result as $row) {
                $nombreMes = getSpanishMonthName($row['MONTH']);
                echo "<strong>Estado:</strong> {$row['Estado_ID']} del {$row['DAY']} de $nombreMes de {$row['YEAR']}<br>";
                echo "<strong>Los siguientes procesos presentaron Novedades:</strong><br>";

                // Utilice nl2br para reemplazar saltos de línea con etiquetas <br>
                $novedadesFormateadas = nl2br($row['Novedades']);
                echo $novedadesFormateadas;

                echo "<br>";

                // Agregar el enlace "Consultar Estado" con el link de la entrada en la base de datos
                echo "<a href='{$row['Link']}' target='_blank'>Consultar Estado</a>";

                echo "<br><br>"; // Agregar un salto de línea adicional después de cada entrada
            }
        } catch (PDOException $e) {
            echo "Error: " . $e->getMessage();
        }
        ?>
    </article>
</section>

<footer>
    <!-- Add any footer content here -->
</footer>

</body>
</html>
