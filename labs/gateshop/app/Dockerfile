FROM php:8.2-apache

# Extensions: pdo_mysql for the DB; dom/simplexml/libxml/pdo_sqlite ship with the base image.
RUN docker-php-ext-install -j"$(nproc)" pdo_mysql mysqli >/dev/null

# Serve app/public as the web root, allow .htaccess rewrites, and use index.php as the directory index.
RUN a2enmod rewrite \
 && sed -ri 's!DocumentRoot /var/www/html!DocumentRoot /var/www/html/app/public!' /etc/apache2/sites-available/000-default.conf \
 && printf '%s\n' \
    '<Directory /var/www/html/app/public>' \
    '  AllowOverride All' \
    '  Require all granted' \
    '  DirectoryIndex index.php' \
    '</Directory>' > /etc/apache2/conf-available/gateshop.conf \
 && a2enconf gateshop

# App code (build context is the project root; see docker-compose.yml).
COPY . /var/www/html/
RUN chown -R www-data:www-data /var/www/html

EXPOSE 80
