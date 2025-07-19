<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * Localized language
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'db' );

/** Database username */
define( 'DB_USER', 'user' );

/** Database password */
define( 'DB_PASSWORD', 'password' );

/** Database hostname */
define( 'DB_HOST', 'db' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',          'HRYh5$Mz`gGME[M[b )h__Urmm6u#c/f,ZU)%RC;1C#Sz$U]OPuZNrV&Wjn o0G4' );
define( 'SECURE_AUTH_KEY',   'I.;QQQ eb>B#hqc=B]_/*|)K|ljrKt+)@Ow)ADD8i0TigHz<%uM4iL*0A4hK cCW' );
define( 'LOGGED_IN_KEY',     'u<Z+E<C8AZ6^ f7[ku52uT>$ <qr=!WYuGZ5Z}(RgXX{}ULiwJiY2%VU=%.4;/xN' );
define( 'NONCE_KEY',         'wj:n5=m+g-:~;{dBe)jrH;2iIMfftfU]^uqpj4)tn4M4K:i 0)R18%`g~%hqUr64' );
define( 'AUTH_SALT',         'k>^t.--$?k}eohe=Z|Xp`=F3Q,p-^ovtcxX!%pV/iJ%=xYo`e=zU.C9L`9iDtAE1' );
define( 'SECURE_AUTH_SALT',  'oF+<+P6*C.:iHy^wBpAXI=t_(/&~_)%kU$/4S2cGt]]*]!Smoterb`UjM8RO`vEg' );
define( 'LOGGED_IN_SALT',    '(#/y}XyDKq]Dm-G6nhv g`L+)~[8u|V|+:h [JHMA>mcwb5$msi&Mf!%;EdEhn`2' );
define( 'NONCE_SALT',        '{yZtx-5fg~cS>r,/9g VnL]}V@HAjK^%:~[11d~/%V_Q|^AB=[SmJaRyVdKTI_[P' );
define( 'WP_CACHE_KEY_SALT', 'STQAS(WGE[3lSH2t[?e^U%ath}XqlU$NUb#.q%l~~Z7xm6K4|YtETcsk-S8[>`;G' );


/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';


/* Add any custom values between this line and the "stop editing" line. */



/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
if ( ! defined( 'WP_DEBUG' ) ) {
	define( 'WP_DEBUG', false );
}

/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
