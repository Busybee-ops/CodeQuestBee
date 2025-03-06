SUBSCRIPTION="Azure subscription 1"
RESOURCEGROUP="beeResourceGroup"
LOCATION="centralus"
PLANNAME="MyAppServicePlanf3624e"
PLANSKU="F1"
SITENAME="bee-2025"
RUNTIME="PYTHON|3.10"
# Set the correct Azure resource group and app name
RESOURCE_GROUP="beeResourceGroup"
WEB_APP_NAME="bee-2025"
STARTUP_FILE="unicorn app.main:app --host 0.0.0.0 --port 8000"
# Set the Azure Web App configuration
az webapp config set --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME --startup-file "$STARTUP_FILE"