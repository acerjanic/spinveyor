#!/bin/zsh
export $(grep -v '^#' .env | xargs)
