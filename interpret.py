# This file interprets the information gotten and stored to/from the memos for collective intellegence
# If you are not using our memo system exactly feel free to take a look at these functions but they won't be too useful

from memo_saving import main
import json


def start_account(account_name,active_key, our_memo_account="space-pictures", our_sending_account="anarchyhasnogods", node="wss://steemd-int.steemit.com"):
    keyword_dict = {}


    if True:
        keyword_dict["type"] = "account"

        keyword_dict["gp"] = "0"
        keyword_dict["ad-token-perm"] = "0"
        keyword_dict["token-upvote-perm"] =  "0"

        #fix before use
        keyword_dict["token-upvote-temp"] =  "0"
        keyword_dict["ad-token-temp"]= "0"
        keyword_dict["token-post-review"]= "0"
        keyword_dict["experience"]= "0"
        keyword_dict["steem-owed"]= "0"
        keyword_dict["vote"]= "PLACEHOLDER"
        keyword_dict["vote-link"]= "PLACEHOLDER"

    keyword_dict["account"] = account_name

    #info = list_to_full_string(real_list)
    print("ddd", our_sending_account, our_memo_account)

    main.save_memo(keyword_dict, our_memo_account, our_sending_account, active_key)




def get_account_info(account,our_account = "anarchyhasnogods", our_memo_account = "space-pictures"):

    return_info = main.retrieve(["account",account], account=our_account, sent_to=our_memo_account)

    if return_info != []:


        return return_info[0]
    return None




def update_account(account, our_sending_account, our_memo_account, changes, active_key):
    # Changes is composed of a list of changes
    #Each seperate change is [keyword,new_information]
    info = get_account_info(account,our_sending_account, our_memo_account)[2]

    info_dict = json.dumps(info[2])
    for i in changes:
        if i[0] == "vote":
            info_dict[i[0]].append(i[1])
        elif i[1] == "DELETE":
            del info_dict[i[0]]

        else:
            info_dict[i[0]] = i[1]

    # USE JSON FIX



    info = list_to_full_string(info)
    return main.save_memo(info, our_memo_account, our_sending_account, active_key)






def list_to_full_string(list_set,our_memo_account, our_sending_account, active_key):
    dump_list = json.dumps(list_set)
    total_len = len(dump_list)
    if total_len > 2000:
        vote_list_post = main.save_memo(json.dumps(list_set["vote"]), our_memo_account, our_sending_account, active_key)
        list_set["vote"] = []
        list_set["vote-link"].append([vote_list_post, our_memo_account])

    return json.dumps(list_set)




def vote_post(post_link, submission_author, submission_time, ratio, our_memo_account, our_sending_account, active_key):
    # FIX
    json_thing = {}
    json_thing["post_link"] = post_link
    json_thing["submission_author"] = submission_author
    json_thing["time"] = str(submission_time)
    json_thing["ratio"] = str(ratio)

    return main.save_memo(json.dumps(json_thing),our_memo_account, our_sending_account, active_key)


def get_account_list(sending_account,memo_account_list, days = 7):
    block = days * 24 * 60 * 20
    # checks up to 7 days ago
    memo_list = []
    temp_list = []
    accounts_in_list = {"accounts": []}

    for i in memo_account_list:
        temp_list.append(main.retrieve(["type", "account"], sending_account, i, not_all_accounts = False, minblock=block))
        for ii in temp_list[0]:
            ii[2] = json.loads(ii[2])
            if (ii[2]["account"] not in accounts_in_list["accounts"]):

                accounts_in_list["accounts"].append(ii[2]["account"])
                accounts_in_list[ii[2]["account"]] = ii

            elif accounts_in_list[ii[2]["account"]][0] > ii[0]:
                accounts_in_list[ii[2]["account"]] = ii

    # Account_in_list is a dictionary, "accounts" is a list of accounts. Each account has its full account memo info in the dict under its account name
    # to go through info in accounts iterate through the account list as dictionary keys
    return accounts_in_list

def get_vote_list(memo_account, sending_account, id, node):
    return_info = main.retrieve(keyword=["type","post-memo"],account=sending_account, sent_to = memo_account )

    pass





