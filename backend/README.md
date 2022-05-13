# Task 1: Identifying Relevant Claims in Tweets

This repository contains the _dataset_, _format checker, scorer and baselines_ for the [CLEF2022-CheckThat! Task 1](https://sites.google.com/view/clef2022-checkthat/tasks/task-1-fighting-the-covid-19-infodemic).
In this task, we focus on the **classification** of tweets in different languages (i.e., Arabic, Bulgarian, Dutch, English, Spanish, Turkish) and different subtasks: (i) Check-worthiness, (ii) Verifiable factual claims detection, (iii) Harmful tweet detection, and (iv) Attention-worthy tweet detection.


This file contains the basic information regarding the CLEF2022-CheckThat! Task 1 on Fighting the COVID-19 Infodemic on tweets provided for the CLEF2022-CheckThat! Lab on "Fighting the COVID-19 Infodemic and Fake News Detection". The current version is listed bellow corresponds to the release of the training, dev, and dev_test data sets. The dev can be used to fine-tune the model and dev_test can be used to evaluate the performance of the model. The final evaluation will be based on the final test set.



__Table of contents:__
- [Evaluation Results](#evaluation-results)
- [List of Versions](#list-of-versions)
- [Contents of the Task 1 Directory](#contents-of-the-repository)
- [Input Data Format](#input-data-format)
	<!-- - [Subtask 1A: Check-Worthiness of Tweets](#subtask-1a-check-worthiness-of-tweets) -->
	<!-- - [Subtask 1B: Check-Worthiness of Debates/Speeches](#subtask-1b-check-worthiness-of-debatesspeeches) -->
- [Output Data Format](#output-data-format)
	<!-- - [Subtask 1A: Check-Worthiness of Tweets](#subtask-1a-check-worthiness-of-tweets-1) -->
	<!-- - [Subtask 1B: Check-Worthiness of Debates/Speeches](#subtask-1b-check-worthiness-of-debatesspeeches-1) -->
- [Format Checkers](#format-checkers)
	<!-- - [Subtask 1A: Check-Worthiness of Tweets](#subtask-1a-check-worthiness-of-tweets-2) -->
	<!-- - [Subtask 1B: Check-Worthiness of Debates/Speeches](#subtask-1b-check-worthiness-of-debatesspeeches-2) -->
- [Scorers](#scorers)
	<!-- - [Subtask 1A: Check-Worthiness of Tweets](#subtask-1a-check-worthiness-of-tweets-3) -->
	<!-- - [Subtask 1B: Check-Worthiness of Debates/Speeches](#subtask-1b-check-worthiness-of-debatesspeeches-3) -->
- [Evaluation Metrics](#evaluation-metrics)
- [Baselines](#baselines)
	<!-- - [Subtask 1A: Check-Worthiness of Tweets](#subtask-1a-check-worthiness-of-tweets-4) -->
	<!-- - [Subtask 1B: Check-Worthiness of Debates/Speeches](#subtask-1b-check-worthiness-of-debatesspeeches-4) -->
- [Credits](#credits)

## Evaluation Results

<!-- Kindly find the leaderboard released in this google sheet, [link](https://tinyurl.com/kfmawuke). you can find in the tab labeled "Task 1". -->

<!-- Submission Guidelines:
- Make sure that you create one account for each team, and submit it through one account only.
- The last file submitted to the leaderboard will be considered as the final submission.
- The output file has to have a `.tsv` extension; otherwise, you will get an error on the leaderboard.
- You need to write a small description of the model submitted in a `.txt` file.
- You have to zip the tsv, `zip submission.zip path_to_tsv_pred_file_1.tsv path_to_tsv_pred_file_2.tsv ... path_to_tsv_pred_file_n.tsv model_description.txt` and submit it through the codalab page.

All leaderboard for dev and test data can be found here, https://competitions.codalab.org/competitions/30853.

*NOTE*: The leaderboard for the Spanish test data is found in a separate leaderboard, https://competitions.codalab.org/competitions/31262. -->


## List of Versions
* __subtask-1a-1b-1c-1d [2022/02/23]__
 - Training/Dev/Dev_Test data for subtasks 1a, 1b, 1c and 1d released for Arabic, Bulgarian, Dutch, and English. For Spanish only subtask 1a Training/Dev/DEV_Test data released. For Turkish Training/DEV data released.


## Contents of the Task 1 Directory
In each directory, we provide task-specific zip files. Each zip file contains train, dev, and dev_test data released with the tweets and the labels assigned. We provide a single JSON file for the majority of the languages. The tweet id can be used to match the data between the TSV file and the JSON files. 

**Notice** Many instances in the TSV file might not have a corresponding entry in the JSON file. This is due to the deletion of tweets during the compilation of the datasets.

* Main folder: [data](./data)
  * Subfolder: [subtasks-arabic](./data/subtask-arabic)
  	This directory contains files for all subtasks for the Arabic language.

  * Subfolder: [subtasks-bulgarian](./data/subtasks-bulgarian)
  	This directory contains files for all subtasks for the Bulgarian language.

  * Subfolder: [subtasks-dutch](./data/subtask-dutch)
  	This directory contains files for all subtasks for the Dutch language.

  * Subfolder: [subtasks-english](./data/subtasks-english)
  	This directory contains files for all subtasks for the English language.

  * Subfolder: [subtask-1A--spanish](./data/subtasks-spanish)
  	This folder contains files for Subtask 1A for the Spanish language.

  * Subfolder: [subtask-1A--turkish](./data/subtasks-turkish)
  	This directory contains files for all subtasks for the Turkish language. Note that, we will soon release data for other subtasks and JSON file is not available for subtask 1A.


* Main folder: [baselines](./baselines)<br/>
	Contains scripts provided for baseline models of the tasks
* Main folder: [formet_checker](./format_checker)<br/>
	Contains scripts provided to check format of the submission file
* Main folder: [scorer](./scorer)<br/>
	Contains scripts provided to score output of the model when provided with label (i.e., dev set).

* [README.md](./README.md) <br/>
	This file!


## Input Data Format

<!-- ### Subtask 1A: Check-Worthiness of Tweets -->
For all languages (**Arabic**, **Bulgarian**, **Dutch**, **English**, **Spanish** and  **Turkish**) and for all subtasks we use the same data format in the train, dev and dev_test files. Each file is TAB seperated (TSV file) containing the tweets and their labels. The text encoding is UTF-8. Each row in the file has the following format:

> topic <TAB> tweet_id <TAB> tweet_url <TAB> tweet_text <TAB> class_label

Where: <br>
* topic: unique ID for the topic the tweet is about <br/>
* tweet_id: Tweet ID for a given tweets given by Twitter <br/>
* tweet_url: URL to the given tweet <br/>
* tweet_text: content of the tweet <br/>
* class_label:
 * subtasks (1A, 1B, 1C): *yes* and *no*
 * subtask (1D):
  * *no_not_interesting*,
	* *yes_asks_question*,
	* *yes_blame_authorities*,
	* *yes_calls_for_action*,
	* *harmful*,
	* *yes_contains_advice*,
	* *yes_discusses_action_taken*,
	* *yes_discusses_cure*,
	* *yes_other*


**Examples:**
> covid-19	1235648554338791427	https://twitter.com/A6Asap/status/1235648554338791427	COVID-19 health advice⚠️ https://t.co/XsSAo52Smu	0<br/>
> covid-19	1235287380292235264	https://twitter.com/ItsCeliaAu/status/1235287380292235264	There's not a single confirmed case of an Asian infected in NYC. Stop discriminating cause the virus definitely doesn't. #racist #coronavirus https://t.co/Wt1NPOuQdy	1<br/>
> covid-19	1236020820947931136	https://twitter.com/ddale8/status/1236020820947931136	Epidemiologist Marc Lipsitch, director of Harvard's Center for Communicable Disease Dynamics: “In the US it is the opposite of contained.' https://t.co/IPAPagz4Vs	1<br/>
> ... <br/>

Note that the gold labels for the task are the ones in the *class_label* column


## Output Data Format
For all languages (**Arabic**, **Bulgarian**, **Dutch**, **English**, **Spanish** and  **Turkish**) and subtasks the data format is the same, which includes submission files.

For each subtask, the expected results file is a list of tweets with the class label for the particular subtask. Each row contains four TAB separated fields:

> topic <TAB> tweet_id <TAB> class_label <TAB> run_id

Where: <br>
* topic: unique ID for the topic the tweet is about given in the test dataset file <br/>
* tweet_id: Tweet ID for a given tweets given by Twitter given in the test dataset file<br/>
* class_label: class label for the particular subtask <br/>
* run_id: string identifier used by participants. <br/>

Example:
> covid-19	1235648554338791427	0  Model_1<br/>
> covid-19	1235287380292235264	1  Model_1<br/>
> covid-19	1236020820947931136	0  Model_1<br/>
> ... <br/>



## Format Checkers
The checker for the subtask is located in the [format_checker](./format_checker) module of the project.
To launch the baseline script you need to install packages dependencies found in [requirement.txt](./requirement.txt) using the following:
> pip3 install -r requirements.txt <br/>

The format checker verifies that your generated results files complies with the expected format.
To launch it run:
> python3 format_checker/main.py --subtask=<name_of_the_subtask> --pred-files-path=<path_to_result_file_1 path_to_result_file_2 ... path_to_result_file_n> <br/>

or
> python3 format_checker/subtask_1.py --pred-files-path=<path_to_result_file_1 path_to_result_file_2 ... path_to_result_file_n> <br/>

`--pred-files-path` take a single string that contains a space separated list of file paths. The lists may be of arbitrary positive length (so even a single file path is OK) but their lengths must match.

__<path_to_result_file_n>__ is the path to the corresponding file with participants' predictions, which must follow the format, described in the [Output Data Format](#subtask-1a-check-worthiness-of-debatesspeeches-1) section.

Note that the checker can not verify whether the prediction files you submit contain all lines / claims), because it does not have access to the corresponding gold file.


## Scorers
The scorer for the subtask is located in the [scorer](./scorer) module of the project.
To launch the script you need to install packages dependencies found in [requirement.txt](./requirement.txt) using the following:
> pip3 install -r requirements.txt <br/>

Launch the scorer for the subtask as follows:
> python3 scorer/subtask_1.py --gold-file-path=<path_gold_file> --pred-file-path=<predictions_file> --subtask=<name_of_the_subtask><br/>

The scorer invokes the format checker for the subtask to verify the output is properly shaped.
It also handles checking if the provided predictions file contains all lines/tweets from the gold one.


## Baselines

The [baselines](./baselines) module contains a majority, random and a simple ngram baseline for each subtask.
To launch the baseline script you need to install packages dependencies found in [requirement.txt](./requirement.txt) using the following:
> pip3 install -r requirements.txt <br/>

To launch the baseline script run the following:
> python3 baselines/subtask_1a.py --train-file-path=<path_to_your_training_data> --test-file-path=<path_to_your_test_data_to_be_evaluated> --subtask=<name_of_the_subtask> --lang=<language_of_the_subtask_1a><br/>

All baselines will be trained on the training tweets and the performance of the model was evaluated on the test tweets.
<!-- The MAP score of both baselines are as follows:<br/>
| Model | English | Arabic | Spanish | Bulgarian |
| :---: | :---: | :---: | :---: | :---: |
| Random Baseline | 0.4795 |  | 0.0806 | 0.2045 |
| Ngram Baseline  | 0.5916 |  | 0.4122 | 0.4729 | -->



## Credits

<!-- Task 1 Organizers: TBA -->

Task website: https://sites.google.com/view/clef2022-checkthat/tasks/task-1-identifying-relevant-claims-in-tweets

Contact:   clef-factcheck@googlegroups.com
