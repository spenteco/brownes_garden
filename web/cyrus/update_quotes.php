<?php

include 'includes.php';

$quote_conn = new SQLite3($DATABASE_FOLDER . 'quotes.sqlite3');

$is_good = 0;

if ($_GET['value'] == '-1') {
    $is_good = -1;
}
if ($_GET['value'] == '+1') {
    $is_good = 1;
}

$query = 'UPDATE quotes SET is_good = ' . $is_good . ' WHERE ROWID = ' . $_GET['n'] . ';';

echo $query;

$result = $quote_conn->query($query);

echo 'OK';

?>
