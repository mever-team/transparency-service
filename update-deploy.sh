#!/bin/bash
set -e  # stop on first error

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

if ! git diff-index --quiet HEAD --; then
  echo -e "${RED}Working tree is dirty. Commit or stash first.${NC}"
  exit 1
fi

echo -e "${BLUE}Updating dev...${NC}"
git checkout dev
git pull --ff-only

echo -e "${BLUE}Updating deploy...${NC}"
git checkout deploy
git merge dev
git push origin deploy

echo -e "${BLUE}Returning to dev...${NC}"
git checkout dev

echo -e "${GREEN}Done ✅${NC}"