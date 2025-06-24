# Daily Article Generator

This tool generates a configurable number of daily news articles for the Mackney Gazette.

## Overview

The daily article generator allows you to:

1. Generate a configurable number of news articles
2. Back up your existing articles before generating new ones
3. Limit the total number of articles to keep in the database
4. Customize the distribution of article types and seriousness

## Configuration

You can customize the article generation parameters by editing the configuration file:
`articles_daily_config.yaml`

Available parameters:

- **Article Generation Settings**
  - Count: Number of articles to generate per day
  - Priority categories: Categories to prioritize when generating articles
  - Seriousness weights: Distribution of article seriousness (serious, balanced, light)
  - Story status weights: Distribution of story status (breaking, ongoing, follow-up)

- **Save Options**
  - Backup before save: Whether to back up the articles CSV before adding new ones
  - Article limit: Maximum number of articles to keep (0 = unlimited)

## Usage

Run the article generator with:

```bash
./generate_articles_daily.sh
```

Or with a custom configuration file:

```bash
./generate_articles_daily.sh --config path/to/custom_config.yaml
```

## Output

The tool generates articles and saves them to the articles database file:

`data/articles.csv`

These articles will be used by the newspaper application for content display.

## Note

- Article generation can take some time, especially if you're generating multiple articles
- The article generator uses the town and people data, so make sure to run the town initialization script first if you haven't already
