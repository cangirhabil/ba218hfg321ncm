
<?php
// create db connection
$conn=new mysqli("db","user","password","db");
if($conn->connect_error) {
    die("connection failed");
   }

?>