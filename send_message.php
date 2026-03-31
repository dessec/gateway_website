<?php
// send_message.php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize input
    $name = htmlspecialchars(strip_tags($_POST['name']));
    $email = htmlspecialchars(strip_tags($_POST['email']));
    $phone = isset($_POST['phone']) ? htmlspecialchars(strip_tags($_POST['phone'])) : 'Not Provided';
    $message = htmlspecialchars(strip_tags($_POST['message']));

    // Target email requested by user
    $to = 'gatewaydetecting@hotmail.com';
    
    // Exact subject requested by user
    $subject = '[Customer Message]';
    
    // Format email body
    $body = "Name: $name\n";
    $body .= "Email: $email\n";
    $body .= "Phone: $phone\n\n";
    $body .= "Message:\n$message\n";

    // Build headers
    $headers = "From: no-reply@gatewaymetaldetectors.com\r\n";
    $headers .= "Reply-To: $email\r\n";
    
    // Headers required to flag the email as urgent (Red Exclamation Mark in Hotmail/Outlook)
    $headers .= "X-Priority: 1 (Highest)\r\n";
    $headers .= "X-MSMail-Priority: High\r\n";
    $headers .= "Importance: High\r\n";

    // Send email via PHP mail()
    if (mail($to, $subject, $body, $headers)) {
        // Redirect back to contact page with success parameter
        header("Location: pages/contact.html?success=true");
        exit;
    } else {
        // Fallback error
        echo "Error: Unable to send email. Please try again later or contact $to directly.";
    }
} else {
    // If not POST, redirect back to contact
    header("Location: pages/contact.html");
    exit;
}
?>
