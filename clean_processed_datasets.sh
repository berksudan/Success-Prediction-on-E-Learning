#!/bin/bash

# GLOBAL VARIABLES ################################
DATASET_DIR="datasets"
BEFORE_LOGIN_DATASET_DIR="before_login_datasets"
AFTER_LOGIN_DATASET_DIR="after_login_datasets"

MERGED_FILE_DIR="merged_file_dir"
PAGE_VIEWS_FILE_DIR="page_views_dir"
VIDEO_VIEWS_FILE_DIR="video_views_dir"
# #################################################

PROJECT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DATASET_PATH="$PROJECT_PATH/$DATASET_DIR"

echo "Dataset path: $DATASET_PATH"

shopt -s extglob
# Clean processed files of before-login dataset.
rm -rv  $DATASET_PATH/$BEFORE_LOGIN_DATASET_DIR/$PAGE_VIEWS_FILE_DIR/!(*.zip)

# Clean processed files of after-login dataset.
rm -rv  $DATASET_PATH/$AFTER_LOGIN_DATASET_DIR/$PAGE_VIEWS_FILE_DIR/!(*.zip)
rm -rv  $DATASET_PATH/$AFTER_LOGIN_DATASET_DIR/$VIDEO_VIEWS_FILE_DIR/!(*.zip)
rm -rfv $DATASET_PATH/$AFTER_LOGIN_DATASET_DIR/$MERGED_FILE_DIR
