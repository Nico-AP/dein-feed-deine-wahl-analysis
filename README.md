# Dein Feed Deine Wahl Monitoring


## Prerequisites

### Install Dependencies

To run the monitoring script, first install the necessary dependencies:

`pip install -r requirements.txt`


### Configure Environment Variables

To run the main script, you need to configure some environment variables in an .env script.

To do so, first copy the `.env.example` file:

``
cp .env.example .env  # Create a copy of the example file.
``

Then set the variables and you are good to go.


## Running the Monitoring Script

To update the monitoring, run:

`python generate_overview.py`


### How it works

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
`/data/overview/overview_{timestamp}.csv`

