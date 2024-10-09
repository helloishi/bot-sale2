echo "Pulling from git.."
echo "-------------------------"
git pull origin backend
echo "-------------------------"
echo "Recreating service..."
echo "-------------------------"
docker compose up web --build -d --no-deps --force-recreate
