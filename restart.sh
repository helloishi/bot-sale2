docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker volume rm $(docker volume ls -q)
docker compose up --build -d 
docker exec -it backend python manage.py makemigrations
docker exec -it backend python manage.py migrate
