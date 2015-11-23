<?php

include 'includes.php';

$quote_conn = new SQLite3($DATABASE_FOLDER . 'quotes.sqlite3'); 
$catalog_conn = new SQLite3($DATABASE_FOLDER . 'catalog.sqlite3');  

if ($_GET['type'] == 'quote_poem_sentences') { 

    $query = 'SELECT DISTINCT cyrus_sentence_n FROM quotes WHERE is_good = 1 ORDER BY 1;';

    $result = $quote_conn->query($query);

    $n = 0;

    echo '[';

    while ($row = $result->fetchArray()) {
        echo $row['cyrus_sentence_n'] . ',';
        
        $n = $n + 1;
    }

    echo ']';
} 

if ($_GET['type'] == 'sentences') { 

    $queryA = 'SELECT DISTINCT cyrus_sentence_n FROM quotes;';

    $resultA = $quote_conn->query($queryA);

    echo '<table><tr><th>Sentence N</th><th># of quotes</th></tr>';

    while ($rowA = $resultA->fetchArray()) {

        $n_minus_1 = 0;
        $n_zero = 0;
        $n_plus_1 = 0;
        
        $queryB = 'SELECT count(*) as n FROM quotes WHERE cyrus_sentence_n = ' . $rowA['cyrus_sentence_n']. ' AND is_good = -1;';
        $resultB = $quote_conn->query($queryB);
        while ($rowB = $resultB->fetchArray()) {
            $n_minus_1 = $rowB['n'];
            break;
        }
        
        $queryB = 'SELECT count(*) as n FROM quotes WHERE cyrus_sentence_n = ' . $rowA['cyrus_sentence_n']. ' AND is_good = 0;';
        $resultB = $quote_conn->query($queryB);
        while ($rowB = $resultB->fetchArray()) {
            $n_zero = $rowB['n'];
            break;
        }
        
        $queryB = 'SELECT count(*) as n FROM quotes WHERE cyrus_sentence_n = ' . $rowA['cyrus_sentence_n']. ' AND is_good = 1;';
        $resultB = $quote_conn->query($queryB);
        while ($rowB = $resultB->fetchArray()) {
            $n_plus_1 = $rowB['n'];
            break;
        }
        
        echo '<tr><td><a href="quotes.html?type=sentences&cyrus_sentence_n=' . $rowA['cyrus_sentence_n'] . '">' . $rowA['cyrus_sentence_n'] . '</a></td><td>' . $n_minus_1 . '</td><td>' . $n_zero . '</td><td>' . $n_plus_1 . '</td></tr>';
    }

    echo '</table>';
} 

if ($_GET['type'] == 'sources') {

    $query = 'SELECT other_file_name, count(*) as n FROM quotes GROUP BY 1 ORDER BY 1;';

    $result = $quote_conn->query($query);

    $n = 0;

    echo '<table><tr><th>file id</th><th>author</th><th>title</th><th># of quotes</th></tr>';

    while ($row = $result->fetchArray()) {

        $pg_file_id = str_replace('_txt.xml', '.xml', $row['other_file_name']);
        $pg_file_id = str_replace('_', '-', $pg_file_id);
        $author = '';
        $title = '';

        $query_b = 'SELECT author, title FROM catalog WHERE file_id = "' . $pg_file_id . '";';    

        $result_b = $catalog_conn->query($query_b);

        while ($row_b = $result_b->fetchArray()) {
            $author = $row_b['author'];
            $title = $row_b['title'];
            break;
        } 

        echo '<tr><td><a href="quotes.html?type=sources&other_file_name=' . $row['other_file_name'] . '">' . $row['other_file_name'] . '</a></td><td>' . $author . '</td><td><i>' . $title . '</i></td><td>' . $row['n'] . '</td></tr>';
        
        $n = $n + 1;
    }

    echo '</table>';
    
    echo '<br/><p>number of sources: ' . $n . '</p>';
}


?>
