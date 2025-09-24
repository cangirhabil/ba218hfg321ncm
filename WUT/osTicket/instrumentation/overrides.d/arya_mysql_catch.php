<?php

##########################################################################################
#                                    mysqli overrides                                    #
##########################################################################################

function check_query($query_str){
    global $DML_detected;
    $query = preg_replace("/\s+/", "", $query_str);
    $crud = array(
        "insert",
        "update",
        "delete",
        "create",
        "drop",
        "alter",
        "truncate"
    );
    foreach ($crud as $key) {
        $result = stripos($query, $key);
        if ($result !== false) {
            if ($result == 0) {
                $DML_detected = true;
                return true;
            }
        }
    }
    $DML_detected = false;
    return false;
}

uopz_set_return(
    'mysqli_query',
    function ($mysql, $query, $result_mode = MYSQLI_STORE_RESULT) {
        try {
            $result = mysqli_query($mysql, $query, $result_mode);
            $the_exception = null;
        }catch(Throwable $e) {
            $result = false;
            $the_exception = $e;
        }
        $is_detected = check_query($query);
        if (($result === false) or ($is_detected===true)){
            if($the_exception) {
                $errno = -1;
                $errstr = $the_exception->getMessage();
            }elseif ($is_detected===true){
                $errno = -9999;
                $errstr = "We detect DDL or DML query";
            }else {
                $errno = mysqli_errno($mysql);
                $errstr = mysqli_error($mysql);
            }
            $json = json_encode(
                [
                    'function' => 'mysqli_query',
                    'params' => [$query],
                    'errno' => $errno,
                    'errstr' => $errstr,
                ]
            );
            __fuzzer_file_put_contents(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", $json . "\n", FILE_APPEND);
            chmod(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", 0777);
            if($the_exception != null) {
                throw $the_exception;
            }
        }
        return $result;
    },
    true
);

uopz_set_return(
    'mysqli',
    'query',
    function ($query, $result_mode = MYSQLI_STORE_RESULT) {
        mysqli_report(MYSQLI_REPORT_ALL ^ MYSQLI_REPORT_STRICT);
        try{
            $result = $this->query($query, $result_mode);
            $the_exception = null;
        }catch(Throwable $e) {
            $result = false;
            $the_exception = $e;
        }
        $is_detected = check_query($query);
        if (($result === false) or ($is_detected===true)){
            if($the_exception) {
                $errno = -1;
                $errstr = $the_exception->getMessage();
            }elseif ($is_detected===true){
                $errno = -9999;
                $errstr = "We detect DDL or DML query";
            } else {
                $errno = $this->errno;
                $errstr = $this->error;
            }
            $json = json_encode(
                [
                    'function' => 'mysqli::query',
                    'params' => [$query],
                    'errno' => $errno,
                    'errstr' => $errstr,
                ]
            );
            __fuzzer_file_put_contents(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", $json . "\n", FILE_APPEND);
            chmod(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", 0777);
            if($the_exception != null) {
                throw $the_exception;
            }
        }
        return $result;
    },
    true
);

uopz_set_return(
    'mysqli_stmt_prepare',
    function ($mysql, $query) {
        mysqli_report(MYSQLI_REPORT_ALL ^ MYSQLI_REPORT_STRICT);
        try{
            $result = mysqli_stmt_prepare($mysql,$query);
            $the_exception = null;
        }catch(Throwable $e) {
            $result = false;
            $the_exception = $e;
        }
        $is_detected = check_query($query);
        if (($result === false) or ($is_detected===true)){
            if($the_exception) {
                $errno = -1;
                $errstr = $the_exception->getMessage();
            }elseif ($is_detected===true){
                $errno = -9999;
                $errstr = "We detect DDL or DML query";
            } else {
                $errno = mysqli_errno($mysql);
                $errstr = mysqli_error($mysql);
            }
            $json = json_encode(
                [
                    'function' => 'mysqli_stmt_prepare',
                    'params' => [$query],
                    'errno' => $errno,
                    'errstr' => $errstr,
                ]
            );
            __fuzzer_file_put_contents(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", $json . "\n", FILE_APPEND);
            chmod(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", 0777);
            if($the_exception != null) {
                throw $the_exception;
            }
        }
        return $result;
    },
    true
);

uopz_set_return(
    'mysqli_stmt',
    'prepare',
    function ($query) {
        mysqli_report(MYSQLI_REPORT_ALL ^ MYSQLI_REPORT_STRICT);
        try{
            $result = $this->prepare($query);
            $the_exception = null;
        }catch(Throwable $e) {
            $result = false;
            $the_exception = $e;
        }
        $is_detected = check_query($query);
        if (($result === false) or ($is_detected===true)){
            if($the_exception) {
                $errno = -1;
                $errstr = $the_exception->getMessage();
            }elseif ($is_detected===true){
                $errno = -9999;
                $errstr = "We detect DDL or DML query";
            } else {
                $errno = $this->errno;
                $errstr = $this->error;
            }
            $json = json_encode(
                [
                    'function' => 'mysqli_stmt::prepare',
                    'params' => [$query],
                    'errno' => $errno,
                    'errstr' => $errstr,
                ]
            );
            __fuzzer_file_put_contents(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", $json . "\n", FILE_APPEND);
            chmod(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", 0777);
            if($the_exception != null) {
                throw $the_exception;
            }
        }
        return $result;
    },
    true
);

uopz_set_return(
    'mysqli_prepare',
    function ($mysql, $query) {
        mysqli_report(MYSQLI_REPORT_ALL ^ MYSQLI_REPORT_STRICT);
        try{
            $result = mysqli_prepare($mysql,$query);
            $the_exception = null;
        }catch(Throwable $e) {
            $result = false;
            $the_exception = $e;
        }
        $is_detected = check_query($query);
        if (($result === false) or ($is_detected===true)){
            if($the_exception) {
                $errno = -1;
                $errstr = $the_exception->getMessage();
            }elseif ($is_detected===true){
                $errno = -9999;
                $errstr = "We detect DDL or DML query";
            } else {
                $errno = mysqli_errno($mysql);
                $errstr = mysqli_error($mysql);
            }
            $json = json_encode(
                [
                    'function' => 'mysqli_prepare',
                    'params' => [$query],
                    'errno' => $errno,
                    'errstr' => $errstr,
                ]
            );
            __fuzzer_file_put_contents(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", $json . "\n", FILE_APPEND);
            chmod(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", 0777);
            if($the_exception != null) {
                throw $the_exception;
            }
        }
        return $result;
    },
    true
);

uopz_set_return(
    'mysqli',
    'prepare',
    function ($query) {
        mysqli_report(MYSQLI_REPORT_ALL ^ MYSQLI_REPORT_STRICT);
        try{
            $result = $this->prepare($query);
            $the_exception = null;
        }catch(Throwable $e) {
            $result = false;
            $the_exception = $e;
        }
        $is_detected = check_query($query);
        if (($result === false) or ($is_detected===true)){
            if($the_exception) {
                $errno = -1;
                $errstr = $the_exception->getMessage();
            }elseif ($is_detected===true){
                $errno = -9999;
                $errstr = "We detect DDL or DML query";
            } else {
                $errno = $this->errno;
                $errstr = $this->error;
            }
            $json = json_encode(
                [
                    'function' => 'mysqli::prepare',
                    'params' => [$query],
                    'errno' => $errno,
                    'errstr' => $errstr,
                ]
            );
            __fuzzer_file_put_contents(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", $json . "\n", FILE_APPEND);
            chmod(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", 0777);
            if($the_exception != null) {
                throw $the_exception;
            }
        }
        return $result;
    },
    true
);

uopz_set_return(
    'mysqli_stmt_bind_param',
    function ($mysql, $types, &$var, &...$vars) {
        global $DML_detected;
        mysqli_report(MYSQLI_REPORT_ALL ^ MYSQLI_REPORT_STRICT);
        try{
            $result = mysqli_stmt_bind_param($mysql, $types, $var, ...$vars);
            $the_exception = null;
        }catch(Throwable $e) {
            $result = false;
            $the_exception = $e;
        }

        // $msg = $var;
        $msg = " | " . $var;
        foreach ($vars as $n) {
            $msg = $msg . " | " . $n;
        }

        // $is_detected = true;
        $is_detected = $DML_detected;
        if (($result === false) or ($is_detected===true)){
            if($the_exception) {
                $errno = -1;
                $errstr = $the_exception->getMessage();
            }elseif ($is_detected===true){
                $errno = -9999;
                $errstr = "We detect BIND PARAM query";
            } else {
                $errno = mysqli_errno($mysql);
                $errstr = mysqli_error($mysql);
            }
            $json = json_encode(
                [
                    'function' => 'mysqli_stmt_bind_param',
                    'params' => [$msg],
                    'errno' => $errno,
                    'errstr' => $errstr,
                ]
            );
            __fuzzer_file_put_contents(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", $json . "\n", FILE_APPEND);
            chmod(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", 0777);
            if($the_exception != null) {
                throw $the_exception;
            }
        }
        return $result;
    },
    true
);

uopz_set_return(
    'mysqli_stmt',
    'bind_param',
    function ($types, &$var, &...$vars){
        global $DML_detected;
        mysqli_report(MYSQLI_REPORT_ALL ^ MYSQLI_REPORT_STRICT);
        try{
            if (is_null($this)){
                $result = null;
            }else{
                $result = $this->bind_param($types, $var, ...$vars);
                $the_exception = null;
            }
        }catch(Throwable $e) {
            $result = false;
            $the_exception = $e;
        }
        $msg = " | " . $var;
        foreach ($vars as $n) {
            $msg = $msg . " | " . $n;
        }

        $is_detected = $DML_detected;
        if (($result === false) or ($is_detected===true)){
            if($the_exception) {
                $errno = -1;
                $errstr = $the_exception->getMessage() . $the_exception->getTraceAsString();
            }elseif ($is_detected===true){
                $errno = -9999;
                $errstr = "We detect BIND PARAM query";
            } else {
                $errno = $this->errno;
                $errstr = $this->error;
            }
            $json = json_encode(
                [
                    'function' => 'mysqli_stmt::bind_param',
                    'params' => [$msg],
                    'errno' => $errno,
                    'errstr' => $errstr,
                ]
            );
            __fuzzer_file_put_contents(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", $json . "\n", FILE_APPEND);
            chmod(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", 0777);
            if($the_exception != null) {
                throw $the_exception;
            }
        }
        return $result;
    },
    true
);

uopz_set_return(
    'PDOStatement',
    'execute',
    function ($params = null) {
        global $DML_detected;
        $query = $this->queryString;
        mysqli_report(MYSQLI_REPORT_ALL ^ MYSQLI_REPORT_STRICT);
        try{
            $result = $this->execute($params);
            $the_exception = null;
        }catch(Throwable $e) {
            $result = false;
            $the_exception = $e;
        }
        $is_detected = check_query($query);
        if ($params != null) {
            foreach ($params as $key => $val) {
                $query = $query . " | " .$key. " => " .$val;
            }
        }
        if (($result === false) or ($is_detected===true) or ($DML_detected===true)){
            if($the_exception) {
                $errno = -1;
                $errstr = $the_exception->getMessage();
            }elseif ($DML_detected===true){
                $errno = -9999;
                $errstr = "We detect DDL or DML query";
            } else {
                $errno = $this->errorCode();
                $errstr = $this->errorInfo();
            }
            $DML_detected = false;
            $json = json_encode(
                [
                    'function' => 'PDOStatement::execute',
                    'params' => [$query],
                    'errno' => $errno,
                    'errstr' => $errstr,
                ]
            );
            __fuzzer_file_put_contents(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", $json . "\n", FILE_APPEND);
            chmod(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", 0777);
            if($the_exception != null) {
                throw $the_exception;
            }
        }
        return $result;
    },
    true
);

uopz_set_return(
    'PDOStatement',
    'bindValue',
    function ($param, $value, $type = PDO::PARAM_STR) {
        global $DML_detected;
        $query = $param. " => " .$value;
        mysqli_report(MYSQLI_REPORT_ALL ^ MYSQLI_REPORT_STRICT);
        try{
            $result = $this->bindValue($param, $value, $type);
            $the_exception = null;
        }catch(Throwable $e) {
            $result = false;
            $the_exception = $e;
        }
        $is_detected = $DML_detected;
        
        if (($result === false) or ($is_detected===true)){
            if($the_exception) {
                $errno = -1;
                $errstr = $the_exception->getMessage();
            }elseif ($is_detected===true){
                $errno = -9999;
                $errstr = "We detect DDL or DML query";
            } else {
                $errno = $this->errorCode();
                $errstr = $this->errorInfo();
            }
            $json = json_encode(
                [
                    'function' => 'PDOStatement::bindValue',
                    'params' => [$query],
                    'errno' => $errno,
                    'errstr' => $errstr,
                ]
            );
            __fuzzer_file_put_contents(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", $json . "\n", FILE_APPEND);
            chmod(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", 0777);
            if($the_exception != null) {
                throw $the_exception;
            }
        }
        return $result;
    },
    true
);

uopz_set_return(
    'PDOStatement',
    'bindParam',
    function ($param, &$var, $type = PDO::PARAM_STR, $maxLength = 0, $driverOptions = null) {
        global $DML_detected;
        $query = $param. " => " .$var;
        mysqli_report(MYSQLI_REPORT_ALL ^ MYSQLI_REPORT_STRICT);
        try{
            $result = $this->bindParam($param, $var, $type, $maxLength, $driverOptions);
            $the_exception = null;
        }catch(Throwable $e) {
            $result = false;
            $the_exception = $e;
        }
        $is_detected = $DML_detected;
        
        if (($result === false) or ($is_detected===true)){
            if($the_exception) {
                $errno = -1;
                $errstr = $the_exception->getMessage();
            }elseif ($is_detected===true){
                $errno = -9999;
                $errstr = "We detect DDL or DML query";
            } else {
                $errno = $this->errorCode();
                $errstr = $this->errorInfo();
            }
            $json = json_encode(
                [
                    'function' => 'PDOStatement::bindParam',
                    'params' => [$query],
                    'errno' => $errno,
                    'errstr' => $errstr,
                ]
            );
            __fuzzer_file_put_contents(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", $json . "\n", FILE_APPEND);
            chmod(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", 0777);
            if($the_exception != null) {
                throw $the_exception;
            }
        }
        return $result;
    },
    true
);

uopz_set_return(
    'mysqli_stmt',
    'execute',
    function ($params = null) {
        global $DML_detected;
        mysqli_report(MYSQLI_REPORT_ALL ^ MYSQLI_REPORT_STRICT);
        try{
            $result = $this->execute($params);
            $the_exception = null;
        }catch(Throwable $e) {
            $result = false;
            $the_exception = $e;
        }
        if (($result === false) or ($DML_detected===true)){
            if($the_exception) {
                $errno = -1;
                $errstr = $the_exception->getMessage();
            }elseif ($DML_detected===true){
                $errno = -9999;
                $errstr = "We detect MySQli execute";
            } else {
                $errno = $this->errorCode();
                $errstr = $this->errorInfo();
            }
        
            $DML_detected = false;
            if ($params == null){
                $json = json_encode(
                    [
                        'function' => 'mysqli_stmt::execute',
                        'errno' => $errno,
                        'errstr' => $errstr,
                    ]
                );
            }else{
                $json = json_encode(
                    [
                        'function' => 'mysqli_stmt::execute',
                        'params' => [$params],
                        'errno' => $errno,
                        'errstr' => $errstr,
                    ]
                );
            }
            
            __fuzzer_file_put_contents(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", $json . "\n", FILE_APPEND);
            chmod(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", 0777);
            if($the_exception != null) {
                throw $the_exception;
            }
        }
        return $result;
    },
    true
);

uopz_set_return(
    'PDO',
    'prepare',
    function (string $query, array $options = []) {
        mysqli_report(MYSQLI_REPORT_ALL ^ MYSQLI_REPORT_STRICT);
        try{
            $result = $this->prepare($query,$options);
            $the_exception = null;
        }catch(Throwable $e) {
            $result = false;
            $the_exception = $e;
        }
        $is_detected = check_query($query);
        if (($result === false) or ($is_detected===true)){
            if($the_exception) {
                $errno = -1;
                $errstr = $the_exception->getMessage();
            }elseif ($is_detected===true){
                $errno = -9999;
                $errstr = "We detect DDL or DML query";
            } else {
                $errno = $this->errorCode();
                $errstr = $this->errorInfo();
            }
            $json = json_encode(
                [
                    'function' => 'PDO::prepare',
                    'params' => [$query],
                    'errno' => $errno,
                    'errstr' => $errstr,
                ]
            );
            __fuzzer_file_put_contents(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", $json . "\n", FILE_APPEND);
            chmod(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", 0777);
            if($the_exception != null) {
                throw $the_exception;
            }
        }
        return $result;
    },
    true
);

uopz_set_return(
    'PDO',
    'query',
    function (string $query, ?int $fetchMode = null) {
        mysqli_report(MYSQLI_REPORT_ALL ^ MYSQLI_REPORT_STRICT);
        try{
            $result = $this->query($query, $fetchMode);
            $the_exception = null;
        }catch(Throwable $e) {
            $result = false;
            $the_exception = $e;
        }
        $is_detected = check_query($query);
        if (($result === false) or ($is_detected===true)){
            if($the_exception) {
                $errno = -1;
                $errstr = $the_exception->getMessage();
            }elseif ($is_detected===true){
                $errno = -9999;
                $errstr = "We detect DDL or DML query";
            } else {
                $errno = $this->errorCode();
                $errstr = $this->errorInfo();
            }
            $json = json_encode(
                [
                    'function' => 'PDO::query',
                    'params' => [$query],
                    'errno' => $errno,
                    'errstr' => $errstr,
                ]
            );
            __fuzzer_file_put_contents(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", $json . "\n", FILE_APPEND);
            chmod(__FUZZER__MYSQL_ERRORS_PATH . __FUZZER__COVID . ".json", 0777);
            if($the_exception != null) {
                throw $the_exception;
            }
        }
        return $result;
    },
    true
);

$DML_detected = false;

?>

