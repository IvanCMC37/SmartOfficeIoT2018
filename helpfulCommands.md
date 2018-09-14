
#### Set development mode as default for flask
echo "export FLASK_ENV=development" >> ~/.bashrc
source ~/.bashrc

#### Starting the virtual environment
'source venv/bin/activate'. To stop run 'deactivate'

#### Recreating the database
'gcloud sql databases create smartoffice --instance=smartoffice-db'