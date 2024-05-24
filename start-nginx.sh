#!/bin/bash
set -e

/usr/bin/wait-for-backend.sh backend 8000

nginx -g 'daemon off;'