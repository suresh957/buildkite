#!/usr/bin/env bash

set -euo pipefail

cat << EOF
steps:
  - label: "Download Artifacts and initiate tests"
    command:
      - "echo this is test file"
    agents:
      queue: cartlink-1
  - block: "Check AWS Results"
  - label: "Checking Results from aws DeviceFarm"
    command:
      - "echo ${BUILDKITE_BUILD_NUMBER}"
    agents:
      queue: cartlink1
EOF
