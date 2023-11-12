<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MySQL Data Display</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }

        table {
            border-collapse: collapse;
            width: 100%;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>

<?php
// Replace with your actual database credentials
$host = 'juansebastianlopez.com';
$user = 'jslo_cgrhost';
$password = '&$r6W6&qGnMG';
$database = 'jslo_cgr';

try {
    $conn = new PDO("mysql:host=$host;dbname=$database", $user, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Replace 'NovedadesCGR' with your actual table name
    $stmt = $conn->prepare("SELECT * FROM NovedadesCGR");
    $stmt->execute();
    $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

    if (count($result) > 0) {
        echo "<table>";
        echo "<tr><th>ID</th><th>Estado_ID</th><th>DAY</th><th>MONTH</th><th>YEAR</th><th>Novedades</th><th>Link</th></tr>";
        foreach ($result as $row) {
            echo "<tr>";
            echo "<td>{$row['id']}</td>";
            echo "<td>{$row['Estado_ID']}</td>";
            echo "<td>{$row['DAY']}</td>";
            echo "<td>{$row['MONTH']}</td>";
            echo "<td>{$row['YEAR']}</td>";
            echo "<td>{$row['Novedades']}</td>";
            echo "<td>{$row['Link']}</td>";
            echo "</tr>";
        }
        echo "</table>";
    } else {
        echo "No data found.";
    }
} catch (PDOException $e) {
    echo "Error: " . $e->getMessage();
}
?>

</body>
</html>
