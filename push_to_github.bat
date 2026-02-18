@echo off
cd /d C:\PythonApplications\AI_Skillsweb

echo Adding changes...
git add .

echo Committing changes...
git commit -m "Update"

echo Pushing to GitHub...
git push

echo Done.
pause
