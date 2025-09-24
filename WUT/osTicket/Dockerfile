# Use PHP 8.3 with Apache
FROM php:8.3.6-apache

# Install system dependencies and PHP extensions
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libzip-dev \
    libicu-dev \
    libonig-dev \
    libxml2-dev \
    libldap2-dev \
    mariadb-client \
    unzip \
    wget \
    curl \
    cron \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-configure ldap --with-libdir=lib/x86_64-linux-gnu/ \
    && docker-php-ext-install -j$(nproc) \
        gd \
        mysqli \
        pdo_mysql \
        zip \
        intl \
        mbstring \
        xml \
        ldap \
        gettext \
        imap \
    && rm -rf /var/lib/apt/lists/*

# Enable Apache modules
RUN a2enmod rewrite ssl headers

# Copy PHP configuration
COPY configs/php.ini /usr/local/etc/php/conf.d/osticket.ini

# Copy Apache configuration
COPY configs/000-default.conf /etc/apache2/sites-available/000-default.conf

# Set proper working directory
WORKDIR /var/www/html

# Download and extract osTicket (using development version)
RUN wget -O osticket.zip https://github.com/osTicket/osTicket/archive/refs/heads/develop.zip \
    && unzip osticket.zip \
    && mv osTicket-develop/* . \
    && mv osTicket-develop/.* . 2>/dev/null || true \
    && rm -rf osTicket-develop osticket.zip

# Set proper permissions and create config file
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html \
    && cp include/ost-sampleconfig.php include/ost-config.php \
    && chmod 666 include/ost-config.php \
    && mkdir -p attachments \
    && chmod 777 attachments

# Create healthcheck script
RUN echo '#!/bin/bash\ncurl -f http://localhost:80/ || exit 1' > /usr/local/bin/healthcheck.sh \
    && chmod +x /usr/local/bin/healthcheck.sh

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD /usr/local/bin/healthcheck.sh

# Expose port 80
EXPOSE 80

# Start Apache in foreground
CMD ["apache2-foreground"]