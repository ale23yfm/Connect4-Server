<?php
$sock = socket_create(AF_INET,SOCK_STREAM,0);
if (!socket_connect($sock, "127.0.0.1", 5988)) {
    die("connect failed: " . socket_strerror(socket_last_error($sock)) . "\n");
}
while (true) {
    $n = socket_recv($sock, $buf, 2048, 0);
    if ($n === false || $n === 0) {
        break;
    }
    echo $buf . "\n";

    if (strpos($buf, "Game over") !== false) {
        break;
    }

    echo "> ";
    $line = fgets(STDIN);
    if ($line === false) {
        break;
    }

    $line = trim($line);
    if ($line === "") {
        $line = " ";
    }
    socket_send($sock, $line, strlen($line), 0);
}

socket_close($sock);