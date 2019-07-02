import os

import pandas

from KMeans import KMeans
from time_operations import TimeOperations

__beg_csv_sep__ = '|'  # CSV separator at the beginning which used for initial pre-processing operations.
__final_csv_sep__ = ','  # Final CSV separator which used for finalized pre-processed file.


# ################### UTILITY METHODS #####################
def is_nav_link(url):
    web_page_ext = {'00asp', '0aspx', '0ashx', '00htm', '0html', 'shtml',  # web page extensions
                    'xhtml', '00php', '00jsp', '0jspx', '000pl', '00cgi'}
    extension_size = 5

    url_splitted = url.rsplit('.', 1)
    if len(url_splitted) == 1:
        return False

    url_ext_part = url_splitted[1]

    if extension_size > len(url_ext_part):
        url_extension = '0' * (extension_size - len(url_ext_part)) + url_ext_part  # Fill with zeroes.
    else:
        url_extension = url_ext_part[:extension_size]

    if web_page_ext.__contains__(url_extension.lower()):  # does have an extension
        return True
    return False


def is_eof(fp):
    cur_pos = fp.tell()
    a_line = fp.readline()
    fp.seek(cur_pos)
    return a_line == ''


def list_to_csv_line(a_list):  # Concatenates items of a list by using csv separator
    csv_sep = PreProcessOperations.current_csv_sep
    line = ''
    for item in a_list:
        line += str(item) + csv_sep
    return line[:-len(csv_sep)]  # Remove last separator character


def line_to_list(a_line):
    csv_sep = PreProcessOperations.current_csv_sep
    return a_line[:-1].split(csv_sep)  # omit new line character at the end & split


def transform_csv_header(old_csv_header):
    csv_sep = PreProcessOperations.current_csv_sep
    old_csv_header = old_csv_header.lower()
    csv_header_line = reduce_multiple_spaces(old_csv_header)
    csv_header_replacements_tuples = [('kullaniciid', 'user_id'), ('loginid', 'session_id'),
                                      ('cikistarih', 'exit_date exit_time'), ('videoid', 'video_id'),
                                      ('tarih', 'date time')]
    for old_feature, new_feature in csv_header_replacements_tuples:
        csv_header_line = csv_header_line.replace(old_feature, new_feature)

    return csv_header_line.replace(' ', csv_sep)


def link_contains_image(url):
    img_extensions = {'.png', '.jpg', '.ico', '.gif'}

    if img_extensions.__contains__(url[-4:]):
        return True
    return False


def display_func_exit_msg(output_file, func_name):
    print('> %s(..) terminated and new file named \'%s\' created.' % (func_name, output_file))
    print('-' * 80)


def reduce_multiple_spaces(a_string):
    return ' '.join(a_string.split())


def generate_uid_sid_primary_key(csv_row_list, uid_idx, sid_idx, num_of_digits):
    # Generates primary key of user-id + session-id .
    if not csv_row_list[0]:  # if csv_row_list is empty
        return 0, 0
    format_string = '{0:0=' + str(num_of_digits) + 'd}'
    user_id = int(csv_row_list[uid_idx])
    session_id = int(csv_row_list[sid_idx])
    uid_sid_primary_key = format_string.format(user_id), format_string.format(session_id)

    return uid_sid_primary_key

# ########################################################


