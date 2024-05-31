#!/bin/bash

# Obtener el ID del contenedor en ejecución
CONTAINER_ID=$(docker ps -q)

if [ -z "$CONTAINER_ID" ]; then
    echo "No hay contenedor en ejecución."
fi

# Obtener el ID de la imagen asociada al contenedor
IMAGE_ID=$(docker inspect --format='{{.Image}}' $CONTAINER_ID)

if [ -z "$IMAGE_ID" ]; then
fi

# Detener y eliminar el contenedor
docker stop $CONTAINER_ID
docker rm $CONTAINER_ID

# Eliminar la imagen asociada (forzando la eliminación)
docker rmi -f $IMAGE_ID

echo "Contenedor detenido y eliminado, imagen eliminada también."
