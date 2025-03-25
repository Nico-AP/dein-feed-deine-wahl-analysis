# Dein Feed Deine Wahl Monitoring & Processing

This repository contains the code for the monitoring and processing of the Dein Feed Deine Wahl project.

## Prerequisites

To be able to run the scripts contained in this repository, make sure to:

### Install Dependencies

To run the monitoring script, first install the necessary dependencies (ideally in a virtual environment):

`pip install -r requirements.txt`


### Configure Environment Variables

To run the main script, you need to configure some environment variables in an .env script.

To do so, first copy the `.env.example` file:

``
cp .env.example .env  # Create a copy of the example file.
``

Then set the variables and you are good to go.


## Monitoring
For monitoring and retrieving the main data, you can use these four scripts:

1. `monitoring/scripts/generate_overview.py`: This script generates an overview of the participants and their donations, downloads all new / not yet locally saved donation. Its output is three fold:
    - A csv file in `./data/overview/overview_{timestamp}.csv` that contains the overview data (all donations attempts, incl. failed, non consent, incomplete, etc.).
    - A csv file in `./data/overview/usable_overview.csv` that contains the overview data of participants that have consented to donate their data and have donated and do have a watch history longer than zero videos.
    - All data doantions as jsons in `/data/donations/`
2. `monitoring/scripts/generate_monitoring_report.py`: This script generates a monitoring report of the participants and their donations. The report consists of two parts:
    - A print-out in the terminal on ...
        - ... the number of total started doantions, completed, and usefull once.
        - ... a print out of the basic demografic statistics. (Details on the encoding later in the README, !TODO!)
    - Four plots in `./plots/` ...
        - ... the number of donations by date.
        - ... the number of donations by date, but only for donations that were completed after 5am.
        - ... the distributions of datapoints by activity category (e.g., likes, comments, etc.).
        - ... the voting behaviour of participants (Erststimme und Zweitstimme).
3. `monitoring/scripts/pull_political_videos.py`: This script downloads all videos that are scraped on a daily basis from the database and saves them as `./data/political_videos.csv`. This only needs to be run once to set up the enviroment. It should take max. 20min, depending on your speed.
4. `monitoring/scripts/process_donations.py`: This script processes the donations and saves them as csvs in `./data/processed_donations/` if you prefer to work with them in that way.

### Running the scripts

To update the monitoring, run:

`python -m monitoring.scripts.generate_overview`

To generate the monitoring report, run:

`python -m monitoring.scripts.generate_monitoring_report`

To pull the political videos, run:

`python -m monitoring.scripts.pull_political_videos`

   The script supports the following command-line arguments:
   - `--date`: Filter videos by a specific date (format: YYYY-MM-DD)
   - `--username`: Filter videos by a specific TikTok username
   - `--output`: Specify a custom output file path (default: data/pol_videos.csv)
   
   Example usage:
   ```
   python -m monitoring.scripts.pull_political_videos --date 2023-05-01 --output /data/filtered_videos.csv
   ```

To process the donations to csv format, run:

`python -m monitoring.scripts.process_donations`


### How the generate_overview.py script works

This will:

1. Retrieve the participation overview through the 
[DDM Project Overview API](https://uzh.github.io/ddm/ddm/develop/researchers/topics/apis.html#_responses_api).
2. Retrieve the questionnaire responses through the 
[DDM Responses API](https://uzh.github.io/ddm/ddm/develop/researchers/topics/apis.html#_responses_api).
3. Gather the donated data for each participant if it has not been saved 
locally through the [DDM Donations API](https://uzh.github.io/ddm/ddm/develop/researchers/topics/apis.html#_responses_api).
4. Compute basic summary statistics and generate a csv file that holds 
information on the number of donated data points per blueprint and particiapnts, 
together with questionnaire responses and additional data. This is saved in
`./data/overview/overview_{timestamp}.csv`


### The encodings for the questionnaire responses are as follows:
The coding schemes are saved and easily accessible in the `monitoring/utils/coding_schemes.py` file.

- Q1_gender: 0 = Female, 1 = Male, 2 = Divers, 3 = Prefer not to say/ Don't know
- Q3_education: 0 = Noch in der Schule, 1 = Schule beendet ohne Abschluss, 2 = Volks- oder Hauptschulabschluss, 3 = Realschulabschluss/Mittlere Reife/Polytechnische Oberschule (oder vergleichbar), 4 = Abgeschlossene Lehre, 5 = Fachhochschulreife, 6 = Abitur/Hochschulreife, 7 = Hochschulabschluss (Universität/FH): Bachelor (oder vergleichbar), 8 = Hochschulabschluss (Universität/FH): Master, Magister, Diplom, Staatsexamen (oder vergleichbar), 9 = Hochschulabschluss (Universität/FH): Promotion, Habilitation (oder vergleichbar), 10 = Keine Angabe/weiß nicht
- Q4_location: Baden-Württemberg = 0, Bayern = 1, Berlin = 2, Brandenburg = 3, Bremen = 4, Hamburg = 5, Hessen = 6, Mecklenburg-Vorpommern = 7, Niedersachsen = 8, Nordrhein-Westfalen = 9, Rheinland-Pfalz = 10, Saarland = 11, Sachsen = 12, Sachsen-Anhalt = 13, Schleswig-Holstein = 14, Thüringen = 15, Ich lebe nicht in Deutschland = 16
- Q5_first_vote: 0 = SPD, 1 = CDU/CSU, 2 = Bündnis 90/Die Grünen, 3 = FDP, 4 = AfD, 5 = Die Linke, 6 = BSW, 7 = Andere Partei, 8 = Ungültig, 9 = Keine Angabe, 10 = Nicht wahlberechtigt, 11 = Nicht wählen
- Q6_second_vote: 0 = SPD, 1 = CDU/CSU, 2 = Bündnis 90/Die Grünen, 3 = FDP, 4 = AfD, 5 = Die Linke, 6 = BSW, 7 = Andere Partei, 8 = Ungültig, 9 = Keine Angabe, 10 = Nicht wahlberechtigt, 11 = Nicht wählen

Political and News Interest where added to the survey only after the launch, the variables are therefore not included for every participant (but for the majority of them)
- Q7_polInt-0 (Interest in Politics): 0 = Überhaupt nicht interessiert to 9 = Sehr stark interessiert
- Q7_polInt-1 (Interest in News): 0 = Überhaupt nicht interessiert to 9 = Sehr stark interessiert


## Metadata retrieval

To retrieve the scraped metadata for videos from the server, you can use the following function:

```
import json

from metadata.api_utils import get_video_metadata

video_id = '12345678910'
metadata = get_video_metadata(video_id)
print(json.dumps(metadata, indent=4))  # print or do something else with the data
```

Just make sure you have set the VIDEO_GET_ENDPOINT and AUTH_TOKEN variables in your .env file.

### Utility functions/scripts

In addition, there are also some utility functions/scripts available:

#### Extracting Video IDs for a specific participant

To extract a list of the videos a participant has watched, you can use the function 
`from metadata.utils import get_video_list_for_participant`.

The function is also available in the command line: 
`python -m metadata.utils.get_participant_videos -- participant_id=<participant ID>`
