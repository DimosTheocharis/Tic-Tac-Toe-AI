## How to play Tic-Tac-Toe in the terminal, using Docker ##

Docker is a technology that helps you create and manage containers. Containers are packages that contain the code and all the dependencies that an app needs in order to run without problems. With this approach, you don't need to install python in your computer or any other dependency that Tic-Tac-Toe-AI needs.

##### Prerequisites #####

- Git -> In order to clone project
- Visual Studio Code -> (or other text editor)
- WSL (Windows Subsystem for Linux) -> In order for Docker Desktop to work in Windows

### Step 1. Instal Docker Desktop ###

##### A) Head to the official Docker Desktop website: https://docs.docker.com/get-docker/ #####

##### B) Select your platform #####

Choose the download package that is specific to your operating system. In my case, i use Windows.

![choose_your_platform](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/main/screenshots/how_to_download_docker_desktop/choose_your_platform.png) 

##### C) Click the download button #####

![click_download_button](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/main/screenshots/how_to_download_docker_desktop/click_download_button.png) 

##### D) Run the .exe that got downloaded and follow the steps of the download wizard. #####

##### E) Checkout the other requirements that Docker Desktop needs #####

For example, in Windows the Windows Subsystem for Linux (WSL) is required in order for the Docker Desktop to run. You can find all requirements in the "System requirements" page.

### Step 2. Clone Project ###

##### A) Copy the project url #####

![copy_clone_url](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/main/screenshots/how_to_run_backend/copy_clone_url.png)  

##### B) Open a text editor and clone the project #####

Here i opened Visual Studio Code in a new window (File > New Window).

![clone_project](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/main/screenshots/how_to_run_backend/clone_project.png)  


### Step 3. Open Docker Desktop ###

##### A) Find and open the Docker Desktop app  #####

![open_docker_desktop](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/main/screenshots/how_to_run_backend/open_docker_desktop.png)

### Step 4. Run the project using Docker ###

##### A) Open the cloned project #####

Open the project with Visual Studio Code: File > Open Folder. You should head to the folder "Tic-Tac-Toe-AI" where `backend_dockerfile` file is located. You may run 

```
    ls
```

in order to assure that you are in the correct folder.

![head_to_backend_folder](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/main/screenshots/how_to_run_backend/head_to_backend_folder_2.png)

##### B) Create an image of the project #####

Open a terminal and run:

```
    docker build -t terminal-game:v1 -f backend_dockerfile .
```

This command will run the code in the `backend_dockerfile` file. It will create an image of the project (called "terminal-game:v1"), ie a shared package containing the code of the project and the instructions to run it.

**Note** Don't forget the '.' in the end of the command. It tells Docker to look for the `dockerfile` in the same directory you are now.

**Note:** Keep in mind that this might take a time.

##### B) Create a container based on the image #####

In the terminal run:

```
    docker run --name terminal-first -i -t terminal-game:v1
```

This command will create a container called "terminal-first" based on the image you created previously. This container is just a snapshot of the image and also the final executable product that will let you play Tic-Tac-Toe-AI.

This command will also run the container in interactive mode, in order to let you give inputs to the program. 

## Step 5. Play the game ##

##### A) Decide your move #####

For example here i placed my symbol 'X' in the third column (column = 2) of the first row (row = 0).

![make_your_move_with_docker](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/main/screenshots/how_to_run_backend/make_your_move_with_docker.png)  

##### B) Wait for the algorithm to play #####

Here the algorithm responded with a move at (row, column) = (1, 1), right in the middle of the grid.

![algorithm_makes_its_move](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/main/screenshots/how_to_run_backend/algorithm_makes_its_move.png)  

##### C) Repeat until game is ended #####

![game_is_terminated](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/main/screenshots/how_to_run_backend/game_is_terminated.png)  

## Step 6. Play game again ##

This step is optional, and is about the beginning of a new game of "Tic-Tac-Toe AI"

##### A) Start the container #####

When you previously finished the game, the container that was up went off, it terminated. In order for you to play again
you have to start the same container again, by running:

```
    docker start -i terminal-first
```

![start_container_again](https://github.com/DimosTheocharis/Tic-Tac-Toe-AI/blob/main/screenshots/how_to_run_backend/start_container_again.png)  


## Step 7. Clear Data ##

This step is optional and involves deleting the image and the container that got created for the project.

##### A) Delete the container #####

In a terminal run (Docker Desktop should be open)

```
    docker container rm terminal-first
```

##### B) Delete the image #####

In a terminal run (Docker Desktop should be open)

```
    docker image rmi terminal-game:v1
```