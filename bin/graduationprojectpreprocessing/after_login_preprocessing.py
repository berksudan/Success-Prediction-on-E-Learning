"""
########################### List of Process Tags  ################################
-> [CSV]: CSV format of input log.
-> [SF]: Given features are selected and others have been omitted.
-> [Sorted]: Data is sorted by 4 attribute respectively.
-> [ExCol]: Exchanged 2 given columns in csv file.
-> [VDur]: Extracted video durations in video views.
-> [FiNones]: If there is any absent item in csv file, fill with NONEs.
-> [FilteredPV]: Final summarized page views table with added session-durations, link-counts, unique-link-counts.
-> [FilteredVV]: Final summarized video views table with added video-durations, video-counts, unique-video-counts.
-> [NoNulls]: Removed the rows that contain 'NULL' word.
-> [CsvSepChanged]: CSV separator of the file has changed to another CSV separator (comma as default).
-> [NoOutl]: Outliers are omitted by using Pandas.
-> [Labeled]: Label data by using means of attributes.
-> [RemovedHeader]: Header is removed .
###################################################################################
"""

import sys
import zipfile

from preprocess_operations import PreProcessOperations as Ppo


def split_dir_filename(file_full_path: str):
    if file_full_path.__contains__('/'):  # Linux file separator.
        file_sep = '/'
    elif file_full_path.__contains__('\\'):  # Windows file separator.
        file_sep = '\\'
    else:  # Doesn't contain directory.
        return None

    file_dir_list = file_full_path.split(file_sep)[:-1]
    filename = file_full_path.split(file_sep)[-1:][0]
    file_dir = ''
    for file_dir_item in file_dir_list:
        file_dir += file_dir_item + file_sep
    return [file_dir, filename]


def process_page_views(repo_dir, pv_dataset):
    page_views_processes = ['CSV', 'SF', 'Sorted', 'FilteredPV']
    pv_file_names = Ppo.create_file_names_with_p_tags(repo_dir, pv_dataset, page_views_processes, out_extension='csv')
    Ppo.after_login_log_to_csv(pv_file_names[0])
    Ppo.select_features_in_csv(pv_file_names[1], selected_features=[1, 2, 3, 4, 5])  # ID feature is omitted.
    Ppo.sort_csv_by_header(pv_file_names[2], feature1='user_id', feature2='session_id', feature3='date',
                           feature4='time')
    Ppo.filter_page_views(pv_file_names[3], usr_idx=0, sid_idx=1, date_idx=2, time_idx=3, url_idx=4,
                          time_format='%H:%M:%S.%f', date_format='%Y-%m-%d')
    return pv_file_names[-1]


def process_video_views(repo_dir, vv_dataset):
    video_views_processes = ['CSV', 'FiNones', 'SF', 'Sorted', 'ExCol', 'VDur', 'FilteredVV']
    vv_file_names = Ppo.create_file_names_with_p_tags(repo_dir, vv_dataset, video_views_processes, out_extension='csv')
    Ppo.after_login_log_to_csv(vv_file_names[0])
    Ppo.fill_with_nones(vv_file_names[1])
    Ppo.select_features_in_csv(vv_file_names[2], selected_features=[1, 2, 3, 4, 5, 6, 7])  # ID feature is omitted.
    Ppo.sort_csv_by_header(vv_file_names[3], feature1='user_id', feature2='session_id', feature3='date',
                           feature4='time')
    Ppo.exchange_columns(vv_file_names[4], feature1='user_id', feature2='session_id')
    Ppo.extract_video_durations(vv_file_names[5], 'date', 'time', 'exit_date', 'exit_time',
                                time_format='%H:%M:%S.%f', date_format='%Y-%m-%d')
    Ppo.filter_video_views(vv_file_names[6], vid_id_idx=0, usr_idx=1, sid_idx=2, vid_dur_idx=5)
    return vv_file_names[-1]


