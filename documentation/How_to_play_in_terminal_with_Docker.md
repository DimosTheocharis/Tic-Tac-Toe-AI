## How to play Tic-Tac-Toe in the terminal, using Docker ##

Docker is a technology that helps you create and manage containers. Containers are packages that contain the code and all the dependencies that an app needs in order to run without problems. With this approach, you don't need to install python in your computer or any other depenency that Tic-Tac-Toe-AI needs.

### Step 1. Instal Docker Desktop ###

##### A) Head to the official Docker Desktop website: https://docs.docker.com/get-docker/ #####

##### B) Select your platform #####

Choose the download package that is specific to your operating system. In my case, i use Windows.

![choose_your_platform](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/BackendDocumentation/screenshots/how_to_download_docker_desktop/choose_your_platform.png) 

##### C) Click the download button #####

![click_download_button](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/BackendDocumentation/screenshots/how_to_download_docker_desktop/click_download_button.png) 

##### D) Run the .exe that got downloaded and follow the steps of the download wizard. #####

### Step 2. Clone Project ###

##### A) Copy the project url #####

![copy_clone_url](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/BackendDocumentation/screenshots/how_to_run_backend/copy_clone_url.png)  

##### B) Open a text editor and clone the project #####

Here i opened Visual Studio Code in a new window (File > New Window).

![clone_project](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/BackendDocumentation/screenshots/how_to_run_backend/clone_project.png)  


### Step 3. Open Docker Desktop ###

##### A) Find and open the Docker Desktop app  #####

![open_docker_desktop](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/BackendDocumentation/screenshots/how_to_run_backend/open_docker_desktop.png)

### Step 4. Run the project using Docker ###

##### A) Open the cloned project #####

You should head to the folder "Tic-Tac-Toe-AI" where `dockerfile` file is located. You may run 

```
    ls
```

in order to assure that you are in the correct folder.

![head_to_backend_folder](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/BackendDocumentation/screenshots/how_to_run_backend/head_to_backend_folder_2.png)

##### B) Open the terminal and run: #####

```
    docker-compose up
```

This command will run the code in the `docker-compose.yaml` file, build the image specified there and run a container that includes your code and the dependencies (python3 for example)

## Step 5. Play the game ##

##### A) Decide your move #####

For example here i placed my symbol 'X' in the third column (column = 2) of the first row (row = 0).

![make_your_move](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/BackendDocumentation/screenshots/how_to_run_backend/make_your_move.png)  

##### B) Wait for the algorithm to play #####

Here the algorithm responded with a move at (row, column) = (1, 1), right in the middle of the grid.

![algorithm_makes_its_move](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/BackendDocumentation/screenshots/how_to_run_backend/algorithm_makes_its_move.png)  

##### C) Repeat until game is ended #####


