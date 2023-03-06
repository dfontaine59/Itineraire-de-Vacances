#!/bin/bash

# dans le répoertoire de travail avec les fichiers python, dockerfile et docker-compose.yml

docker container rm -f iti_streamlit_compose
docker container rm -f iti_fastapi_compose

# -----------------------------------------------------------------------------------------
# partie image api
docker image build . -t iti_fastapi:latest -f Dockerfile_fastapi

# -----------------------------------------------------------------------------------------
# partie image streamlit
docker image build . -t iti_streamlit:latest -f Dockerfile_streamlit

docker-compose up