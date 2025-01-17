# Letterboxd Watchlist Merger Tool
This project takes one or more Letterboxd users and generates movie reccomendations from their watchlisted films. Input user names and the tool will parse their watchlists from their public Letterboxd profile, find the intersection of all users' watchlists, and save the Canadian streaming service with the license to each film.

## System Requirements
| Python Package | Min. Version |
|----------------|--------------|
| numpy          | 1.21.5       |
| pandas         | 2.2.3        |
| Requests       | 2.32.3       |
| beautifulsoup4 | 4.10.0       |

## Installation

Create a project directory under your home directory:
```bash
cd C:\ && mkdir -p watchlist_merger
```
Navigate to the new directory and clone the repsository from the project URL:
```bash
cd C:\watchlist_merger
git clone https://github.com/Luka626/watchlist_merger.git .
```
Install required packages via your tool of choice (pip shown):
```bash
cd C:\watchlist_merger
pip install -r requirements.txt
```
The tool is now installed.

> [!TIP]
> Speed up execution by downloading exports of users' Letterboxd data, use path to export in lieu of username in -u argument.

## Usage
- Navigate to the module and read the instructions:
```bash
cd C:\ && python3 watchlist_merger --help
```
- Run the program with user names following the -u tag:
````bash
cd C:\
python3 watchlist_merger -u user1 user2
````
- Inspect output:
````
cat intersection_watchlist.csv
````

> [!TIP]
> You can specify the output file with the -o argument.
