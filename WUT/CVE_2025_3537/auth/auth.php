<?php
session_start();
$host="db";
$username="user";
$pass="password";
$db="db";

$conn=mysqli_connect($host,$username,$pass,$db);
if(!$conn){
	die("Database connection error");
}


if(!isset($_SESSION['auth']))
{	
header('Location:../login.php');	
}
?>
