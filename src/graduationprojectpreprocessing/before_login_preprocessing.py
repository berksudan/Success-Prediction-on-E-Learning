"""
########################## List of Process Tags  ################################
-> [CSV]: CSV format of input log
-> [NoBots]: Crawler that visited the page have been removed.
-> [SF]: Given features are selected and others have been omitted.
-> [UserIDs]: User ids are extracted according to their IP and User-Agent info.
-> [Sorted]: Data is sorted by 3 attribute respectively.
-> [SessionIDs]: Session ids are extracted according to delta time between logs that has same User-ID.
-> [AllPages]: Logs contains image, redirected links and non-pages have been omitted.
-> [FilteredPV]: Final summarized page views table with added session-durations, unique-link-counts, link-counts.
#################################################################################
"""
import zipfile

from preprocess_operations import PreProcessOperations as Ppo


def process_page_views(repo_dir, pv_dataset):
    page_views_processes = ['CSV', 'NoBots', 'SF', 'UserIDs', 'Sorted', 'AllPages', 'SessionIDs', 'FilteredPV']
    pv_file_names = Ppo.create_file_names_with_p_tags(repo_dir, pv_dataset, page_views_processes, out_extension='csv')

    Ppo.before_login_log_to_csv(pv_file_names[0])
    Ppo.clean_bots_from_csv(pv_file_names[1], user_agent_idx=9)
    Ppo.select_features_in_csv(pv_file_names[2], selected_features=[0, 1, 4, 8, 9, 10])
    users_dict = Ppo.extract_usr_ids(pv_file_names[3], ip_idx=3, usr_agent_idx=4)
    Ppo.write_usr_ids(pv_file_names[3], users_dict, ip_idx=3, usr_agent_idx=4)
    Ppo.sort_csv_by_header(pv_file_names[4], feature1='user_id', feature2='date', feature3='time', feature4=None)
    Ppo.clean_non_page_links_from_csv(pv_file_names[5], uid_idx=0, date_idx=1, time_idx=2, url_idx=3)
    Ppo.calc_session_ids(pv_file_names[6], user_id_idx=0, date_idx=1, time_idx=2, time_format='%H:%M:%S',
                         date_format='%Y-%m-%d')
    Ppo.filter_page_views(pv_file_names[7], usr_idx=1, sid_idx=0, date_idx=2, time_idx=3, url_idx=4,
                          time_format='%H:%M:%S', date_format='%Y-%m-%d')
    return pv_file_names[len(page_views_processes)]


def extract_dataset_from_zip(output_dir, dataset_name):
    path_to_zip_file = output_dir + dataset_name + ".zip"
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(output_dir)
    zip_ref.close()


def main():
    ds_dir = 'datasets/before_login_datasets/'  # Directory of dataset files
    page_views_dir = ds_dir + 'page_views_dir/'
    page_views_dataset = 'u_extend15.log'  # name of log dataset.

    extract_dataset_from_zip(page_views_dir, page_views_dataset)

    processed_pv = process_page_views(repo_dir=page_views_dir, pv_dataset=page_views_dataset)

    print('Name of Final Page Views:  \"%s\"' % processed_pv)
    print('Program has successfully terminated.')


if __name__ == '__main__':
    main()
