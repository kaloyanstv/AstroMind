<?php
// login.php
header('Content-Type: application/json');

// Get data from the frontend (AJAX request)
$data = json_decode(file_get_contents("php://input"), true);
$username = $data['username'];
$password = $data['password'];

// Database connection
$servername = 'aws-0-eu-central-1.pooler.supabase.com';
$dbUsername = 'postgres.jvilzwfbaenvjwztsflq';
$dbPassword = 'AstroMind123';
$dbName = 'postgres';
$dbPort = 6543;  // Make sure the port is an integer or string, no extra spaces.

// Create connection with port included correctly
$conn = new mysqli($servername, $dbUsername, $dbPassword, $dbName, $dbPort);

// Check for connection error
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Query the database to check if the user exists
$sql = "SELECT * FROM users WHERE username = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $username);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows > 0) {
    $user = $result->fetch_assoc();

    // Verify password
    if (password_verify($password, $user['password'])) {
        // Success: valid user
        echo json_encode(["success" => true]);
    } else {
        // Invalid password
        echo json_encode(["success" => false]);
    }
} else {
    // No such user exists
    echo json_encode(["success" => false]);
}

$stmt->close();
$conn->close();
?>

