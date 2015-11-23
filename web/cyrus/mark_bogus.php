<?php

include 'includes.php';

$quote_conn = new SQLite3($DATABASE_FOLDER . 'quotes.sqlite3');

$query = 'UPDATE quotes SET is_good = -1 WHERE cyrus_sentence_n = ' . $_GET['sentence_n'] . ';';

echo $query;

$result = $quote_conn->query($query);

echo 'OK';

?>
