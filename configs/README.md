# Dataset configurations

Here you can find some configurations of datasets that belong
to a specific problem.

## High Frequency Dataset

This dataset has some files with an high frequency. Those files are preferred
to be in cache. We construct this dataset to best fit the LFU algorithm.

### Steps summary

* Creates 2 set of files with different frequency distribution (using Poisson distribution with different lambda value):
  * More requested file max frequencies
  * Less requested files max frequencies

For each day:

* Shuffle all filenames
* Select a subset of files  (perc_file_x_day)
* Insert all files requests in base to the file frequency distribution above
* Random number between 0 to max frequency
* Shuffle all day requests

## Recency Focused Dataset

This dataset focus on files order and we construct it to fit LRU as best algorithm.

### Steps summary

For each day (until # of daily request is reached):

* Shuffle all filenames
* Select a subset of files  (perc_file_x_day)
* Insert all files requests in sequence
* Randomly invert file sequence (50%)

## Size Focused Dataset

Here we want to focus on a specific file size that is preferred for the files in cache.
The best target for this dataset are Size [Big, Small].

### Steps summary

* Generate a set of files with 2 different file size distribution

For each day (until # of daily request is reached):

* Shuffle all filenames
* Select a subset of files  (perc_file_x_day)
* Insert all files requests in sequence
* Note: the idea is that a group file with different size from the other is used as noise
