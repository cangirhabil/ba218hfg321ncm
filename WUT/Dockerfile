FROM php:8.3.6-apache

RUN apt-get update && \
    apt-get install -y --no-install-recommends vim git wget rsync default-mysql-client libpng-dev icu-devtools libicu-dev libjpeg-dev graphicsmagick-libmagick-dev-compat libzip-dev sudo less curl # libpq-dev

RUN apt-get update && apt-get install -y iputils-ping dnsutils zip # For web tools

RUN docker-php-ext-configure bcmath
RUN docker-php-ext-configure exif
RUN docker-php-ext-configure gd --with-freetype --with-jpeg
RUN docker-php-ext-configure intl
RUN docker-php-ext-configure pdo_mysql 
RUN docker-php-ext-configure mysqli
RUN docker-php-ext-configure zip
RUN	docker-php-ext-install -j "$(nproc)" bcmath exif gd intl pdo_mysql mysqli zip opcache # pgsql pdo_pgsql pcntl ftp

WORKDIR /var/www/

RUN pecl install uopz
RUN pecl install xdebug
RUN pecl install pcov

RUN rm /bin/sh && ln -s bash /bin/sh

COPY ./configs/php.ini "$PHP_INI_DIR/php.ini"
COPY ./configs/mpm_prefork.conf /etc/apache2/mods-available/mpm_prefork.conf
COPY ./instrumentation/ /var/www/fuzzer/
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY --from=composer:latest@sha256:1ac7a547cb88acb0de62663b70f2b3d80ad27355288245159404b6ae40cd9ca3 /usr/bin/composer /usr/local/bin/composer

RUN curl -fsSL https://get.docker.com | sh
ARG APP
COPY ${APP}/ /var/www/html/
RUN a2enmod rewrite

COPY ./loc_counter.sh /
RUN chmod +x /loc_counter.sh

WORKDIR /var/www/html/
ENTRYPOINT ["/entrypoint.sh"]

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
