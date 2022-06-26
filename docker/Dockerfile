FROM continuumio/miniconda3:latest

COPY . /opt/refactai
WORKDIR /opt/refactai


# Install requirements
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["/"]

