#!/bin/bash
# https://docs.docker.com/engine/admin/multi-service_container/

TIMEOUT=60
PORTS=${PORTS:-"empty"}

if [ "$PORTS" != "empty" ]; then

    PORTS=${PORTS//,/ }
    PORTS=${PORTS//;/ }
    PORTS=${PORTS//|/ }

    for PORT in $PORTS; do

        if [[ $PORT =~ ^-?[0-9]+$ ]] && [ $PORT -gt 0 ] && [ $PORT -le 65535 ]; then

            RES_PORTS=$RES_PORTS' '$PORT

        fi

    done

else

    echo "Error: LIST OF PORTS not defined."
    exit 1

fi

if [ -z "$RES_PORTS" ]; then

    echo "Error: LIST OF PORTS is empty."
    exit 1

fi

for PORT in $RES_PORTS; do

    $(which gunicorn) -p /run/gunicorn.$PORT.pid --bind 0.0.0.0:$PORT app:app --daemon

    status=$?

    if [ $status -ne 0 ]; then

          echo "Error: FLASK PROGRAM start error $status."
          exit $status

    fi

    sleep 1 # delay pid file

done

while /bin/true; do

    for PORT in $RES_PORTS; do

        if [ $(ps -ax | grep -i $(cat /run/gunicorn.$PORT.pid) | grep -v 'grep' | wc -l) -eq 0 ]; then

            echo "Error: One of the FLASK PROGRAM has already exited."
            exit 1

        fi


    done 

    sleep $TIMEOUT # delay check pid

done
