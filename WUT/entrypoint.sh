#!/bin/bash
mkdir -p /shared-tmpfs/{branch_statements,coverage-reports,exception-reports,error-reports,mysql-error-reports,shell-error-reports,unserialize-error-reports,pathtraversal-error-reports,xxe-error-reports}
chmod -R 777 /shared-tmpfs/
chown -R www-data:www-data /var/www/ /shared-tmpfs/{branch_statements,coverage-reports,exception-reports,error-reports,mysql-error-reports,shell-error-reports,unserialize-error-reports,pathtraversal-error-reports,xxe-error-reports}

if [ 0 -lt ${REQUIRES_DB} ]; then
	while ! mysqladmin ping -h"db" --silent; do
		echo "Waiting for db"
		sleep 1
	done
	echo "DB appears online!"
fi


if [ -f /var/www/html/init.sh ]; then
    chmod +x /var/www/html/init.sh
    /var/www/html/init.sh
fi

if [ -f /loc_counter.sh ]; then
    echo "Counting the LoC"
    /loc_counter.sh
fi

sed -e  "s|pcov.directory=.*|pcov.directory=${FUZZER_COVERAGE_PATH}|" -i ${PHP_INI_DIR}/php.ini
/usr/sbin/apache2ctl -D FOREGROUND
