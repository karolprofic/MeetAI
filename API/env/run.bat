@echo off

set CONDAPATH=%PROGRAMDATA%\Miniconda3
set ENVNAME=MeetAI
set ENVPATH=""

rem If Miniconda3 folder does not exist ask for the path 
:find_conda
if not exist %CONDAPATH%\ (
	set /p CONDAPATH=Enter path to Miniconda3 folder: 
	goto find_conda
	pause
	exit
) 

:find_environment
rem Find the MeetAI Conda environment 
if exist %CONDAPATH%\envs\%ENVNAME%\ (
	echo Found global Conda environment
	set ENVPATH=%CONDAPATH%\envs\%ENVNAME%
) 
if exist %USERPROFILE%\.conda\envs\%ENVNAME%\ (
	echo Found local Conda environment
  	set ENVPATH=C:\Users\%USERNAME%\.conda\envs\%ENVNAME%
)

rem If the environment does not exist ask whether to create it
if %ENVPATH%=="" (
	echo Cannot find MeetAI Conda environment.
	goto instalation_option
	pause
	exit
)

rem Activate MeetAI Conda enviroment and run API server
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python main.py
call conda deactivate
pause
exit

rem Ask user whether to create an environment
:instalation_option
set choice=
set /p choice=Do you want to create it [Y/N]?: 
if not '%choice%'=='' set choice=%choice:~0,1%
if '%choice%'=='Y' goto install_enviroment
if '%choice%'=='y' goto install_enviroment
if '%choice%'=='N' goto exit_script
if '%choice%'=='n' goto exit_script
if '%choice%'=='' goto exit_script
echo "%choice%" is not valid
goto instalation_option


:exit_script
echo Thank you for using our software!
pause
exit


:install_enviroment
echo The creation of MeetAI Conda environment has been started!
call %CONDAPATH%\Scripts\activate.bat base
call conda env create -f conda.yaml 
call conda deactivate
goto find_environment
pause
exit

