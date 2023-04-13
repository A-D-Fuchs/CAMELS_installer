::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCuDJH+R90ojFCtGQwmNKGK1CIk6ycHJ4uuTnm48eccTS7P4+5mrDNMs40v3YZch2n9IpOIBDRxdbS6ITyIRhV0Mv2eKVw==
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJgZko0
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQITCTZxYDfCcSuZCbsa4e/u/euFrkhddfIvdIbY26CHL+5T7Er2Nbso12lPis4BCRVMbV7rSxckrHxLu2GLI9TcsgHlCmSI5EQiGnF7lXqQvzIodNZliaM=
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQITCTZxYDfCNXj6B/Uf5+b95u2SsEwfWOd/dYrayaGcJe0W5FGkZpkrwm1bis5ATA9ZbBWuegow6XpNoWWXM9TcpwfkClqM9145CWB5gm3En2s0ZpNtgtMGwSmz+UPrnqlQwnfzV61DBnfg1akoKMEZ7gO3eweIsrZHT7bjarPwQzPQM2wNhX3GhZd53pY5Vix8VB0aivlh9CfsSoau2HIBJjWFqenl20wmYtf+YrBZjRihzzJb3emmhFgNQmpAWVQCQRaGSS7cGwPYhb/YbA1kqdi5db1ndnwrV6RWOxwk9MA3qSO9j/ZsP8SwiSHKHtfZEwl+P6XgJ32Y6CSoZWa2f8tDjwGg7LbPwuMut6fO97myLM6+uYh+CLcCB9TML5izeaW3ooB9lJmCmToGR1in/i4PCQKr31r2gSf2tO8yfmjuKLCnTPxqeslbkly1NnrJkWYJ5qarGZPzW2jvTcrKryBm2JPZKEQx+Erb6iNR7ClDlV/W/LQyGXT85MXKNMDhSXFU77Ot5AxeIT6OYD4e19gRT+KXfACPwaJy4L1NmVcfqqckB2rhsu/J7JpYrMk4vXU+4VI5c5Y8krMsnRoIFGAcXfjfyOaYR47VZxBG6M9ZgQ2l08Y51FYFLWMC6GSHCBMImk4o9vVqsN2bpaB+UIiXKX0=
::dhA7uBVwLU+EWH+l3XA9KQ8UAUSqCSuYA6cQ4eab
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCuDJH+R90ojFCtGQwmNKGK1CIk6ycHJ4uuTnm48eccTS7P4+5mrDNMs40v3YZch2n9IpNkZAid2UT+KSkIXiENnmlfLMt+Z0w==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
SETLOCAL
for /f %%i in ('.\run\read_ini.bat /i python_exe_path .\run\NOMAD-CAMELS.ini') do set python_exe=%%i
for /f %%i in ('.\run\read_ini.bat /i camels_start_path .\run\NOMAD-CAMELS.ini') do set camels_start_path=%%i
start %python_exe% %camels_start_path%
ENDLOCAL