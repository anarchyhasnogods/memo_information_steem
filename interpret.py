# This file interprets the information gotten and stored to/from the memos for collective intellegence
# If you are not using our memo system exactly feel free to take a look at these functions but they won't be too useful

from memo_saving import main


def start_account(account_name,active_key,keyword_list=[], our_memo_account="space-pictures", our_sending_account="anarchyhasnogods", node="wss://steemd-int.steemit.com"):

    print("here")
    if keyword_list == []:
        keyword_list.append(["gp","0"])
        keyword_list.append(["ad-token-perm","0"])
        keyword_list.append(["token-upvote-perm","0"])
        keyword_list.append(["token-upvote-temp","0"])
        keyword_list.append(["ad-token-temp","0"])
        keyword_list.append(["token-post-review","0"])
        keyword_list.append(["experience","0"])
        keyword_list.append(["steem-owed","0"])
        keyword_list.append(["vote","0"])
    keyword_list.append(["account", account_name])
    real_list = []
    for i in keyword_list:
        real_list.append(i[0])
        real_list.append(i[1])
    info = list_to_full_string(real_list)

    main.save_memo(info, our_memo_account, our_sending_account, active_key)




def get_account_info(account,our_account = "anarchyhasnogods", our_memo_account = "space-pictures"):

    return_info = main.retrieve(["account",account], account=our_account, sent_to=our_memo_account)



    return return_info[0]





def update_account(account, our_sending_account, our_memo_account, changes, active_key):
    # Changes is composed of a list of changes
    #Each seperate change is [keyword,new_information]
    info = get_account_info(account,our_sending_account, our_memo_account)[2]




    for i in range(0, len(info), 2): # First one is key, second one is var
        for ii in range(len(changes)):
            if changes[ii][0] == info[i]:# Checks if key is correct
                if changes[ii][1] == "DELETE":
                    info[i+1].pop()
                    info[i].pop()
                else:
                    info[i + 1] = changes[ii][1] # if key is correct changes variable
                changes.pop(ii) # removes it from changes and exists loop
                break

    if len(changes) != 0:
        for i in changes:
            info.append(i[0])
            info.append(i[1])

    info = list_to_full_string(info)
    main.save_memo(info, our_memo_account, our_sending_account, active_key)






def list_to_full_string(list_set):
    total_len = 0
    for i in list_set:
        total_len += len(i)

    if total_len > 2000:
        for i in range(0,len(list_set-1), 2):
            if list_set[i] == "vote":
                new_set = list_set[i]
                new_set = new_set.split(";")
                link_pos = static_vote_memo(new_set)
            list_set[i+1] = " "

        for i in range(0,len(list_set)-1,2):
            if list_set[i] == "vote_link":
                list_set[i+1] += ";" + link_pos

    string_main = ""
    print(list_set)
    for i in range(0,len(list_set), 2):
        string_main += list_set[i] + ":" + list_set[i+1] + ":"


    return string_main[0:len(string_main)-2]



   


def static_vote_memo(vote_list):
    pass



