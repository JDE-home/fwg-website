<?php
// Einstellungen für das Kontaktformular – hier anpassen.
return [
    'to'        => 'info@fwg-oelde.de',     // Empfänger der Nachrichten
    'from'      => 'noreply@fwg-oelde.de',  // Absender: muss zur Domain des Hostings gehören (SPF/DKIM)
    'site_name' => 'FWG Oelde',
    'min_seconds' => 3,                     // Mindestzeit zwischen Seitenaufruf und Absenden (Bot-Schutz)
    'max_per_hour' => 5,                    // Nachrichten pro IP und Stunde
    'allowed_origin' => '',                 // optional, z. B. 'https://www.fwg-oelde.de'; leer = gleiche Domain
    'log_file' => '',                       // optional: Pfad für Fehlerprotokoll (ohne Nachrichteninhalt)
];
