#!/bin/bash
set -e

/usr/bin/wait-for-backend.sh backend 8001

nginx -g 'daemon off;'