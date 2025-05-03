<?php

$filename = 'forum.txt';

// POST-Anfrage: Beitrag speichern
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $username = $_POST["username"];
    $message = $_POST["message"];
    $timestamp = date("Y-m-d H:i:s");

    if ($username && $message) {
        $entry = json_encode(["username" => $username, 
        "message" => $message, 
        "timestamp" => $timestamp]) . PHP_EOL;
        file_put_contents($filename, $entry, FILE_APPEND);
        echo json_encode(["success" => true]);
        exit;
    }
}


// GET-Anfrage: Beiträge aus txtDatei lesen
if ($_SERVER["REQUEST_METHOD"] === "GET") {
    $posts = [];
    if (file_exists($filename)) {
        $lines = file($filename, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        foreach ($lines as $line) {
            $posts[] = json_decode($line, true);
        }
    }
    echo json_encode($posts);
    exit;
}
?>
