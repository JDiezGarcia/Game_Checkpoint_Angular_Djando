# Bike Rider install and configuration steps

Example environment file on `config/private/dev/super-secrets.env`:
```
GC_MAIL_HOST=smtp.gmail.com
GC_MAIL_PORT=587
GC_MAIL_NAME=Bike Rider
GC_MAIL_USER=bikerider@gmail.com
GC_MAIL_PASS=account_or_app_password
```


To configure the project for production, use the folder `config/private/prod`. The files and variables are the same, so you can copy the development config over to prod.

To start the project in development mode, use: `docker-compose up`

To build and deploy the project in production mode, use: `docker-compose -f docker-compose.prod.yml up`

Note that since some container names are the same in dev and prod, you might need to run `docker-compose down` to remove old containers.
