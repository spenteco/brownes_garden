<?php

include 'includes.php';

$catalog_conn = new SQLite3($DATABASE_FOLDER . 'catalog.sqlite3');  

$query = 'SELECT file_id, author, title FROM catalog;';    

$result = $catalog_conn->query($query);

$output = array();

while ($row = $result->fetchArray()) {
    
    $file_id = $row['file_id'];
    if ($file_id == 'Song' || $file_id == 'Gen' || $file_id == 'Neh') {
        $file_id = $file_id . '.xml';
    }
    if ($file_id == 'Psalms') {
        $file_id = 'Ps.xml';
    }
    
    array_push($output, [$file_id, $row['author'], $row['title']]);
} 

echo json_encode($output);

?>
