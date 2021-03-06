# This will be a function-based helper for storing information in transactions on the steem blockchain
# This will not try to interperet the data
from websocket import create_connection
from steem import Steem
import time
import json

def retrieve(keyword=[], account="anarchyhasnogods",sent_to="randowhale", position=-1, recent = 1, step = 10000, minblock = -1, node="wss://steemd.privex.io", not_all_accounts = True):
    # minblock is blocks before current block
    # account is the account that sent the memo
    # sent-to is account that it was sent to
    # keyword is what it looks for in the json ["type","account"] would bring back memos with the type account
    # -1 position means the latest, anything else means a specific memo where the position is known
    # step means how many actions it grabs at once
    # notallaccounts is wether or not it looks at every account


    node_connection = create_connection(node)
    s = Steem(node=node_connection)
    memo_list = []
    if position > -1:
        # This returns the memo based on a saved position
        return get_memo(s.get_account_history(sent_to, position, 1))


    else:
        # If the first is 0, it checks the first one with the keyword or account
        #(or and depending on keyword and account)
        found = True
        memo_list = []
        # This gets the total amount of items in the accounts history
        # This it to prevent errors related to going before the creation of the account
        memo_thing = s.get_account_history(sent_to,-1,0)
        size = memo_thing[0][0]
        if minblock > 0:
            minblock = memo_thing[0][1]["block"] - minblock
        position = size
        if position < 0:
            position = step +1
        if step > position:
            step = position - 1
        while found:
            # Checks if the

            if (recent > 0 and len(memo_list) > 0) and not_all_accounts:
                if len(memo_list) >= recent:

                    break

            history = s.get_account_history(sent_to, position, step)
            memos = get_memo(history)
            has_min_block = False
            #print(len(memos),keyword)
            for i in range(len(memos)-1, -1, -1):
                # goes through memos one at a time, starting with latest

                if len(memo_list) >= recent and not_all_accounts:
                    # ends if there are enough memos
             #       print("here")
                    break
                has_keyword = False

                if memos[i][3] < minblock:
                    has_min_block = True
                has_account = False
                if memos[i][1] == account:
                    has_account = True
                if keyword != []:
                    # checks if keyword is in the memo

                    #print("HERE")
                    try:
                        new_memo = json.loads(str(memos[i][2]))
                     #   print(new_memo)
                        for ii in keyword:
                      #      print(i)

                            has_keyword = False
                            # print(new_memo)
                            #print(new_memo[i[0]], "This")
                            print(keyword,ii,new_memo)
                            if new_memo[ii[0]] == ii[1]:
                                print("MEMO KEYYYYYYYYYYYYYYYYYYYYYYYYY")
                                has_keyword = True
                            if not has_keyword:
                       #         print("this_pos")
                                break
                        #print("her")
                    except Exception as e:
                        #print(e)
                        pass

                if has_keyword and has_account:
              #      print("THIS", i)
                    memo_list.append(memos[i])
               #     print(memo_list)

            #print("here")

            if position == step+1 or has_min_block or (recent <= len(memo_list) and not_all_accounts):
                # ends if it has gone through all the memos, reached the min block, or has too many memos
             #   print("break")
                break

            elif position-step <= step:
                position = step+1

            else:

                position -=step

        #print(memo_list)
        print("HEREEE")
        print(memo_list)
        return memo_list
    # This checks if it has the keyword or is by the account


def save_memo(information, to, account_from, active_key, transaction_size=0.001, asset="SBD", node="wss://steemd-int.steemit.com",try_thing = [0,0]):
    # print statements are because im testing rn
    # This should send a memo and return the position

    print("AAAAAAAAaa",information)
    index = None
    try:
        node_connection = create_connection(node)
        s = Steem(node=node_connection, keys=active_key)
        s.transfer(to,transaction_size,asset=asset,account=account_from, memo=json.dumps(information))
        try_thing[0] = 0
    except Exception as e:
        print(e)
        if try_thing[0] > 5:
            try_thing[0] = 0
            return False
        return save_memo(information,to,account_from,active_key,transaction_size,asset,node, try_thing[0] +1)
    time.sleep(3)
    while index == None or index == []:
        print("THIS")
        try:
            print("THISSS")
            print(information)
            print(information["type"])
            if information["type"] == "account":
                index = retrieve(account=account_from, sent_to=to, recent=1, step=50, keyword=[["account",str(information["account"])], ["type","account"]])
            elif information["type"] == "post":
                index = retrieve(account=account_from, sent_to=to, recent=1, step=50, keyword=[["post_link",information["post_link"]]])
            elif information["type"] == "vote-link":

                print("Thisone")
                print(account_from,to,information["account"])

                index = retrieve(account=account_from, sent_to=to, recent=1, step=50, keyword=[["type","vote-link"],["account",information["account"]]])

                print("index try")


        except Exception as e:
            print("EXCEPTTT")
            print(e)
        try_thing[1] += 1
        if try_thing[1] > 5:
            try_thing[1] = 0
            print("FALSE1")
            return False




    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(index)
    return index[0][0]



def get_memo(history_list):
    # this goes through every account action and sees if it is a transfer
    # it then adds it to the list for the functions above to check
    memos = []
    for i in history_list:
        memo = []
        for ii in i:

            if type(ii) == dict:
                try:

                    if ii['op'][0] == 'transfer':
                        memo.append(ii['op'][1]['from'])
                        memo.append(ii['op'][1]['memo'])
                        memo.append(ii['block'])
                        memos.append(memo)

                    else:
                        memo = []
                except:
                    pass
            if type(ii) == int:

                memo.append(ii)

    return memos








