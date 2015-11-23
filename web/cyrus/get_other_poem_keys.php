<?php

include 'includes.php';

$conn = new SQLite3($DATABASE_FOLDER . 'other_poems.sqlite3'); 

$query = 'SELECT start_time, poem_type, poem_number FROM poems WHERE poem_type = "' . $_GET['type'] . '" ORDER BY 1, 2, 3;';

$result = $conn->query($query); 

echo '[';

while ($row = $result->fetchArray()) {
  echo '["' . $row['start_time'] . '","' . $row['poem_type'] . '","' . $row['poem_number'] . '"],';
}

echo ']';

?>
