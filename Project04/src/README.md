## Note!!
You must install the packages defined in the "requirements.txt" file, open the terminal and follow these steps:
    python3
    pip install -r requirements.txt

## Running
To run the code, you have to execute main.py with the following command format: 

* If you want to color Asia with lcv and mrv heuristics: 

python3 main.py -m Asia -lcv -mrv 
 
* If you want to also enable arc consistency: 

python3 main.py -m Europe -lcv -mrv -ac3

* to also add Neighbourhood-distance parameter:

python main.py -m Europe -lcv -mrv -ac3 -ND 2

