<?php
/**
 * Kontaktformular der FWG Oelde.
 * Nimmt POST-Daten entgegen, prüft sie und verschickt sie per E-Mail. Es werden keine Daten gespeichert.
 */
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

$cfg = require __DIR__ . '/config.php';

function respond(int $code, string $msg, array $extra = []): never {
    http_response_code($code);
    echo json_encode(['ok' => $code < 300, 'message' => $msg] + $extra, JSON_UNESCAPED_UNICODE);
    exit;
}
function clean(string $v, int $max): string {
    $v = trim(preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $v) ?? '');
    return mb_substr($v, 0, $max);
}
function single_line(string $v): string { return trim(preg_replace('/\s+/u', ' ', $v) ?? ''); }

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') respond(405, 'Nur POST erlaubt.');

// Herkunft prüfen (Schutz gegen Fremdformulare)
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin !== '') {
    $own = $cfg['allowed_origin'] ?: ((($_SERVER['HTTPS'] ?? '') !== '' && $_SERVER['HTTPS'] !== 'off' ? 'https://' : 'http://') . ($_SERVER['HTTP_HOST'] ?? ''));
    if (rtrim($origin, '/') !== rtrim($own, '/')) respond(403, 'Anfrage nicht erlaubt.');
}

// Honeypot und Zeitprüfung
if (clean((string)($_POST['website'] ?? ''), 200) !== '') respond(200, 'Danke für Ihre Nachricht!'); // Bots stillschweigend ignorieren
$ts = (int)($_POST['ts'] ?? 0);
if ($ts <= 0 || (time() - intdiv($ts, 1000)) < (int)$cfg['min_seconds']) respond(400, 'Bitte versuchen Sie es noch einmal.');

// Rate-Limit pro IP (nur gehashte IP im Temp-Verzeichnis)
$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$rl = sys_get_temp_dir() . '/fwg_rl_' . hash('sha256', $ip . 'fwg-oelde');
$hits = is_file($rl) ? array_filter(array_map('intval', file($rl, FILE_IGNORE_NEW_LINES) ?: []), fn($t) => $t > time() - 3600) : [];
if (count($hits) >= (int)$cfg['max_per_hour']) respond(429, 'Zu viele Nachrichten. Bitte versuchen Sie es später erneut.');

// Felder
$name = single_line(clean((string)($_POST['name'] ?? trim(($_POST['vorname'] ?? '') . ' ' . ($_POST['nachname'] ?? ''))), 120));
$email = single_line(clean((string)($_POST['email'] ?? ''), 200));
$phone = single_line(clean((string)($_POST['phone'] ?? ''), 50));
$topic = single_line(clean((string)($_POST['topic'] ?? ''), 80));
$message = clean((string)($_POST['message'] ?? ''), 5000);
$privacy = ($_POST['privacy'] ?? '') === '1';
$form = single_line(clean((string)($_POST['form'] ?? 'kontakt'), 30));

$errors = [];
if ($name === '') $errors['name'] = 'Bitte geben Sie Ihren Namen an.';
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors['email'] = 'Bitte geben Sie eine gültige E-Mail-Adresse an.';
if ($form === 'kontakt' && mb_strlen($message) < 5) $errors['message'] = 'Bitte schreiben Sie uns eine Nachricht.';
if (!$privacy) $errors['privacy'] = 'Bitte stimmen Sie der Datenschutzerklärung zu.';
if ($errors) respond(422, 'Bitte prüfen Sie Ihre Eingaben.', ['errors' => $errors]);

// Mail
$subject = $cfg['site_name'] . ': ' . ($form === 'mitmachen' ? 'Anfrage Mitmachen' : 'Kontaktformular') . ' von ' . $name;
$body = "Neue Nachricht über die Website\n\n"
      . "Formular: $form\nName: $name\nE-Mail: $email\n"
      . ($phone !== '' ? "Telefon: $phone\n" : '')
      . ($topic !== '' ? "Anliegen: $topic\n" : '')
      . "\nNachricht:\n" . ($message !== '' ? $message : '(keine)') . "\n";
$headers = [
    'From' => $cfg['site_name'] . ' Website <' . $cfg['from'] . '>',
    'Reply-To' => $name !== '' ? '"' . str_replace(['"', '\\'], '', $name) . '" <' . $email . '>' : $email,
    'MIME-Version' => '1.0',
    'Content-Type' => 'text/plain; charset=UTF-8',
    'X-Mailer' => 'FWG-Oelde-Website',
];
$encSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
$sent = mail($cfg['to'], $encSubject, $body, $headers);

if (!$sent) {
    if ($cfg['log_file']) @file_put_contents($cfg['log_file'], date('c') . " mail() fehlgeschlagen ($form)\n", FILE_APPEND);
    respond(500, 'Die Nachricht konnte nicht versendet werden. Bitte schreiben Sie uns direkt an ' . $cfg['to'] . '.');
}
$hits[] = time();
@file_put_contents($rl, implode("\n", $hits));
respond(200, 'Vielen Dank! Ihre Nachricht ist bei uns angekommen. Wir melden uns bald bei Ihnen.');
