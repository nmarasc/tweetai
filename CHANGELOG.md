## [Unreleased]

- Database for generated tweets to prevent duplicates

## [1.0.3] - 2022-02-11

### Added
- Start script for running the container

### Changed
- Model training check arranged in a more sensible order

### Fixed
- Start time for fetching tweet data

## [1.0.2] - 2022-02-10

### Added
- Dockerfile for image building
- Build and release scripts to streamline docker builds

### Changed
- Project named changed to TweetAI as the code is generic

### Fixed
- Unique tweet check did not account for quotes in tweet data

## [1.0.1] - 2022-02-07

### Added
-

### Changed
- Adjust tweets posting to be on even hour cycle
- Pre generate tweet buffer on start

### Fixed
- Reset model after generating to reduce memory usage

## [1.0.0] - 2022-02-03

### Added
- Base model downloading
- Gathering tweet data
- Training model on the data
- Generating a buffer of about 10 tweets
- Posting tweets on a 2 hour cycle

### Changed
-

### Fixed
-
