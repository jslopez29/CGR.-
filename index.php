<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte Novedades de Procesos</title>
</head>
<body>

<?php
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

    // Mostrar sección para "Novedades Corrupción"
    echo "<h1>Novedades Corrupción</h1>";

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
        
        echo "<br><br>"; // Agregar un salto de línea adicional después de cada entrada
    }

    // Mostrar sección para "Novedades Regalías"
    echo "<h1>Novedades Regalías</h1>";

    // Reemplace 'NovedadesCGR' con el nombre real de su tabla
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
        
        echo "<br><br>"; // Agregar un salto de línea adicional después de cada entrada
    }
} catch (PDOException $e) {
    echo "Error: " . $e->getMessage();
}
?>

</body>
</html>
