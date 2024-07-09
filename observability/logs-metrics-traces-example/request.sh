#!bin/sh

random_sleep() {
    sleep $(( ( RANDOM % 5 )  + 1 ))
}

for i in {1..100}; do
    curl -X GET http://localhost:9998/call-ms-two
    sleep 5
done