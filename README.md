[Linux]
python3 -m virtualenv .env #Create virtualenv

source .env/bin/activate #activate env

python3 -m pip install -r requirements.txt #install requirements pack

deactivate #deactivate

[Windows]
python -m virtualenv .env #Create virtualenv

.\.env\Scripts\activate #activate env

python -m pip install -r requirements.txt #install requirements pack

deactivate #deactivate