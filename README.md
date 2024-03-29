# dataset-generator
A generator of test datasets

## How to use

Install the dependencies:

```bash
pip install -e requirements.txt
```

Start the UI and open [localhost](http://127.0.0.1:8050/):

```bash
python main.py --ui
```

> **NOTE 0**: the UI starts in debug mode as default  
> **NOTE 1**: it is possible to open the dataset already created to inspect them
> just using the load button with the same folder name of the generated dataset

You can use also the script mode passing a valid configuration as in the following
example:

```bash
python dataset_generator.py gen configs/HighFreqDataset.json --dest-folder ./dataset
```

### Configuration example

```json
{
    "seed": 42,
    "num_days": 90,
    "num_req_x_day": 1000,
    "dest_folder": "HighFrequencyDataset",
    "function": {
        "function_name": "HighFrequencyDataset",
        "kwargs": {
            "num_files": 100000,
            "min_file_size": 100,
            "max_file_size": 24000,
            "lambda_less_req_files": 1.0,
            "lambda_more_req_files": 10.0,
            "perc_more_req_files": 10.0,
            "perc_files_x_day": 1.0,
            "size_generator_function": "gen_random_sizes"
        }
    }
}
```

> **NOTE**: the `function_name` have to be a valid `GenFunction` derived class and
the kwargs are the input passed to the `__init__` function.
