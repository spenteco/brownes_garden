<?php

include 'includes.php';

$conn = new SQLite3($DATABASE_FOLDER . 'poems.sqlite3'); 

$query = 'SELECT width, height, source_files, poem_json FROM poems WHERE start_time = ' . $_GET['start_time'] . ' AND poem_type = "' . $_GET['poem_type'] . '" AND poem_number = ' . $_GET['poem_number'] . ';';

$result = $conn->query($query); 

while ($row = $result->fetchArray()) {
  echo '["' . $row['width'] . '","' . $row['height'] . '",' . json_encode($row['source_files']) . ',' . json_encode($row['poem_json']) . ']';
}

?>
