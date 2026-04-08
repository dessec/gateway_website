<?php
// send_message.php
session_start();

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require 'phpmailer/Exception.php';
require 'phpmailer/PHPMailer.php';
require 'phpmailer/SMTP.php';

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

    $mail = new PHPMailer(true);

    try {
        // Server settings
        $mail->isSMTP();
        
        // TODO: Replace with your actual SMTP server details
        $mail->Host       = 'smtp.hostinger.com'; // e.g. smtp.hostinger.com
        $mail->SMTPAuth   = true;
        
        // IMPORTANT: Enter your SMTP username (usually your full email address)
        $mail->Username   = 'no-reply@gatewaymetaldetectors.com';
        
        // IMPORTANT: Enter your SMTP password
        $mail->Password   = 'YOUR_EMAIL_PASSWORD_HERE';
        
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS; // Enable TLS encryption, `ssl` also accepted
        $mail->Port       = 465; // TCP port to connect to

        // Recipients
        $mail->setFrom('no-reply@gatewaymetaldetectors.com', 'Gateway Metal Detectors'); // Domain-based FROM address
        $mail->addAddress($to); // Add a recipient

        // Reply-To field correctly set to the visitor's email
        $mail->addReplyTo($email, $name);

        // Content
        $mail->isHTML(false); // Set email format to plain text
        $mail->Subject = $subject;
        $mail->Body    = $body;
        
        // Headers to flag as urgent
        $mail->addCustomHeader('X-Priority', '1 (Highest)');
        $mail->addCustomHeader('X-MSMail-Priority', 'High');
        $mail->addCustomHeader('Importance', 'High');

        $mail->send();
        
        // Redirect back to contact page with success parameter
        header("Location: pages/contact.html?success=true");
        exit;
    } catch (Exception $e) {
        // Fallback error
        echo "Error: Unable to send email. Mailer Error: {$mail->ErrorInfo}";
    }
} else {
    // If not POST, redirect back to contact
    header("Location: pages/contact.html");
    exit;
}
?>
