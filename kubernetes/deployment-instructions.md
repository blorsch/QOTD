Create all deployments/services/volumes/claims

On Postgres pod, exec "-stdin --tty -- createdb -U [db-username] quotes", then exec [pod-name] --stdin --tty -- python manage.py db init -> db migrate -> db upgrade
