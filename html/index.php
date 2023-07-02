<?php
    require_once("config.php");

    // POSTリクエスト以外をはじく
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        header("HTTP/1.1 405 Method Not Allowed");
        exit;
    }

    header('Content-Type: application/json; charset=UTF-8');
    
    // 入力チェック
    $latitude = $_POST["latitude"];
    if ($latitude == "") {
        throw new ValueError("Missing required parameter latitude");
    }

    $longitude = $_POST["longitude"];
    if ($longitude == "") {
        throw new ValueError("Missing required parameter longitude");
    }

    $limit = $_POST["limit"];
    if ($limit == "") {
        throw new ValueError("Missing required parameter limit");
    }

    $tourism_info_list = find_tourism_info($latitude, $longitude, $limit);
    print json_encode($tourism_info_list, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);


    function find_tourism_info($latitude, $longitude, $limit)
    {
        $tourism_info_list = fetch_tourism_info();

        // 距離を計算して、観光情報に追加する
        foreach ($tourism_info_list as &$tourism_info) {
            $distance = calculate_distance($latitude, $longitude, $tourism_info['latitude'], $tourism_info['longitude']);
            $tourism_info = array_merge($tourism_info, array('distance' => $distance));
        }

        // 距離順にソートする
        $ids = array_column($tourism_info_list, 'distance');
        array_multisort($ids, SORT_ASC, $tourism_info_list);

        // limit分だけスライスして返す
        return array_slice($tourism_info_list, 0, $limit);
    }

    function fetch_tourism_info()
    {
        global $dsn, $user, $password; // defined at "config.php"

        $dbh = new PDO($dsn, $user, $password);
        $dbh -> setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        $sql = 'SELECT * FROM tourism_info';

        $stmt = $dbh -> prepare($sql);
        $stmt -> execute();

        $tourism_info_list = $stmt -> fetchAll(PDO::FETCH_ASSOC);
        $dbh = null;

        return $tourism_info_list;
    }

    function calculate_distance($latitude1, $longitude1, $latitude2, $longitude2)
    {
        $r = 6371.137; // 赤道半径 (km)
        return $r * acos(
            sin($latitude1 * pi() / 180) * sin($latitude2 * pi() / 180)
          + cos($latitude1 * pi() / 180) * cos($latitude2 * pi() / 180)
          * cos($longitude2 * pi() / 180 - $longitude1 * pi() / 180)
        );
    }
?>
