@echo off
@cd %~dp0
docker-compose -f docker-compose-poll.yml up -d --build
pause