# If you have docker:
```
docker pull truthadjustr/flaskcrud 
docker run -d truthadjustr/flaskcrud /entrypoint.sh
```
Then, get open browser point to http://<container_ipaddr_here>

# Or manually setup needed python modules, open terminal and
 - pip install flask
 - pip install flask-wtf
 - pip install flask-sqlalchemy
 - pip install flask-migrate
 - pip install flask-bootstrap
 - pip install flask-login
 - pip install flask-redis

And then, `run.sh`

or 

 - pip install -r requirements.txt

And then, `run.sh`

Finally, open browser http://localhost
