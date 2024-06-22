FOR /F "tokens=5*" %%F IN ('netstat -nao ^| findstr :8080') DO (
  echo %%F
  SET OUTPUT=%%F
)
ECHO %OUTPUT%
taskkill /F /PID %OUTPUT%



