# Tour Planner AI Agent

This project provides a small interactive command-line assistant that helps you discover interesting places to visit in any destination city.

It relies on the free [OpenTripMap](https://opentripmap.io/) API to retrieve points of interest (POI) and present short Wikipedia-style descriptions.

## Setup

1. **Clone / open the project**

2. Install Python dependencies (preferably in a virtualenv):

```bash
pip install -r requirements.txt
```

3. Obtain a free API key from OpenTripMap and expose it as an environment variable:

```bash
export OPENTRIPMAP_API_KEY="YOUR_KEY_HERE"
```

## Usage

Run the interactive assistant:

```bash
python tour_planner.py
```

You will be prompted for a destination city. The tool will then list nearby places within a 5-kilometre radius. Choose a place's number to read more details, press `n` for a new city, or `q` to quit.

## Example session

```
$ python tour_planner.py
============================
  Welcome to Tour Planner!  
============================

Enter a destination city (or 'q' to quit): Paris

Found Paris at (lat 48.8534, lon 2.3488).
Searching for interesting places within 5 km…
+----+---------------------------+------------------------------------------+-----------+
| #  | Place                     | Kinds                                    | Distance  |
+====+===========================+==========================================+===========+
| 1  | Eiffel Tower             | architecture, towers, cultural, historic | 354 m     |
| 2  | Louvre Museum            | museums, cultural, architecture          | 890 m     |
| …  | …                         | …                                        | …         |
+----+---------------------------+------------------------------------------+-----------+

Enter the # of a place to learn more, 'n' for new place, or 'q' to quit: 1
============================================================
Eiffel Tower
============================================================
Kinds: architecture,towers,cultural,historic

The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France…

More info: https://www.toureiffel.paris/
============================================================
```

Enjoy planning your next trip! :)
