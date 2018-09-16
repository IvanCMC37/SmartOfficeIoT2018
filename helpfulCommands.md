
#### Set development mode as default for flask
echo "export FLASK_ENV=development" >> ~/.bashrc
source ~/.bashrc

#### Starting the virtual environment
'source venv/bin/activate'. To stop run 'deactivate'

#### add ip to authorized list
gcloud sql instances patch smartoffice-db --authorized-networks=220.240.203.7

#### Recreating the database
'gcloud sql databases create smartoffice --instance=smartoffice-db'

#### Get ip address of cloud
' gcloud sql instances describe smartofficedb | grep 'ipAddress:' '

#### When getting error object is not json serializable
'result, errors = schema.user_schema.dump(new_user)'

#### rasppi time config
sudo raspi-config  //should keep rasppi in UTC time for security reasons