class PreProcessOperations:
    current_csv_sep = __beg_csv_sep__  # Beginning-CSV-Separator is set as default.

    @staticmethod
    def create_file_names_with_p_tags(repo_dir, dataset, process_tags, out_extension):
        file_names = [repo_dir + dataset]
        ds_name = dataset.split('.')[0]

        cumulative_process_tags = ['[%s]' % process_tags[0]]
        for i in range(1, len(process_tags)):
            cumulative_process_tags.append('%s[%s]' % (cumulative_process_tags[i - 1], process_tags[i]))

        for tag in cumulative_process_tags:
            file_names.append('%s%s%s.%s' % (repo_dir, ds_name, tag, out_extension))

        return file_names

    @staticmethod
    def extract_video_durations(csv_file, d1_feature, t1_feature, d2_feature, t2_feature, time_format, date_format,
                                process_tag='VDur'):
        csv_sep = PreProcessOperations.current_csv_sep
        t_o = TimeOperations(time_format, date_format)

        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')
        input_csv = open(csv_file)
        output_csv = open(new_csv_file, 'w')

        csv_header = input_csv.__next__()  # pass csv header

        csv_header_list = line_to_list(csv_header)
        d1_idx = csv_header_list.index(d1_feature)
        t1_idx = csv_header_list.index(t1_feature)
        d2_idx = csv_header_list.index(d2_feature)
        t2_idx = csv_header_list.index(t2_feature)

        csv_header = csv_header.replace(csv_sep + t2_feature, '')  # Delete t2_feature
        csv_header = csv_header.replace(d2_feature, 'video_duration')  # Add new feature called 'video_duration'
        output_csv.write(csv_header)  # Write new header to first row of the file.

        for line in input_csv:
            line_list = line_to_list(line)

            if line_list[d2_idx] == 'NONE':  # If exit date of video is NONE.
                video_duration = 1  # Video duration is unknown, so we assume that it's 1 second.
            else:
                list2 = [line_list[d2_idx], line_list[t2_idx]]
                list1 = [line_list[d1_idx], line_list[t1_idx]]
                video_duration = t_o.calc_time_diff(list2, list1, date_idx=0, time_idx=1)

            line_list.remove(line_list[t2_idx])
            line_list[d2_idx] = video_duration
            output_csv.write(list_to_csv_line(line_list) + '\n')

        input_csv.close()
        output_csv.close()
        display_func_exit_msg(output_file=new_csv_file, func_name='extract_video_durations')
        return new_csv_file

    @staticmethod
    def fill_with_nones(csv_file, process_tag='FiNones'):  # Fill absent items with NONEs.
        csv_sep = PreProcessOperations.current_csv_sep
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')

        input_csv = open(csv_file)
        output_csv = open(new_csv_file, 'w')

        csv_header = input_csv.__next__()  # pass csv header
        output_csv.write(csv_header)  # Write same header to first row of the file.

        csv_col_size = csv_header.count(csv_sep) + 1

        for line in input_csv:
            line = line.replace('NULL', 'NONE')
            line_col_size = line.count(csv_sep) + 1
            line_list = line_to_list(line)

            for i in range(csv_col_size - line_col_size):
                line_list.append('NONE')
            output_csv.write(list_to_csv_line(line_list) + '\n')

        input_csv.close()
        output_csv.close()
        display_func_exit_msg(output_file=new_csv_file, func_name='fill_with_nones')
        return new_csv_file

    @staticmethod
    def exchange_columns(csv_file, feature1, feature2, process_tag='ExCol'):
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')

        input_csv = open(csv_file)
        output_csv = open(new_csv_file, 'w')

        header_items = line_to_list(input_csv.__next__())
        item1_idx = header_items.index(feature1)
        item2_idx = header_items.index(feature2)

        header_items[item1_idx], header_items[item2_idx] = header_items[item2_idx], header_items[item1_idx]  # Swap
        output_csv.write(list_to_csv_line(header_items) + '\n')

        for line in input_csv:
            line_items = line_to_list(line)
            line_items[item1_idx], line_items[item2_idx] = line_items[item2_idx], line_items[item1_idx]  # Swap

            output_csv.write(list_to_csv_line(line_items) + '\n')

        input_csv.close()
        output_csv.close()
        display_func_exit_msg(output_file=new_csv_file, func_name='exchange_columns')
        return new_csv_file

    @staticmethod
    def before_login_log_to_csv(log_file, process_tag='CSV'):
        csv_sep = PreProcessOperations.current_csv_sep
        csv_file = log_file.split('.')[0] + '[' + process_tag + '].csv'

        input_log_file = open(log_file, encoding='ISO-8859-1')
        output_csv_file = open(csv_file, 'w')

        csv_header_items = [
            'date', 'time', 's-ip', 'cs-method', 'cs-uri-stem', 'cs-uri-query', 's-port', 'cs-username', 'c-ip',
            'cs(User-Agent)', 'cs(Referer)', 'sc-status', 'sc-substatus', 'sc-win32-status', 'time-taken']

        csv_header = list_to_csv_line(csv_header_items)
        output_csv_file.write(csv_header + '\n')  # Write header to first row of the file.

        count_comment, count_log = 0, 0
        for line in input_log_file:
            if not line.startswith('#'):  # If row is not comment, consider.
                count_log += 1
                line = line[:-1].replace(' ', csv_sep)
                output_csv_file.write(line + '\n')
            else:  # If row is comment, don't consider.
                count_comment += 1
        input_log_file.close()
        output_csv_file.close()

        print('> INFO: %d out of %d log-rows converted to csv format.' % (count_log, count_log + count_comment))
        print('> INFO: %d out of %d comment-rows have been omitted.' % (count_comment, count_log + count_comment))
        display_func_exit_msg(output_file=csv_file, func_name='before_login_log_to_csv')
        return csv_file

    @staticmethod
    def after_login_log_to_csv(log_file, process_tag='CSV'):
        csv_sep = PreProcessOperations.current_csv_sep
        csv_file = log_file.split('.')[0] + '[' + process_tag + '].csv'

        input_log_file = open(log_file)
        output_csv_file = open(csv_file, 'w')

        old_csv_header = input_log_file.__next__()
        new_csv_header = transform_csv_header(old_csv_header)
        output_csv_file.write(new_csv_header + '\n')  # Write header to first row of the file.

        with open(log_file) as f:
            num_of_rows = sum(1 for _ in f)

        input_log_file.__next__()  # Pass line filled with dashes
        for i in range(num_of_rows - 5):  # Reduce first 2 rows and last 3 rows
            line = input_log_file.__next__()
            spaces_reduced_row = reduce_multiple_spaces(line).replace(' ', csv_sep)
            output_csv_file.write(spaces_reduced_row + '\n')
        input_log_file.close()
        output_csv_file.close()
        display_func_exit_msg(output_file=csv_file, func_name='after_login_log_to_csv')
        return csv_file

    @staticmethod
    def clean_bots_from_csv(csv_file, user_agent_idx, process_tag='NoBots'):
        bot_log_count = 0
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')
        unprocessed_csv_file = open(csv_file, 'r')
        processed_csv_file = open(new_csv_file, 'w')

        csv_header = unprocessed_csv_file.__next__()  # pass csv header
        processed_csv_file.write(csv_header)  # Write same header to first row of the file.

        for line in unprocessed_csv_file:
            user_agent = line_to_list(line)[user_agent_idx]

            if not user_agent.lower().__contains__('bot'):  # If line doesn't contain 'bot' in any case.
                processed_csv_file.write(line)
            else:
                bot_log_count += 1
        unprocessed_csv_file.close()
        processed_csv_file.close()

        print('> INFO: %d bot logs have been omitted.' % bot_log_count)
        display_func_exit_msg(output_file=new_csv_file, func_name='clean_bots_from_csv')
        return new_csv_file

    @staticmethod
    def select_features_in_csv(csv_file, selected_features, remove_header=False, process_tag='SF'):
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')

        unprocessed_csv_file = open(csv_file, 'r')
        processed_csv_file = open(new_csv_file, 'w')

        if remove_header:
            unprocessed_csv_file.__next__()  # pass csv

        for line in unprocessed_csv_file:
            item_list = line_to_list(line)

            new_item_list = []
            for col in selected_features:
                new_item_list.append(item_list[col])

            processed_csv_file.write(list_to_csv_line(new_item_list) + '\n')
        unprocessed_csv_file.close()
        processed_csv_file.close()
        display_func_exit_msg(output_file=new_csv_file, func_name='select_features_in_csv')
        return new_csv_file

    @staticmethod
    def extract_usr_ids(csv_file, ip_idx, usr_agent_idx):
        unprocessed_csv_file = open(csv_file, 'r')
        unprocessed_csv_file.__next__()  # pass csv header

        users_set = set()  # Set of tuple_of_ip_and_user-agent
        users_dict = {}  # key = tuple_of_ip_and_user-agent & value = user_id
        users_dict_count = 0
        for line in unprocessed_csv_file:
            tmp_list = line_to_list(line)
            a_tuple = (tmp_list[ip_idx], tmp_list[usr_agent_idx])
            if not users_set.__contains__(a_tuple):
                users_set.add(a_tuple)
                users_dict[a_tuple] = users_dict_count
                users_dict_count += 1
        unprocessed_csv_file.close()
        return users_dict

    @staticmethod
    def write_usr_ids(csv_file, users_dict, ip_idx, usr_agent_idx, process_tag='UserIDs'):
        csv_sep = PreProcessOperations.current_csv_sep
        unprocessed_csv_file = open(csv_file, 'r')
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')
        processed_csv_file = open(new_csv_file, 'w')

        csv_header = unprocessed_csv_file.__next__()
        new_csv_header = 'user_id' + csv_sep + csv_header
        processed_csv_file.write(new_csv_header)  # Write new header to first row of the file.

        for line in unprocessed_csv_file:
            tmp_list = line_to_list(line)
            a_tuple = (tmp_list[ip_idx], tmp_list[usr_agent_idx])

            user_id = users_dict.get(a_tuple)
            new_line = str(user_id) + csv_sep + line
            processed_csv_file.write(new_line)
        unprocessed_csv_file.close()
        processed_csv_file.close()
        display_func_exit_msg(output_file=new_csv_file, func_name='write_usr_ids')
        return new_csv_file

    @staticmethod
    def sort_csv_by_header(csv_file, feature1, feature2, feature3, feature4,
                           process_tag='Sorted'):  # sort up to 4 header
        csv_sep = PreProcessOperations.current_csv_sep
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')
        df = pandas.read_csv(csv_file, sep=csv_sep)

        if feature2 is None:  # Sort by 1 header
            df = df.sort_values([feature1])
            print('> INFO: Sorted values by 1 features: %s' % feature1)
        elif feature3 is None:  # Sort by 2 headers
            df = df.sort_values([feature1, feature2])
            print('> INFO: Sorted values by 2 features: %s, %s' % (feature1, feature2))
        elif feature4 is None:  # Sort by 3 headers
            df = df.sort_values([feature1, feature2, feature3])
            print('> INFO: Sorted values by 3 features: %s, %s, %s' % (feature1, feature2, feature3))
        else:  # Sort by 4 headers
            df = df.sort_values([feature1, feature2, feature3, feature4])
            print('> INFO: Sorted values by 4 features: %s, %s, %s, %s' % (feature1, feature2, feature3, feature4))

        df.to_csv(new_csv_file, index=False, sep=csv_sep)
        display_func_exit_msg(output_file=new_csv_file, func_name='sort_csv_by_header')
        return new_csv_file

    @staticmethod
    def calc_session_ids(csv_file, user_id_idx, date_idx, time_idx, time_format, date_format, threshold_sec=600,
                         process_tag='SessionIDs'):
        csv_sep = PreProcessOperations.current_csv_sep
        t_o = TimeOperations(time_format, date_format)

        unprocessed_csv_file = open(csv_file, 'r')
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')
        processed_csv_file = open(new_csv_file, 'w')

        csv_header = unprocessed_csv_file.__next__()
        new_header = 'session_id' + csv_sep + csv_header
        processed_csv_file.write(new_header)  # Write new header to new file.

        first_ln = unprocessed_csv_file.__next__()
        processed_csv_file.write('0' + csv_sep + first_ln)  # write first row with session_id = 0

        prev_ln = line_to_list(first_ln)
        session_id = 0  # initialize session id
        for line in unprocessed_csv_file:
            cur_ln = line_to_list(line)

            if cur_ln[user_id_idx] != prev_ln[user_id_idx]:  # different user
                session_id += 1
            else:  # same user
                real_diff = t_o.calc_time_diff(cur_ln, prev_ln, date_idx, time_idx)
                if real_diff > threshold_sec:  # same user && large diff
                    session_id += 1
            new_line = str(session_id) + csv_sep + line
            processed_csv_file.write(new_line)

            prev_ln = cur_ln
        unprocessed_csv_file.close()
        processed_csv_file.close()
        display_func_exit_msg(output_file=new_csv_file, func_name='calc_session_ids')
        return new_csv_file

    @staticmethod
    def clean_non_page_links_from_csv(csv_file, uid_idx, date_idx, time_idx, url_idx, process_tag='AllPages'):
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')
        input_csv = open(csv_file, 'r')
        output_csv = open(new_csv_file, 'w')

        csv_header = input_csv.__next__()  # pass csv header
        output_csv.write(csv_header)  # Write same header to first row of the file.
        prev_ln = line_to_list(input_csv.__next__())  # first line

        cnt_non_pages_log = 0
        cnt_all_log = 1

        for line in input_csv:
            cnt_all_log += 1
            cur_ln = line_to_list(line)
            sid_time_tup0 = (prev_ln[uid_idx], prev_ln[date_idx], prev_ln[time_idx])
            sid_time_tup1 = (cur_ln[uid_idx], prev_ln[date_idx], cur_ln[time_idx])

            both_nav_links = is_nav_link(prev_ln[url_idx]) and is_nav_link(cur_ln[url_idx])
            prev_ln_is_redirected_link = (sid_time_tup0 == sid_time_tup1 and both_nav_links)
            if link_contains_image(prev_ln[url_idx]) or not is_nav_link(prev_ln[url_idx]) or prev_ln_is_redirected_link:
                cnt_non_pages_log += 1  # omitted 1 log.
            else:
                output_csv.write(list_to_csv_line(prev_ln) + '\n')

            prev_ln = cur_ln

        if not link_contains_image(prev_ln[url_idx]):
            output_csv.write(list_to_csv_line(prev_ln) + '\n')  # handle last line

        input_csv.close()
        output_csv.close()
        print('> INFO: %d out of %d rows that contains non-pages have been omitted.' % (cnt_non_pages_log, cnt_all_log))
        display_func_exit_msg(output_file=new_csv_file, func_name='clean_non_page_links_from_csv')
        return new_csv_file

    @staticmethod
    def filter_page_views(csv_file, usr_idx, sid_idx, date_idx, time_idx, url_idx, time_format, date_format,
                          session_avg_wait_t=20, process_tag='FilteredPV'):
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')
        input_csv = open(csv_file, 'r')
        output_csv = open(new_csv_file, 'w')
        t_o = TimeOperations(time_format=time_format, date_format=date_format)

        new_csv_header_items = ['user_id', 'session_id', 'link_count', 'unique_link_count', 'session_duration_in_s']

        new_csv_header = list_to_csv_line(new_csv_header_items)
        output_csv.write(new_csv_header + '\n')  # Write new header to first row of the file.

        input_csv.__next__()  # Pass CSV Header.
        prev_ln = session_1st_ln = line_to_list(input_csv.__next__())
        link_cnt = unq_link_cnt = 0
        unique_links_set = set()

        for line in input_csv:
            cur_ln = line_to_list(line)

            link_cnt += 1
            if not unique_links_set.__contains__(prev_ln[url_idx]):
                unique_links_set.add(prev_ln[url_idx])
                unq_link_cnt += 1

            if cur_ln[sid_idx] != prev_ln[sid_idx]:  # different session
                session_duration = session_avg_wait_t + t_o.calc_time_diff(prev_ln, session_1st_ln, date_idx, time_idx)
                csv_list = [prev_ln[usr_idx], prev_ln[sid_idx], link_cnt, unq_link_cnt, session_duration]
                output_csv.write(list_to_csv_line(csv_list) + '\n')

                unq_link_cnt = link_cnt = 0
                unique_links_set = set()
                session_1st_ln = cur_ln

            prev_ln = cur_ln

        # handle last line
        last_ln = prev_ln
        link_cnt += 1
        if not unique_links_set.__contains__(last_ln[url_idx]):
            unq_link_cnt += 1
        duration = session_avg_wait_t + t_o.calc_time_diff(prev_ln, session_1st_ln, date_idx, time_idx)
        csv_list = [last_ln[usr_idx], last_ln[sid_idx], link_cnt, unq_link_cnt, duration]
        output_csv.write(list_to_csv_line(csv_list) + '\n')

        input_csv.close()
        output_csv.close()
        display_func_exit_msg(output_file=new_csv_file, func_name='filter_page_views')
        return new_csv_file

    @staticmethod
    def filter_video_views(csv_file, vid_id_idx, usr_idx, sid_idx, vid_dur_idx, process_tag='FilteredVV'):
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')
        input_csv = open(csv_file, 'r')
        output_csv = open(new_csv_file, 'w')

        new_csv_header_items = ['user_id', 'session_id', 'vid_count', 'unique_vid_count', 'total_vid_view']
        new_csv_header = list_to_csv_line(new_csv_header_items)
        output_csv.write(new_csv_header + '\n')  # Write new header to first row of the file.

        input_csv.__next__()  # Pass CSV Header.
        prev_ln = line_to_list(input_csv.__next__())  # first line
        vid_cnt = unq_vid_cnt = 0
        unique_vids_set = set()
        session_video_dur = 0

        for line in input_csv:
            cur_ln = line_to_list(line)
            vid_cnt += 1
            if not unique_vids_set.__contains__(prev_ln[vid_id_idx]):
                unique_vids_set.add(prev_ln[vid_id_idx])
                unq_vid_cnt += 1

            if cur_ln[sid_idx] != prev_ln[sid_idx]:  # different session
                csv_list = [prev_ln[usr_idx], prev_ln[sid_idx], vid_cnt, unq_vid_cnt, int(prev_ln[vid_dur_idx])]
                output_csv.write(list_to_csv_line(csv_list) + '\n')

                unq_vid_cnt = vid_cnt = 0
                unique_vids_set = set()
                session_video_dur = 0
            prev_ln = cur_ln

        last_ln = prev_ln  # handle last line
        vid_cnt += 1
        session_video_dur += int(last_ln[vid_dur_idx])
        if not unique_vids_set.__contains__(last_ln[vid_id_idx]):
            unq_vid_cnt += 1
        csv_list = [last_ln[usr_idx], last_ln[sid_idx], vid_cnt, unq_vid_cnt, int(last_ln[vid_dur_idx])]
        output_csv.write(list_to_csv_line(csv_list) + '\n')

        input_csv.close()
        output_csv.close()
        display_func_exit_msg(output_file=new_csv_file, func_name='filter_video_views')
        return new_csv_file

    @staticmethod
    def merge_video_page_views(mf_dir, pv_file, vv_file, uid_idx, sid_idx, merged_file='merged_pv_vv.csv'):
        merged_csv_file = mf_dir + merged_file
        input_vv = open(vv_file, 'r')
        input_pv = open(pv_file, 'r')

        if not os.path.exists(mf_dir):
            os.makedirs(mf_dir)

        merged_csv = open(merged_csv_file, 'w')

        pv_header_list = line_to_list(input_pv.__next__())
        vv_header_list = line_to_list(input_vv.__next__())

        del vv_header_list[uid_idx:sid_idx + 1]  # delete user_id and session_id feature video-views.
        empty_vv_row_size = vv_header_list.__len__()

        pv_header_list.extend(vv_header_list)
        merged_csv_header = list_to_csv_line(pv_header_list)
        merged_csv.write(merged_csv_header + '\n')

        vv_line = input_vv.readline()  # first line of video-views
        vv_row_list = line_to_list(vv_line)
        vv_pk = generate_uid_sid_primary_key(vv_row_list, uid_idx, sid_idx, num_of_digits=7)
        for pv_line in input_pv:
            pv_row_list = line_to_list(pv_line)
            pv_pk = generate_uid_sid_primary_key(pv_row_list, uid_idx, sid_idx, num_of_digits=7)
            while vv_line and pv_pk > vv_pk:
                vv_line = input_vv.readline()
                vv_row_list = line_to_list(vv_line)
                vv_pk = generate_uid_sid_primary_key(vv_row_list, uid_idx, sid_idx, num_of_digits=7)

            if vv_line and pv_pk == vv_pk:  # User_ids and Session_ids match.
                del vv_row_list[uid_idx:sid_idx + 1]  # delete user_id and session_id
                pv_row_list.extend(vv_row_list)
            else:  # User_ids and Session_ids doesn't match, fill with NULLs.
                pv_row_list.extend(['NULL'] * empty_vv_row_size)

            merged_csv.write(list_to_csv_line(pv_row_list) + '\n')

        input_vv.close()
        input_pv.close()
        merged_csv.close()
        display_func_exit_msg(output_file=merged_csv_file, func_name='merge_video_page_views')
        return merged_file

    @staticmethod
    def clear_rows_contain_null(csv_file, null_word='NULL', process_tag='NoNulls'):
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')
        input_csv = open(csv_file, 'r')
        output_csv = open(new_csv_file, 'w')

        csv_header = input_csv.__next__()  # pass csv header
        output_csv.write(csv_header)  # Write same header to first row of the file.

        for line in input_csv:
            if not line.__contains__(null_word):
                output_csv.write(line)

        input_csv.close()
        output_csv.close()
        display_func_exit_msg(output_file=new_csv_file, func_name='clear_rows_contain_null')
        return new_csv_file

    @staticmethod
    def change_csv_separator(csv_file, new_csv_sep=__final_csv_sep__, process_tag='CsvSepChanged'):
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')
        cur_csv_sep = PreProcessOperations.current_csv_sep
        PreProcessOperations.current_csv_sep = new_csv_sep
        input_csv = open(csv_file, 'r')
        output_csv = open(new_csv_file, 'w')

        for line in input_csv:
            line = line.replace(cur_csv_sep, new_csv_sep)
            output_csv.write(line)
        input_csv.close()
        output_csv.close()
        display_func_exit_msg(output_file=new_csv_file, func_name='change_csv_separator')
        return new_csv_file

    @staticmethod
    def remove_outliers(csv_file, low_bound=0.05, high_bound=0.95, process_tag='NoOutl'):
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')
        df = pandas.read_csv(csv_file, sep=PreProcessOperations.current_csv_sep)

        quantized_df = df.quantile([low_bound, high_bound])

        filtered_df = df.apply(lambda x: x[(x > quantized_df.loc[low_bound, x.name]) &
                                           (x < quantized_df.loc[high_bound, x.name])], axis=0)

        filtered_df.dropna(inplace=True)
        filtered_df.to_csv(new_csv_file, index=False)
        display_func_exit_msg(output_file=new_csv_file, func_name='remove_outliers')
        return new_csv_file

    @staticmethod
    def normalize_data(csv_file, process_tag='Normalized'):
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')
        df = pandas.read_csv(csv_file)
        df_norm = (df - df.mean()) / (df.max() - df.min())
        df_norm.to_csv(new_csv_file, index=False)
        display_func_exit_msg(output_file=new_csv_file, func_name='normalize_data')
        return new_csv_file

    @staticmethod
    def label_data(csv_file, feature1: str, feature2: str, feature3: str, use_k_means=False, range_weight=0.65,
                   process_tag='Labeled'):
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')

        if use_k_means:  # Use KMeans
            k_means = KMeans(iteration_num=300, num_of_class=2)
            k_means.load_dataset(csv_file, delimiter=PreProcessOperations.current_csv_sep, has_header=True)
            k_means.create_two_initial_centroids()
            k_means.iterate_k_means()
            k_means.print_results()
            k_means.write_dataset(new_csv_file, delimiter=PreProcessOperations.current_csv_sep)
        else:  # Use Threshold Method
            df = pandas.read_csv(csv_file)
            mean1 = df[feature1].mean() - df[feature1].std() * range_weight
            mean2 = df[feature2].mean() - df[feature2].std() * range_weight
            mean3 = df[feature3].mean() - df[feature3].std() * range_weight

            input_csv = open(csv_file, 'r')
            output_csv = open(new_csv_file, 'w')

            header_l = line_to_list(input_csv.__next__())
            header_l.append('class_success')
            output_csv.write(list_to_csv_line(header_l) + '\n')

            f1_idx, f2_idx, f3_idx = header_l.index(feature1), header_l.index(feature2), header_l.index(feature3)

            success_cnt, fail_cnt = 0, 0
            for raw_line in input_csv:
                line = line_to_list(raw_line)
                if float(line[f1_idx]) > mean1 and float(line[f2_idx]) > mean2 and float(line[f3_idx]) > mean3:
                    line_label = 1
                    success_cnt += 1
                else:
                    line_label = 0
                    fail_cnt += 1
                line.append(line_label)
                output_csv.write(list_to_csv_line(line) + '\n')

            print('INFO: Class=1: {}, Class=0: {}'.format(success_cnt, fail_cnt))
            print('INFO: Success Rate: %f%%' % (100 * success_cnt / (fail_cnt + success_cnt)))
            input_csv.close()
            output_csv.close()

        display_func_exit_msg(output_file=new_csv_file, func_name='label_data')
        return new_csv_file

    @staticmethod
    def finalize_merged_file(csv_file, process_tag='RemovedHeader'):
        new_csv_file = csv_file.replace('.csv', '[' + process_tag + '].csv')
        df = pandas.read_csv(csv_file, sep=PreProcessOperations.current_csv_sep)
        df.to_csv(new_csv_file, index=False, sep=PreProcessOperations.current_csv_sep, header=False)
