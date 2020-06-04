#
# General settings
#

SHELL = /bin/bash

CURRENT_DIR = $(shell pwd)

.ONESHELL:
# .SHELLFLAGS = -e

# Environment variables
export ASED_PIGEON_LOG_LEVEL = DEBUG
export ASED_PIGEON_INBOUND_HOST = 127.0.0.1
export ASED_PIGEON_INBOUND_PORT = 9089
export ASED_PIGEON_OUTBOUND_HOST = 127.0.0.1
export ASED_PIGEON_OUTBOUND_PORT = 9090
export ASED_PIGEON_INBOUND_KAKFA_TOPIC = pigeon.test.inbound
export ASED_PIGEON_OUTBOUND_KAKFA_TOPICS = pigeon.test.outbound
export ASED_PIGEON_KAFKA_HOST = 127.0.0.1
export ASED_PIGEON_KAFKA_PORT = 19092
export ASED_PIGEON_KAFKA_PORT = 19092
export ASED_PIGEON_OUTPUT_HANDLER_COUNT = 1
export ASED_PIGEON_UDP_LISTENER_COUNT = 1

.PHONY: fly
fly:
	mkdir -p logs
	source .venv/bin/activate
	python -m messenger


.PHONY: test_short_circuit_udp
test_short_circuit_udp:
#	$(info $$var is [${ASED_PIGEON_LOG_LEVEL}])echo Hello world
	mkdir -p logs
	source .venv/bin/activate
	python -m messenger.test.stress.short_circuit_udp.inbound
