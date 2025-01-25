# Importing packages and creating global variables.
import itertools
from collections import defaultdict
import pandas as pd
GROCERIES = pd.read_csv("Groceries_dataset.csv")
GROCERY_LISTS = defaultdict(int)
MEMBER_NUMBERS = []
ITEM_COMBOS = []
COMBO_COUNTS = defaultdict(int)
ITEM_COUNTS = defaultdict(int)
ASSOCIATION_RULES = {}

def create_member_list():
    """Creates a list of member numbers in order to see what they buy at the store to determine relationships."""
    for member_num in GROCERIES['Member_number']:
        if member_num not in MEMBER_NUMBERS:
            MEMBER_NUMBERS.append(member_num)

def create_grocery_list():
    """Uses member numbers to sort the items they bought into lists."""
    for i in MEMBER_NUMBERS:
        GROCERY_LISTS.update({i: GROCERIES[GROCERIES['Member_number'] == i]['itemDescription'].values})


def create_combos():
    """Creates item combos and counts the number of items in each list."""
    for list in GROCERY_LISTS:
        for item in GROCERY_LISTS[list]:
            if item in GROCERY_LISTS[list]:
                ITEM_COUNTS[item] += 1
        ITEM_COMBOS.append(set(itertools.combinations(GROCERY_LISTS[list], 2)))

def count_combos():
    """ Creates every possible item combination and counts how often the items are paired together."""
    for items in ITEM_COMBOS:
        for item in items:
            COMBO_COUNTS[(item[0], item[1])] += 1
            COMBO_COUNTS[(item[1], item[0])] += 1

def create_association_rules():
    """Creates the support, confidence, and lift values for each group of items to determine which ones are most likely to be purchased
    together."""
    for a,b in COMBO_COUNTS:
        support = round(COMBO_COUNTS[a,b] / len(GROCERY_LISTS), 3)
        confidence = round(support / (ITEM_COUNTS[a] / len(GROCERY_LISTS)), 3)
        lift = round(confidence / (ITEM_COUNTS[b] / len(GROCERY_LISTS)), 3)
        if support >= 0.01 and confidence >= 0.5 and lift >= 1:
            ASSOCIATION_RULES[a,b]= {'support':support, 'confidence':confidence, 'lift':lift}

def association_rule_csv():
    association_rules_df = pd.DataFrame(ASSOCIATION_RULES).transpose()
    print(association_rules_df)
    association_rules_df.to_csv('ASSOCIATION_RULES.csv')


# Runs each function in order to create association rules for the grocery items.
create_member_list()
create_grocery_list()
create_combos()
count_combos()
create_association_rules()
association_rule_csv()