def process_merged_file(repo_dir, mf_dataset, k_means_used: bool):
    merged_file_processes = ['NoNulls', 'CsvSepChanged', 'SF', 'NoOutl', 'Normalized', 'Labeled', 'RemovedHeader']
    mf_file_names = Ppo.create_file_names_with_p_tags(repo_dir, mf_dataset, merged_file_processes, out_extension='csv')
    Ppo.clear_rows_contain_null(mf_file_names[0], null_word='NULL')
    Ppo.change_csv_separator(mf_file_names[1])
    Ppo.select_features_in_csv(mf_file_names[2], [3, 6, 7])
    Ppo.remove_outliers(mf_file_names[3], low_bound=0.05, high_bound=0.95)
    Ppo.normalize_data(mf_file_names[4])
    Ppo.label_data(mf_file_names[5], feature1='unique_link_count', feature2='unique_vid_count',
                   feature3='total_vid_view', use_k_means=k_means_used)
    Ppo.finalize_merged_file(mf_file_names[6])

    return mf_file_names[-1]


def extract_dataset_from_zip(output_dir, dataset_name):
    path_to_zip_file = output_dir + dataset_name + ".zip"
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(output_dir)
    zip_ref.close()


def main(label_with_k_means: bool, pv_full_path: str, vv_full_path: str, merged_file_target: str, files_zipped: bool):
    page_views_dir = split_dir_filename(pv_full_path)[0]  # Directory of page-views files and its processed versions.
    page_views_dataset = split_dir_filename(pv_full_path)[1]
    video_views_dir = split_dir_filename(vv_full_path)[0]  # Directory of video-views files and its processed versions.
    video_views_dataset = split_dir_filename(vv_full_path)[1]

    merged_file_dir = merged_file_target + 'merged_file_dir/'  # Directory of merged files and its processed versions.

    if files_zipped:  # Extraction of text dataset file from zip to their path.
        page_views_dataset = page_views_dataset.replace('.zip', '')
        video_views_dataset = video_views_dataset.replace('.zip', '')
        extract_dataset_from_zip(page_views_dir, page_views_dataset)
        extract_dataset_from_zip(video_views_dir, video_views_dataset)

    # Process page-views and video-views.
    processed_pv = process_page_views(page_views_dir, pv_dataset=page_views_dataset)
    processed_vv = process_video_views(video_views_dir, vv_dataset=video_views_dataset)

    # Merge page-views and video-views, then process merged file.
    merged_file_dataset = Ppo.merge_video_page_views(merged_file_dir, processed_pv, processed_vv, uid_idx=0, sid_idx=1)
    processed_mf = process_merged_file(merged_file_dir, mf_dataset=merged_file_dataset, k_means_used=label_with_k_means)

    print('Name of Final Page Views:  \"%s\"' % processed_pv)
    print('Name of Final Video Views: \"%s\"' % processed_vv)
    print('Name of Final Merged File: \"%s\"' % processed_mf)
    print('Program has successfully terminated.')


if __name__ == '__main__':
    k_means_parameter = sys.argv[1]
    page_views_full_path = sys.argv[2]
    video_views_full_path = sys.argv[3]
    merged_file_target_dir = sys.argv[4]
    zip_parameter = sys.argv[5]

    use_k_means = None
    if k_means_parameter == '1':
        use_k_means = True
    elif k_means_parameter == '0':
        use_k_means = False
    else:
        exit("k_means_parameter is wrong. It must be 0 or 1.")

    are_files_zipped = None
    if zip_parameter == '1':
        are_files_zipped = True
    elif zip_parameter == '0':
        are_files_zipped = False
    else:
        exit("zip_parameter is wrong. It must be 0 or 1.")

    print('-' * 80)
    print('PARAMETERS:')
    print('-> Use KMeans Algorithm: <<%s>>' % use_k_means)
    print('-> Page-Views File Full Path: <<%s>>' % page_views_full_path)
    print('-> Video-Views File Full Path: <<%s>>' % video_views_full_path)
    print('-> Merged File Target Directory: <<%s>>' % merged_file_target_dir)
    print('-> Video and Page-Views Files are Zipped: <<%s>>' % are_files_zipped)
    print('-' * 80)

    main(use_k_means, page_views_full_path, video_views_full_path, merged_file_target_dir, are_files_zipped)
# python3 after_login_preprocessing.py 0 datasets/after_login_datasets/page_views_dir/pageViews.txt datasets/after_login_datasets/video_views_dir/videoViews.txt datasets/ 1
