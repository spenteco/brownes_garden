<?php

include 'includes.php';

$conn = new SQLite3($DATABASE_FOLDER . 'other_poems.sqlite3'); 

$query = 'SELECT source_files, poem_json FROM poems WHERE start_time = ' . $_GET['start_time'] . ' AND poem_type = "' . $_GET['poem_type'] . '" AND poem_number = "' . $_GET['poem_number'] . '";';

//echo $query . '<br/>';

$result = $conn->query($query); 

while ($row = $result->fetchArray()) {
  echo '[' . $row['source_files'] . ',' . $row['poem_json'] . ']';
}

?>
