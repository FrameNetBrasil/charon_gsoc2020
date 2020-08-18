This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

The repository contains code for a multimodal annotation preprocessing tool built using React and PHP. 

GSoC report links:   
https://github.com/FrameNetBrasil/webtool/blob/gsoc2020_2/GSoC2020/weekly_reports/FirstEvaluationReport_idea2.md
https://github.com/FrameNetBrasil/webtool/blob/gsoc2020_2/GSoC2020/weekly_reports/SecondEvaluationReport_idea2.md

This distribution is running as a Docker container. In order to run this container you'll need docker installed:

* [Docker Windows](https://docs.docker.com/windows/started)
* [Docker OS X](https://docs.docker.com/mac/started/)
* [Docker Linux](https://docs.docker.com/linux/started/)

### Usage

* Clone this repository at an accessible folder

```sh
$ git clone https://github.com/FrameNetBrasil/charon.git
```
* Download the trained model file from this google drive link, and save it in the public/server folder
https://drive.google.com/file/d/1iw7VIoBspqgChl-4nDU809A6rvwZqKk5/view?usp=sharing

* Start the container

```sh
$ cd charon/devops/charon
$ docker-compose up
```

* Build frontend app

```sh
$ cd charon
$ docker exec -it fnbr-webserver-charon bash

// inside the container

# npm install
# npm run build
```
 
* Access the app at http://localhost:8600

* To start the flask server follow these steps inside the root directory of the container:  

```sh
$ cd public/server
$ apt-get install python3.7
$ apt-get install python3-pip python3-dev python3-venv
$ python3 -m pip install --upgrade pip 
$ python3 -m pip install numpy matplotlib keras opencv-python scikit-learn scikit-image scipy argparse mysql-connector-python Pillow pickle-mixin glob3 flask opencv_contrib_python mpld3 moviepy
$ python3 -m pip install flask_cors, requests
$ apt update && apt install -y libsm6 libxext6
$ apt-get install -y libxrender-dev
$ python3 -m pip install --upgrade pip 
$ python3 -m pip install tensorflow==2.2.0 --no-cache-dir
$ python3 -m pip install elementpath
$ apt-get install python3-tk 
$ python3 track_objects.py
```
The server will start running on http://127.0.0.1:5000/

#### Container Parameters

Parameters are available to the container (mainly the webserver port) at

```shell
/charon/devops/charon/.env
```

Also adjust React env at (baseURL for API)

```shell
/charon/.env
```
Note: Since frame element updates are not being made currently in the ObjectMM table, to avoid referential integrity errors, temporarily remove the foreign keys by executing the following sql commands in the ObjectMM table from phpmyadmin:

```shell
ALTER TABLE objectmm DROP FOREIGN KEY fk_ObjectMM_AnnotationSetMM
ALTER TABLE objectmm DROP FOREIGN KEY fk_ObjectMM_FrameElement
```

## Built With

* PHP 7.4
* MariaDb 10.4
* PhpMyAdmin 5.0.1
* React 
* IBM Cloud Speech-to-Text API URL: https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?end_of_phrase_silence_time=2.0&split_transcript_at_phrase_end=true&speaker_labels=true



<!--
### Steps to reproduce:
1. Install React, npm and Node js on your system.  
2. Install Xampp to run the development server. 
3. Add the paths of these packages to the environment variables of your system.    
4. Clone this repository using Github Desktop.  
5. Copy the server and vendor folders listed under the src directory to your local xampp/htdocs/ folder.  
6. Install composer on your system, and copy the composer.json file present in src to your xampp/htdocs folder.  
7. Open another command prompt or terminal, move to the directory xampp/htdocs and then run `composer require php-ffmpeg/php-ffmpeg`  
8. Run the add_paths.bat file if using a Windows System or add_paths.sh file if using a Linux system, to add the paths to environment variables.  
9. Open xampp control panel as administrator and start apache and mysql.  
10. Access the phpmyadmin page at `localhost/phpmyadmin` and import the webtool mysql database dump located at mariadb/webtool_github_bkp.sql.gz (You may have to update the entry:`$cfg['ExecTimeLimit'] = 0;` of the config.default.php file in the phpmyadmin/libraries folder of xampp to import the whole dump without problems of time limit being exceeded which can break the import.). Also change the `max_execution_time` entry in php.ini under xampp/php/ to 0 , i.e. `max_execution_time=0`
9. Open the folder of the cloned repository on your machine using Command Prompt or Terminal eg: `cd Desktop/charon` 
10. Run `npm install` to install all the dependencies to run the app. 
11. Run `npm start` to start the app. 
12. The app will open at localhost:3000 in a tab on your browser  
13. Select a video file from your computer or enter a URL. You will receive a few notifications from the app. Then select your language, corpus and document from the dropdown lists. Finally click on the Upload Files button.  
14. Wait for the server to run, as it may take some time to generate the audio transcripts. The video file, extracted audio file, generated thumbnail and audio transcript text files will be stored under `Video_Store/full/`, `Audio_Store/audio/`, `Images_Store/thumbnails/` and `Text_Store/transcripts` folders under src respectively, if all the size constraints, duplicate checks, URL validation, etc. checks are successful.  
15. A new entry in the documentmm table will be generated, that can be accessed using phpmyadmin.  
-->
