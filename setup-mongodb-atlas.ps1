# PowerShell script to set up MongoDB Atlas connection for the Resume Skill Extractor

Write-Host "MongoDB Atlas Setup Script" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will help you configure your application to use MongoDB Atlas."
Write-Host ""

# Ask for MongoDB Atlas connection details
$MONGODB_URI = Read-Host -Prompt "Enter your MongoDB Atlas Connection String (mongodb+srv://...)"
$MONGODB_DB_NAME = Read-Host -Prompt "Enter your MongoDB Database Name [resume_extractor]"

if ([string]::IsNullOrWhiteSpace($MONGODB_DB_NAME)) {
    $MONGODB_DB_NAME = "resume_extractor"
}

# Create .env file
Write-Host "Creating .env file..."
Set-Content -Path ".env" -Value "MONGODB_URI=$MONGODB_URI"
Add-Content -Path ".env" -Value "MONGODB_DB_NAME=$MONGODB_DB_NAME"
Add-Content -Path ".env" -Value "PORT=8000"

Write-Host ""
Write-Host "Configuration complete! Your .env file has been created with the following settings:" -ForegroundColor Green
Write-Host "------------------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "MONGODB_URI=$MONGODB_URI"
Write-Host "MONGODB_DB_NAME=$MONGODB_DB_NAME"
Write-Host "PORT=8000"
Write-Host "------------------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host ""
Write-Host "You can now run 'docker-compose up -d' to start the application using MongoDB Atlas." -ForegroundColor Yellow 