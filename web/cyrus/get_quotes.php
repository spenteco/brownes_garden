<?php

include 'includes.php';

$quote_conn = new SQLite3($DATABASE_FOLDER . 'quotes.sqlite3'); 
$catalog_conn = new SQLite3($DATABASE_FOLDER . 'catalog.sqlite3'); 
 

if ($_GET['type'] == 'quote_poem_sentences') { 

    $values_for_client = array();

    $query = 'SELECT DISTINCT cyrus_sentence FROM quotes where cyrus_sentence_n = "' . $_GET['cyrus_sentence_n'] . '" AND is_good = 1;';

    $result = $quote_conn->query($query);

    while ($row = $result->fetchArray()) {
        array_push($values_for_client, $row['cyrus_sentence']);
    }

    $matching_sentences = array();

    $query = 'SELECT other_file_name, other_sentence_n, other_sentence, match_lemmas FROM quotes where cyrus_sentence_n = "' . $_GET['cyrus_sentence_n'] . '" AND is_good = 1 ORDER BY 4 DESC, 1 ASC, 2 ASC;';

    $result = $quote_conn->query($query);

    while ($row = $result->fetchArray()) {

        $pg_file_id = str_replace('_txt.xml', '.xml', $row['other_file_name']);
        $pg_file_id = str_replace('_', '-', $pg_file_id);
        $pg_file_id = str_replace('PG-', 'PG_', $pg_file_id);
        if ($pg_file_id == 'Song.xml' || $pg_file_id == 'Gen.xml' || $pg_file_id == 'Neh.xml' || $pg_file_id == 'Ps.xml') {
            $pg_file_id = str_replace('.xml', '', $pg_file_id);
        }
    
        $author = $pg_file_id;
        $title = $pg_file_id;

        $query_b = 'SELECT author, title FROM catalog WHERE file_id = "' . $pg_file_id . '";';    

        $result_b = $catalog_conn->query($query_b);

        while ($row_b = $result_b->fetchArray()) {
            $author = $row_b['author'];
            $title = $row_b['title'];
            break;
        }

        array_push($matching_sentences, array($row['other_sentence'], $author, $title, $row['other_file_name'], $row['other_sentence_n']));
    }

    array_push($values_for_client, $matching_sentences, '<p class="other_sentence_source"><span class="author"> Browne, Thomas, Sir.</span> <span class="title">The garden of Cyrus, or the quincunciall, lozenge, or net-work plantations of the ancients, artificially, naturally, mystically considered.</span></p>');

    echo json_encode($values_for_client);
} 

