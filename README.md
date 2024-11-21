# StreamSmart
<p align="center">
    <img src="logostreamsmart" width="100%">
</p>

<p align="center">
  <a href="#presentation">Presentation of the application</a> •
  <a href="#how-to-run">How to run the application </a> •
  <a href="#how-it-works">How the application works</a> •
  <a href="#credits">Credits</a> •
  <a href="#todo">TODO</a> 
</p>

## Presentation
**Note : This repository is part of a 2nd Year project at ENSAI school. Hereis the [link](https://ludo2ne.github.io/ENSAI-2A-Projet-info/doc/projet/sujets-2024-2025.html#streamsmart) of the subject : link . The goal of this project is To develop a Python application, explore software architecture, communicate with a PostgreSQL database, use web services, and design and model using UML.**


This project aims to develop a comparison tool that analyzes different platforms' catalogs to recommend the subscription best suited to your movie tastes. The user creates a watchlist, and the application returns the subscription that best meets their needs (most cost-effective, offers the most films in the watchlist, etc.).


<p align="center">
    <img src="logo streamsmart" width="100%">
</p>

### Features

1: User Management (Create a user, Log in, Delete a user)

2: Search for a movie  by its name

3: See the details of a movie : 

F4: Watchlist Management (Create a watchlist, Add a movie to a watchlist, Delete a watchlist)

F5: For a watchlist, propose the most cost-effective streaming subscription (Based on 4 criteria : )

### Tech stack

- Logging system
- Command-Line Interface (with InquirePy)
- PostgreSQL database
- Backend API using FastAPI 
- Collecting the Data from The Movie Data Base's API
- CI/CD using Github workflows


## How to run the App

After opening the project, in the terminal , run the following instruction :

```
python start_application

```

By running this script you do these 4 steps :

- Installing the newer version of pip
- Installing all the requirements from requirements.txt
- Launching the webservice
- Launching the App


You can have access to the API with this [link](http://127.0.0.1:8000/docs)






## Demonstration

In this section, we present a way to test major features of our project.
