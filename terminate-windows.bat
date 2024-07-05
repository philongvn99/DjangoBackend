FOR /F "tokens=5*" %%F IN ('netstat -nao ^| findstr :8080') DO (
  SET OUTPUT=%%F
)
taskkill /F /PID %OUTPUT%



