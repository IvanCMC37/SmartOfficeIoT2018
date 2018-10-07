
#### Set development mode as default for flask
1. echo "export FLASK_ENV=development" >> ~/.bashrc
   source ~/.bashrc
2. (Better way)
Add to .flaskenv file
FLASK_APP=app.py
FLASK_ENV=development

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

#### fixing a corrupted git
delete .git folder, reclone git repo locally, copy .git folder back into project

#### give github credentials for pushing/pulling
git config credential.helper store

#### solving the circular import issue when using sqlalchemy and marshmallow
use db.init_app(APP) and ma.init_app(APP) and import db and ma from another module

#### Set volume of your pi
alsamixer

#### disable assistantPi.service to prevent sensehat crash
sudo systemctl stop AssistantPi.service
sudo systemctl disable AssistantPi.service
sudo reboot

#### enable assistantPi.service in order to run google assistant
<!-- sudo systemctl start AssistantPi.service -->
sudo systemctl enable AssistantPi.service
sudo reboot