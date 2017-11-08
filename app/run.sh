#!/bin/bash
# https://docs.docker.com/engine/admin/multi-service_container/

PORTS=${PORTS:-"empty"}

if [ "$PORTS" != "empty" ]; then

    PORTS=${PORTS//,/ }
    PORTS=${PORTS//;/ }
    PORTS=${PORTS//|/ }

    for PORT in $PORTS; do

        if [[ $PORT =~ ^-?[0-9]+$ ]]; then

            $(which gunicorn) -p /run/gunicorn.$PORT.pid --bind 0.0.0.0:$PORT app:app --daemon

            status=$?
            if [ $status -ne 0 ]; then
                  echo "Failed to start: $status"
                  exit $status

                fi

        fi

    done

fi

while /bin/true; do

    for PORT in $PORTS; do

        if [[ $PORT =~ ^-?[0-9]+$ ]]; then

            if [ $(ps -ax | grep -i $(cat /run/gunicorn.$PORT.pid) | grep -v 'grep' | wc -l) -eq 0 ]; then

                echo "One of the processes has already exited."
                exit -1

            fi

        fi

    done 

    sleep 60 # delay

done
