#!/bin/bash

ACTION=$1

if [[ "$ACTION" == "START" ]]; then
    PORT=$2
    NAME=$3

    if [[ -z "$PORT" || -z "$NAME" ]]; then
        echo "Usage: $0 START <port> <name>"
        exit 1
    fi

    echo "Starting project '$NAME' on port $PORT..."
    PORT=$PORT docker-compose -p "$NAME" up --build

elif [[ "$ACTION" == "STOP" ]]; then
    NAME=$2

    if [[ -z "$NAME" ]]; then
        echo "Usage: $0 STOP <name>"
        exit 1
    fi

    echo "Stopping project '$NAME' and removing volumes..."
    docker-compose -p "$NAME" down -v

else
    echo "Invalid action. Use START or STOP."
    exit 1
fi
