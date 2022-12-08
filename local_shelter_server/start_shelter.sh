IP=$(ifconfig eth0 | awk '/inet/ { print $2 }')
echo $IP

PORT=":8000"

DEST=${IP}${PORT}

echo $DEST

cd /root/LivingLab-ShelterServer/local_shelter_server

pwd

sleep 5s
python3 manage.py migrate # migrate database

sleep 5s

python3 manage.py runserver $DEST
