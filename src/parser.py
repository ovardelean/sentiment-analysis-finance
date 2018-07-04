import os, sys, json, re, time
import config as config
import nltk

class Parser(object):
    def __init__(self):
        self.leading = self.load_dictionary(config.DICT_LEADING)
        self.lagging = self.load_dictionary(config.DICT_LAGGING)
        self.lagging_rev = self.load_dictionary(config.DICT_LAGGING_REV)
        self.directionality = self.load_dictionary(config.DICT_DIRECTIONALITY)
        self.positive = self.load_dictionary(config.DICT_POSITIVE)
        self.negative = self.load_dictionary(config.DICT_NEGATIVE)

    def load_dictionary(self, file_path):
        with open(file_path, 'rb') as f:
            return json.load(f)

    def check_indicators_3(self, i, tokens, marked, result):
        if marked[i] or marked[i+1] or marked[i+2]:
            return marked, result
        group = " ".join([tokens[i], tokens[i+1], tokens[i+2]])
        #group = " ".join(tokens[i:i+1])
        if group in self.leading.keys():
            marked[i], marked[i+1], marked[i+2] = True, True, True
            result[i], result[i+1], result[i+2] = self.leading[group], "*", "*"
        elif group in self.lagging.keys():
            marked[i], marked[i+1], marked[i+2] = True, True, True
            result[i], result[i+1], result[i+2] = self.lagging[group], "*", "*"
        return marked, result

    def check_indicators_2(self, i, tokens, marked, result):
        if marked[i] or marked[i+1]:
            return marked, result
        group = " ".join([tokens[i], tokens[i+1]])
        #group = " ".join(tokens[i:i+1])
        if group in self.leading.keys():
            marked[i], marked[i+1] = True, True
            result[i], result[i+1] = self.leading[group], "*"
        elif group in self.lagging.keys():
            marked[i], marked[i+1] = True, True
            result[i], result[i+1] = self.lagging[group], "*"
        elif group in self.lagging_rev.keys():
            marked[i], marked[i+1] = True, True
            result[i], result[i+1] = self.lagging_rev[group], "*"
        return marked, result

    def group_stars(self, result, tokens):
        new_result = []
        new_tokens = []
        for i in range(0, len(result)):
            if result[i] == "*":
                new_tokens[-1] += " " + tokens[i]
            else:
                new_result.append(result[i])
                new_tokens.append(tokens[i])
        return new_result, new_tokens

    # def group_indicators(self, result, tokens):
    #     new_result = []
    #     new_tokens = []
    #     had = False
    #     for i in range(0, len(result)):
    #         if not result[i]:
    #             continue
    #         if i < len(result) - 1:
    #             if result[i] in ['lagging', 'leading'] and result[i+1] in ['up', 'down']:
    #                 new_result.append(result[i]+":"+result[i+1])
    #                 new_tokens.append(tokens[i] + " " + tokens[i+1])
    #                 had = True
    #                 continue
    #             if result[i+1] in ['lagging', 'leading'] and result[i] in ['up', 'down']:
    #                 new_result.append(result[i+1]+":"+result[i])
    #                 new_tokens.append(tokens[i+1] + " " + tokens[i])
    #                 had = True
    #                 continue
    #         if not had:
    #             new_result.append(result[i])
    #             new_tokens.append(tokens[i])
    #         had = False
    #     return new_result, new_tokens

    def group_indicators(self, result, tokens):
        new_result = []
        new_tokens = []
        had = False
        target = ['lagging', 'lagging-rev', 'leading']
        groupwith = ['up', 'down']
        for i in range(0, len(result)):
            if not result[i]:
                continue
            if result[i] in target:
                if i < len(result)-1 and result[i+1] in groupwith:
                    new_result.append(result[i]+":"+result[i+1])
                    new_tokens.append(tokens[i]+" "+tokens[i+1])
                    had = True
                elif i > 0 and result[i-1] in groupwith:
                    new_result.append(result[i]+":"+result[i-1])
                    new_tokens.append(tokens[i]+" "+tokens[i-1])
                    had = True
                elif i < len(result)-2 and not result[i+1] and result[i+2] in groupwith:
                    new_result.append(result[i]+":"+result[i+2])
                    new_tokens.append(tokens[i]+" "+tokens[i+2])
                    had = True
                elif i > 1 and not result[i-1] and result[i-2] in groupwith:
                    new_result.append(result[i]+":"+result[i-2])
                    new_tokens.append(tokens[i]+" "+tokens[i-2])
                    had = True
                # elif i < len(result)-3 and not result[i+1] and not result[i+2] and result[i+3] in groupwith:
                #     new_result.append(result[i]+":"+result[i+3])
                #     new_tokens.append(tokens[i]+" "+tokens[i+3])
                #     had = True
                # elif i > 2 and not result[i-1] and not result[i-2] and result[i-3] in groupwith:
                #     new_result.append(result[i]+":"+result[i-3])
                #     new_tokens.append(tokens[i]+" "+tokens[i-3])
                #     had = True
                # elif i < len(result)-4 and not result[i+1] and not result[i+2] and not result[i+3] and result[i+4] in groupwith:
                #     new_result.append(result[i]+":"+result[i+4])
                #     new_tokens.append(tokens[i]+" "+tokens[i+4])
                #     had = True
                # elif i > 3 and not result[i-1] and not result[i-2] and not result[i-3] and result[i-4] in groupwith:
                #     new_result.append(result[i]+":"+result[i-4])
                #     new_tokens.append(tokens[i]+" "+tokens[i-4])
                #     had = True

                if not had:
                    new_result.append(result[i])
                    new_tokens.append(tokens[i])
                continue

            elif result[i] in groupwith:
                if i < len(result)-1 and result[i+1] in target:
                    continue
                elif i < len(result)-2 and not result[i+1] and result[i+2] in target:
                    continue
                # elif i < len(result)-3 and not result[i+1] and not result[i+2] and result[i+3] in target:
                #     continue
                # elif i < len(result)-4 and not result[i+1] and not result[i+2] and not result[i+3] and result[i+4] in target:
                #     continue

            if not had:
                new_result.append(result[i])
                new_tokens.append(tokens[i])
            had = False

        return new_result, new_tokens

    def parse(self, doc, require_tokens=False):
        tokens = nltk.word_tokenize(doc)
        tokens = [i.lower().strip() for i in tokens]
        tokens_length = len(tokens)

        marked = [False for i in range(0,tokens_length)]
        result = [None for i in range(0,tokens_length)]

        tokens_length = len(tokens)

        for i in range(0, tokens_length):
            if i < tokens_length - 2:
                marked, result = self. check_indicators_3(i, tokens, marked, result)
            if i < tokens_length - 1:
                marked, result = self. check_indicators_2(i, tokens, marked, result)

            word = tokens[i]

            # if require_tokens and marked[i]:
            #     group = " ".join([tokens[i], tokens[i+1]])
            #     print word, marked[i], result[i], "Group: ", group

            if marked[i]:
                continue

            if word in self.lagging:
                marked[i] = True
                result[i] = self.lagging[word]
            elif word in self.leading:
                marked[i] = True
                result[i] = self.leading[word]
            elif word in self.lagging_rev:
                marked[i] = True
                result[i] = self.lagging_rev[word]
            elif word in self.directionality:
                marked[i] = True
                result[i] = self.directionality[word]
            elif word in self.positive:
                marked[i] = True
                result[i] = self.positive[word]
            elif word in self.negative:
                marked[i] = True
                result[i] = self.negative[word]
            else:
                result[i] = None

        result, tokens = self.group_stars(result, tokens)
        grouped_results, grouped_tokens = self.group_indicators(result, tokens)

        # print grouped_results
        # print grouped_tokens
        # time.sleep(10)

        if require_tokens:
            return grouped_results, grouped_tokens
        return grouped_results

if __name__ == '__main__':
    parser = Parser()
    print parser.parse("Sales have risen in other export markets")