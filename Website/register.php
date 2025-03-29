<?php
// register.php
header('Content-Type: application/json');

// Enable error reporting for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Get data from the frontend (AJAX request)
$data = json_decode(file_get_contents("php://input"), true);

if (!$data || !isset($data['username']) || !isset($data['password'])) {
    echo json_encode(["success" => false, "message" => "Invalid input data"]);
    exit;
}

$username = trim($data['username']);
$password = trim($data['password']);

// Validate input
if (empty($username) || empty($password)) {
    echo json_encode(["success" => false, "message" => "Username and password are required"]);
    exit;
}

// Hash the password securely
$hashedPassword = password_hash($password, PASSWORD_DEFAULT);

// Database connection details
$servername = 'aws-0-eu-central-1.pooler.supabase.com';
$dbUsername = 'postgres.jvilzwfbaenvjwztsflq';
$dbPassword = 'AstroMind123';
$dbName = 'postgres';
$dbPort = 6543; // Make sure this port is correct

// Create connection with port included
$conn = new mysqli($servername, $dbUsername, $dbPassword, $dbName, $dbPort);

// Check for connection error
if ($conn->connect_error) {
    echo json_encode(["success" => false, "message" => "Database connection failed: " . $conn->connect_error]);
    exit;
}

// Check if username exists
$sql = "SELECT * FROM users WHERE username = ?";
$stmt = $conn->prepare($sql);
if (!$stmt) {
    echo json_encode(["success" => false, "message" => "SQL error: " . $conn->error]);
    exit;
}

$stmt->bind_param("s", $username);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows > 0) {
    echo json_encode(["success" => false, "message" => "Username already exists"]);
} else {
    // Insert new user
    $insertSql = "INSERT INTO users (username, password) VALUES (?, ?)";
    $stmtInsert = $conn->prepare($insertSql);

    if (!$stmtInsert) {
        echo json_encode(["success" => false, "message" => "SQL Insert Error: " . $conn->error]);
        exit;
    }

    $stmtInsert->bind_param("ss", $username, $hashedPassword);

    if ($stmtInsert->execute()) {
        echo json_encode(["success" => true, "message" => "User registered successfully"]);
    } else {
        echo json_encode(["success" => false, "message" => "Registration failed: " . $stmtInsert->error]);
    }

    $stmtInsert->close();
}

$stmt->close();
$conn->close();
?>

