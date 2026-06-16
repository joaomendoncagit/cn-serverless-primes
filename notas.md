```bash
men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ tree
.
├── README.md
├── benchmark
│   ├── coldstart.py
│   ├── concurrent.py
│   └── latency.py
├── figures
├── lambda
│   └── lambda_function.py
├── notas.md
└── results

5 directories, 6 files
```

```bash
men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ python3 -m venv venv
men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ source venv/bin/activate
(venv) men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ which python
/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab/venv/bin/python
(venv) men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ python --version
Python 3.12.3
```

```bash
(venv) men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ pip install -r requirements.txt
(venv) men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ pip list
Package            Version
------------------ -----------
aiohappyeyeballs   2.6.2
aiohttp            3.14.1
aiosignal          1.4.0
attrs              26.1.0
certifi            2026.5.20
charset-normalizer 3.4.7
contourpy          1.3.3
cycler             0.12.1
fonttools          4.63.0
frozenlist         1.8.0
idna               3.18
kiwisolver         1.5.0
matplotlib         3.11.0
multidict          6.7.1
numpy              2.4.6
packaging          26.2
pandas             3.0.3
pillow             12.2.0
pip                24.0
propcache          0.5.2
pyparsing          3.3.2
python-dateutil    2.9.0.post0
requests           2.34.2
six                1.17.0
typing_extensions  4.15.0
urllib3            2.7.0
yarl               1.24.2
```

```bash
(venv) men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ pip freeze > requirements.txt
(venv) men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ cat requirements.txt
aiohappyeyeballs==2.6.2
aiohttp==3.14.1
aiosignal==1.4.0
attrs==26.1.0
certifi==2026.5.20
charset-normalizer==3.4.7
contourpy==1.3.3
cycler==0.12.1
fonttools==4.63.0
frozenlist==1.8.0
idna==3.18
kiwisolver==1.5.0
matplotlib==3.11.0
multidict==6.7.1
numpy==2.4.6
packaging==26.2
pandas==3.0.3
pillow==12.2.0
propcache==0.5.2
pyparsing==3.3.2
python-dateutil==2.9.0.post0
requests==2.34.2
six==1.17.0
typing_extensions==4.15.0
urllib3==2.7.0
yarl==1.24.2
```

- Now, all the "python packages and exact respective versions" installed in the current environment, which is the virtual environment venv/, are recorded on the file requirements.txt

```bash
(venv) men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ cat .gitignore 
venv/

__pycache__/
*.pyc

.env

.vscode

results/*
figures/*
```

```bash
(venv) men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ nano .gitignore
(venv) men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ cat .gitignore 
venv/

__pycache__/
*.pyc

.env

.vscode

results/*
figures/*
```

```bash
(venv) men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ touch results/.gitkeep
touch figures/.gitkeep
```

```bash
(venv) men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ nano lambda/lambda_function.py
(venv) men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ cat lambda/lambda_function.py 
import json

def generate_primes(n):
    primes = []

    for candidate in range(2, n):
        is_prime = True

        for divisor in range(2, int(candidate**0.5) + 1):
            if candidate % divisor == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(candidate)

    return primes


def lambda_handler(event, context):

    n = int(event.get("n", 100))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "n": n,
            "primes": generate_primes(n)
        })
    }


if __name__ == "__main__":

    event = {
        "n": 20
    }

    print(lambda_handler(event, None))
(venv) men-jo@DESKTOP-629L8A9:/mnt/c/Users/Joao Tiago/Documents/Uni/CN/ProjetoLaboratorial/projeto_lab$ python lambda/lambda_function.py
{'statusCode': 200, 'body': '{"n": 20, "primes": [2, 3, 5, 7, 11, 13, 17, 19]}'}
```