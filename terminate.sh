OUTPUT=$(netstat -nao | grep :8000)
taskkill //F //PID ${OUTPUT##* }