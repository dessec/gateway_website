<?php
header('Content-Type: application/json');

// Check if request is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'error' => 'Invalid request method.']);
    exit;
}

$lat = isset($_POST['lat']) ? floatval($_POST['lat']) : null;
$lng = isset($_POST['lng']) ? floatval($_POST['lng']) : null;
$desc = isset($_POST['desc']) ? trim($_POST['desc']) : '';

if (!$lat || !$lng || empty($desc) || !isset($_FILES['photo']) || $_FILES['photo']['error'] !== UPLOAD_ERR_OK) {
    echo json_encode(['success' => false, 'error' => 'Missing required fields or valid file upload.']);
    exit;
}

// Validate file type
$fileType = mime_content_type($_FILES['photo']['tmp_name']);
$allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];

if (!in_array($fileType, $allowedTypes)) {
    echo json_encode(['success' => false, 'error' => 'Invalid file type. Only JPG, PNG, and GIF are allowed.']);
    exit;
}

// Ensure unique filename
$extension = pathinfo($_FILES['photo']['name'], PATHINFO_EXTENSION);
$filename = uniqid('find_') . '.' . $extension;
$uploadDir = __DIR__ . '/uploads/';

// Create directory if it doesn't exist
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0755, true);
}

$destination = $uploadDir . $filename;

if (move_uploaded_file($_FILES['photo']['tmp_name'], $destination)) {
    $dataFile = __DIR__ . '/pins.json';

    // Read and lock file
    $pins = [];
    if (file_exists($dataFile)) {
        $json = file_get_contents($dataFile);
        if ($json) {
            $pins = json_decode($json, true) ?: [];
        }
    }

    $newPin = [
        'lat' => $lat,
        'lng' => $lng,
        'desc' => htmlspecialchars($desc),
        'img' => 'uploads/' . $filename,
        'date' => date('c')
    ];

    $pins[] = $newPin;

    // Save securely
    if (file_put_contents($dataFile, json_encode($pins, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT), LOCK_EX) !== false) {
        echo json_encode(['success' => true, 'pin' => $newPin]);
    }
    else {
        echo json_encode(['success' => false, 'error' => 'Failed to write to database.']);
    }
}
else {
    echo json_encode(['success' => false, 'error' => 'Failed to save uploaded file.']);
}