if ($_GET['type'] == 'sentences') { 

    $query = 'SELECT cyrus_sentence FROM quotes where cyrus_sentence_n = "' . $_GET['cyrus_sentence_n'] . '";';

    $result = $quote_conn->query($query);

    while ($row = $result->fetchArray()) {
        echo '<div class="cyrus_sentence_div"><p class="cyrus_sentence">' . $row['cyrus_sentence'] . '</p><button type="button" onclick="javascript:mark_sentence_bogus(\'' . $_GET['cyrus_sentence_n'] . '\');">BOGUS</button> <button type="button" onclick="javascript:next_sentence(\'' . $_GET['cyrus_sentence_n'] . '\');">Next</button> <a href="/cyrus/quotes.html?type=sentences">List</a><br/></div>';
        break;
    }

    echo '<div class="other_sentences_div">'; 
    
    $query = 'SELECT other_file_name, other_sentence_n, other_sentence, match_lemmas, is_good, ROWID as n FROM quotes where cyrus_sentence_n = "' . $_GET['cyrus_sentence_n'] . '" ORDER BY 5 DESC, 1 ASC, 2 ASC;';

    $result = $quote_conn->query($query);

    echo '<table>';

    while ($row = $result->fetchArray()) {

        $is_good_minus_1 = '';
        $is_good_0 = '';
        $is_good_plus_1 = '';

        if ($row['is_good'] == -1) {
            $is_good_minus_1 = ' checked="checked" ';
        }

        if ($row['is_good'] == 0) {
            $is_good_0 = ' checked="checked" ';
        }

        if ($row['is_good'] == 1) {
            $is_good_plus_1 = ' checked="checked" ';
        }

        echo '<tr><td class="radio_buttons"><input type="radio" name="goodness' . $row['n'] . '" n="' . $row['n'] . '"  value="-1"' . $is_good_minus_1 . '> -1 <input type="radio" name="goodness' . $row['n'] . '" n="' . $row['n'] . '"  value="0"' . $is_good_0 . '> 0 <input type="radio" name="goodness' . $row['n'] . '" n="' . $row['n'] . '" value="+1"' . $is_good_plus_1 . '> +1 </td><td>';

        echo '<p class="other_sentence">' . $row['other_sentence'] . ' ' . $row['match_lemmas'] . '</p>';

        $pg_file_id = str_replace('_txt.xml', '.xml', $row['other_file_name']);
        $pg_file_id = str_replace('_', '-', $pg_file_id);
        
        if (strpos($row['other_file_name'], 'PG_') === False) {
        }
        else {
            $pg_file_id = str_replace('_txt.xml', '.xml', $row['other_file_name']);
        }
        
        if (strpos($row['other_file_name'], 'Ecclesiaties') === False &&
            strpos($row['other_file_name'], 'Psalms') === False &&
            strpos($row['other_file_name'], 'Gen') === False &&
            strpos($row['other_file_name'], 'Neh') === False &&
            strpos($row['other_file_name'], 'Song') === False) {
        }
        else {
            $pg_file_id = str_replace('_txt.xml', '', $row['other_file_name']);
        }
        
        $author = '';
        $title = '';

        $query_b = 'SELECT author, title FROM catalog WHERE file_id = "' . $pg_file_id . '";';    

        $result_b = $catalog_conn->query($query_b);

        while ($row_b = $result_b->fetchArray()) {
            $author = $row_b['author'];
            $title = $row_b['title'];
            break;
        }

        echo '<p class="other_sentence_details">' . $row['other_file_name'] . ' ' . $row['other_sentence_n'] . '; ' . $author . ' <i>' . $title . '</i></p>';

        echo '</td></tr>';
    }

    echo '</table>';

    echo '</div>';
} 

if ($_GET['type'] == 'sources') {

    $pg_file_id = str_replace('_txt.xml', '.xml', $_GET['other_file_name']);
    $pg_file_id = str_replace('_', '-', $pg_file_id);
    $author = '';
    $title = '';

    $last_cyrus_sentence_n = -1;

    $query_b = 'SELECT author, title FROM catalog WHERE file_id = "' . $pg_file_id . '";';    

    $result_b = $catalog_conn->query($query_b);

    while ($row_b = $result_b->fetchArray()) {
        $author = $row_b['author'];
        $title = $row_b['title'];
        break;
    }

    echo '<p class="source_heading">' . $author . ' <i>' . $title . '</i></p>';

    $query = 'SELECT cyrus_sentence_n, cyrus_sentence, other_sentence_n, other_sentence, match_lemmas FROM quotes where other_file_name = "' . $_GET['other_file_name'] . '" ORDER BY 1, 2;';

    $result = $quote_conn->query($query);

    while ($row = $result->fetchArray()) {

        if ($row['cyrus_sentence_n'] != $last_cyrus_sentence_n) {

            echo '<p class="cyrus_sentence">' . $row['cyrus_sentence_n'] . ' ' . $row['cyrus_sentence'] . '</p>';
            $last_cyrus_sentence_n = $row['cyrus_sentence_n'];
        }

        echo '<p class="other_sentence">' . $row['other_sentence_n'] . ' ' .  $row['other_sentence'] . ' ' . $row['match_lemmas'] . '</p>';
    }
}


?>
