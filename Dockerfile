#
# Start with ubuntu+python image
#

FROM python:3.8.3-slim


#
# Setup non-root user and app directory
#
RUN apt update
RUN apt install -y netcat

# Create non-root user account

RUN useradd -u 999 --system --shell=/bin/bash pigeon


# Create app directory

RUN mkdir -p /opt/app
RUN chown -R pigeon:pigeon /opt/app


# Switch to the non-root user and the app directory

USER pigeon
RUN id
WORKDIR /opt/app


#
# Create and setup the Python virtual environment
#

RUN python -m venv venv


# Upgrade pip inside the virtualenv due to pip bug with private repos 

RUN venv/bin/pip install --no-cache-dir -U pip 


# copy over sources and requirements file
COPY --chown=pigeon:pigeon requirements.txt requirements.txt

RUN venv/bin/pip install --no-cache-dir -r requirements.txt

#
# Add project sources
#
COPY --chown=pigeon:pigeon messenger messenger

#
# Add logs dir
#
RUN mkdir -p logs

## Expose port(s)

# UDP Port
EXPOSE 9089
EXPOSE 9090

# Stress test command
# CMD ["venv/bin/python", "-m", "messenger.test.stress.short_circuit_udp.inbound"]

# Default command
CMD ["venv/bin/python", "-m", "messenger"]

