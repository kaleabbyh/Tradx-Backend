#!/bin/bash

# stop executing the script on error
set -e

echo ""
echo "-----------------------------------------"
echo "Running git pull"
echo "-----------------------------------------"
echo ""
git pull


echo ""
echo "-----------------------------------------"
echo "Deploying Backend"
echo "-----------------------------------------"
echo ""

docker compose up -d --build

echo ""
echo "-----------------------------------------"
echo "Deployment completed successfully"
echo "-----------------------------------------"
echo ""
