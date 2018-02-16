# This will be a function-based helper for storing information in transactions on the steem blockchain
# This will not try to interperet the data
from websocket import create_connection
from steem import Steem
import time
import json

def retrieve(keyword=[], account="anarchyhasnogods",sent_to="randowhale", position=-1, keyword_and_account = True, recent = 1, step = 10000, minblock = -1, node="wss://steemd.privex.io", not_all_accounts = True):
    # minblock is blocks before current block
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
        print(3, position)
        while found:
            print(found)
            # Checks if the

            if (recent > 0 and len(memo_list) > 0) and not_all_accounts:
                if len(memo_list) >= recent:

                    break

            history = s.get_account_history(sent_to, position, step)
            memos = get_memo(history)
            has_min_block = False
            for i in range(len(memos)-1, -1, -1):
                if len(memo_list) >= recent and not_all_accounts:
                    break
                has_keyword = False

                if memos[i][3] < minblock:
                    has_min_block = True
                if keyword != []:
                    try:
                        new_memo = json.loads(str(memos[i][2]))
                        print(new_memo)
                        if new_memo[keyword[0]] == keyword[1]:
                            has_keyword = True
                    except:
                        pass


                has_account = memos[i][1] == account
                #print(memos[i][1], account)
                if keyword_and_account:
                    if has_keyword and has_account:

                        memo_list.append(memos[i])
                else:
                    if has_account or has_keyword:
                        #print("added")
                        memo_list.append(memos[i])






            if position == step+1 or has_min_block:

                break

            elif position-step <= step:
                position = step+1

            else:
                position -=step


        return memo_list
    # This checks if it has the keyword or is by the account


def save_memo(information, to, account_from, active_key, transaction_size=0.001, asset="SBD", node="wss://steemd-int.steemit.com"):
    index = None
    node_connection = create_connection(node)
    s = Steem(node=node_connection, keys=active_key)
    print(to,account_from)
    s.transfer(to,transaction_size,asset=asset,account=account_from, memo=json.dumps(information))
    print("here")
    if information["type"] == "account":
        index = retrieve(account=account_from, sent_to=to, recent=1, step=50, keyword=["account",information["account"]])
    elif information["type"] == "post":
        index = retrieve(account=account_from, sent_to=to, recent=1, step=50, keyword=["post_link",information["post_link"]])
    if index == [] or index == None:
        return False
    return index[0][0]



def get_memo(history_list):
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








