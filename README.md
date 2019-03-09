<p align="center">
  <a href="" rel="noopener">
 <img width=300px src="./assets/honesty.jpeg" alt="honesty-logo"></a>
</p>

<h3 align="center">Honesty</h3>

<div align="center">

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
<br>
</div>

------------------------------------------

> PWA cum ChatBot, that furnishes users with all the government sponsored policies, schemes and loans.

------------------------------------------

### Features

- Dialogflow model used to pre-process user queries.

- doc2vec model to find out similar policies, based on the entities found in the given query.

- PWA, which is cross-platform and can be accessed at ease.

- Dynamic scraper and parser to fetch latest policies and schemes.

- Multi-language (Hindi for now) support, to entertain queries from any rural person

- Offline SMS (TextLocal) and calling service (Dialogflow) to fetch any necessary detail 


------------------------------------------

### Installation

* Make sure you have [mongodb](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/) and [ngrok](https://ngrok.com/) installed on your device, using ngrok to port an http tunnel to your localhost
* Install dependencies and run flask app
```sh
        $ cd app
        $ pip3 install -r requirements.txt
        $ sudo service mongod start
        $ flask run
```
* Add your own API keys for TextLocal and Dialogflow
* Run [final_module.py](https://github.com/2knal/Honesty/blob/master/sms/final_module.py)
------------------------------------------
### Contributing

 We're are open to `enhancements` & `bug-fixes` :smile: Also do have a look [here](./CONTRIBUTING.md).

-------------------------------------------

### Note

- This project was done under `30 hours with minimal pre-preparation`.

------------------------------------------
### Contributors

- [@vtg2000](https://github.com/vtg2000)
- [@2knal](https://github.com/2knal)
- [@anay121](https://github.com/anay121)
- [@fate2703](https://github.com/fate2703/)
- [@KaustubhDamania](https://github.com/KaustubhDamania/)
- [@mihir2510](https://github.com/mihir2510)

------------------------------------------
#### Recognition
`This repository is a part of Smart India Hackathon 2019`
<br/>
[@BitsPlease](https://www.sih.gov.in/finalResult)
