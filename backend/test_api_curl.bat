@echo off
echo Testing API endpoints with curl...

echo.
echo 1. Testing registration...
curl -X POST "http://127.0.0.1:8000/api/register" ^
-H "Content-Type: application/json" ^
-H "Origin: http://localhost:3000" ^
-d "{\"email\":\"testuser@example.com\",\"password\":\"testpassword123\",\"name\":\"Test User\"}"

echo.
echo.
echo 2. Testing login with the registered user...
curl -X POST "http://127.0.0.1:8000/api/login" ^
-H "Content-Type: application/x-www-form-urlencoded" ^
-d "username=testuser@example.com&password=testpassword123"

echo.
echo.
echo Test completed.
pause