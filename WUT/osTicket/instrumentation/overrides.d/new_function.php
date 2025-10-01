<?php

    // For disabling nonce verification in WordPress
    uopz_set_return('wp_verify_nonce', function($nonce, $action) {
        return 1;
    }, true);
    
?>