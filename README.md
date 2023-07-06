# AutoAnalyst

AutoAnalyst is a self-service analytics suite that empowers users to draw actionable insights from their data using natural language. It can be tailored to work with a database and data catalog of your preference. Currently, AutoAnalyst supports Postgres, Redshift, BigQuery, and SQLite databases, with more being actively added. For data catalog, it supports CSV files at present, but compatibility with Alation and Datahub is being actively developed. A PyPi package for AutoAnalyst is in the works, but for now, the project can be set up locally using the instructions below.

## Local Setup

1. Clone this repository to your local machine.
2. Create a Python virtual environment.
3. Install the necessary dependencies with `pip install -r requirements.txt`.
4. Choose to follow either the demo setup or custom database setup instructions.

### Demo Setup

1. Update the `auto_analyst/config.json` file with your OpenAI API Key.
2. Run `python -m auto_analyst.app`.
3. Open a web browser and go to `localhost:5000`.

### Custom Database Setup

1. Update the `auto_analyst/config.json` file with your:
   - OpenAI API Key.
   - Flask secret key.
   - Database credentials.
   - Data catalog connection details.
2. Run `python -m auto_analyst.app`.
3. Open a web browser and go to `localhost:5000`.

Once AutoAnalyst is running, you should see something similar to this in your web browser:

![Screenshot of the demo](https://github.com/aadityaubhat/auto-analyst/blob/main/misc/auto_analyst.png)

## Demo

You can watch a comprehensive demo of the AutoAnalyst suite
[![IMAGE ALT TEXT HERE](https://github.com/aadityaubhat/auto-analyst/blob/main/misc/youtube_thumbnail.png)](https://www.youtube.com/watch?v=fp1nv-GdKic)

## Contributing

Contributions to the AutoAnalyst project are welcome and appreciated. If you're interested in contributing, please see our [CONTRIBUTING.md](CONTRIBUTING.md) guide. You'll find information on how to get started, our coding standards, and how to submit your changes for review. 

For major changes, please open an issue first to discuss what you would like to change. We encourage you to use the issues page for bug reports and feature requests.

Together, we can build a robust, intuitive, and versatile self-service analytics suite!
