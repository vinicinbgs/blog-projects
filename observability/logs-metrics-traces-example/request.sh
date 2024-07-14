#!bin/sh

TIMES=1000
SLEEP=0
ROUTE="/call-ms-two"

for i in "$@"
do
case $i in
    sleep=*)
    SLEEP="${i#*=}"
    shift
    ;;
    times=*)
    TIMES="${i#*=}"
    shift
    ;;
    route=*)
    ROUTE="${i#*=}"
    shift
    ;;
    *)
    ;;
esac
done

for i in $(eval echo {1..$TIMES}); do
    curl -X GET http://localhost:9998$ROUTE
    sleep $SLEEP
done