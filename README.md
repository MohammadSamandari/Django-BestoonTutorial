## Bestoon

A sinple income and expense system.


#### Curl:
we can run curl to send a data to a url and get the answer.
we also can create a file in bin/ folder and run that file easily

* Creating the file :

vi ~bin/bestoonexpense.sh

* Creating a file  like this:
mytoken=1234567

curl --data "token=$mytoken&amount=$1&text=$2" http://localhost:8009/submit/expense/

* make the file executable
chmod 755 THEFILE

* run the file like this:
bestoonexpense AMOUNT "TEXT"

