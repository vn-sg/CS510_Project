#!/bin/bash

python3 baselines/subtask_1.py \
--train-file-path=/mnt/d/clef2022-checkthat-lab-main-task1/data/subtasks-english/CT22_english_1A_checkworthy/CT22_english_1A_checkworthy_train.tsv \
--dev-file-path=/mnt/d/clef2022-checkthat-lab-main-task1/data/subtasks-english/CT22_english_1A_checkworthy/CT22_english_1A_checkworthy_dev_test.tsv \
--subtask=checkworthy \
--lang=english