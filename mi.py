def split_rule(rule):
    rules_processed = []
    for index, rule in enumerate(rule):
        temp = rule.split('=')
        rules_processed.append((temp[0].split(","), temp[1], index))
    return rules_processed


def filter_avant(rules_processed, facts):
    rule_applicable = []
    for premise in split_rule(rules_processed):
        if set(premise[0]).issubset(facts):
            rule_applicable.append(premise)
    return rule_applicable


def filter_arriere(rules_raw_text, but):
    rule_applicable = []
    for premise in split_rule(rules_raw_text):
        if premise[1] == but:
            rule_applicable.append(premise)
    return rule_applicable


def select_first_rule(rules_filtered):
    if not rules_filtered:
        return None
    else:
        return rules_filtered[0]


def select_rule_most(rules_filtered):
    if not rules_filtered:
        return None
    else:
        chosen = rules_filtered[0]
        temp = rules_filtered[0][0]
        for premises in rules_filtered:
            if len(premises[0]) > len(temp[0]):
                chosen = premises
    return chosen


def execution_avant(rules_selected, facts, rules):
    facts.append(rules_selected[1])
    rule_applied = rules_selected
    rules.pop(rules_selected[2])
    return rule_applied[0:-1]


def execution_arriere(rules_selected, facts, rules, goals):
    goals.pop(0)
    for i in rules_selected[0]:
        goals.insert(0, i)
    goals = list(set(goals))
    for goal in goals:
        if goal in facts:
            goals.remove(goal)
    rules.pop(rules_selected[2])
    return goals
