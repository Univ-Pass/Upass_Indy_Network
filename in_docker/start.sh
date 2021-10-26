#!/bin/bash

set -e

email=${1}

python3 generate_did.py "${email}"

