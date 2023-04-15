from time import time


class TrieTree:

    class TrieNode:
        def __init__(self, letter, is_end=False, parent=None) -> None:
            self.letter = letter
            self.child_dic = {}
            self.is_end = is_end
            self.parent = parent

        def print_tree(self) -> None:
            print("--------")
            #print(f"{self.letter}|is_end: {self.is_end}|parent: {self.parent.letter if self.parent is not None else 'None'}")
            #for key, value in self.child_dic.items():
                #print(f"--{key}-> ({value.letter})")
            for key, value in self.child_dic.items():
                value.print_tree()

    def __init__(self) -> None:
        self.root = self.TrieNode("root")

    def construct_tree(self, filename) -> None:
        start_time = time()
        try:
            with open(filename, "r", encoding="utf-8") as f:
                word_lst = f.readlines()
                for i in range(len(word_lst)):
                    word_lst[i] = word_lst[i][:-1]
        except FileNotFoundError:
            print("Error: can't find 'sensitive_words_lines.txt'.")
            return -1
        for i in word_lst:
            node_ptr = self.root
            for index, j in enumerate(i):
                # skip the existing end
                if node_ptr.is_end:
                    continue
                # insert new letter to the tree and keep going
                if j not in node_ptr.child_dic:
                    node_ptr.child_dic[j] = self.TrieNode(j, False, node_ptr)
                node_ptr = node_ptr.child_dic[j]
                # insert end flag
                if index == len(i) - 1:
                    node_ptr.is_end = True
        end_time = time()
        #print(f"Trie construction time(s): {end_time - start_time}")

    def censor(self, text, ignore_chars="") -> dict:
        # parse ignore chars file
        try:
            with open(ignore_chars, "r", encoding="utf-8") as f:
                ignore_chars = f.readlines()
                for i in range(len(ignore_chars)):
                    ignore_chars[i] = ignore_chars[i][:-1]
        except FileNotFoundError:
            return {"Error": "can't find 'ignored_chars.txt'."}

        start_time = time()
        text = text.lower()
        result = {"passed": True, "banned_word_num": 0, "banned_words": [], "execution time(s)": 0}

        head_ptr = 0
        for index, i in enumerate(text):
            # skip the current letter if it is ignored
            if i in ignore_chars:
                continue
            # teleport to the head pointer
            if index < head_ptr:
                continue
            head_ptr = index
            letter_ptr = index
            node_ptr = self.root
            curr_word = ""
            while True:
                if node_ptr.is_end:
                    result["passed"] = False
                    result["banned_word_num"] += 1
                    result["banned_words"].append([curr_word, index+1])
                    head_ptr = letter_ptr
                    break
                if letter_ptr >= len(text):
                    break
                # skip the current letter if it is ignored
                if text[letter_ptr] in ignore_chars:
                    letter_ptr += 1
                    continue
                if text[letter_ptr] in node_ptr.child_dic:
                    curr_word += text[letter_ptr]
                    node_ptr = node_ptr.child_dic[text[letter_ptr]]
                    letter_ptr += 1
                else:
                    break
        end_time = time()
        result["execution time(s)"] = end_time - start_time
        return result


def run(text):
    try:
        with open(text, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print("Error: can't find 'text.txt'.")
        while True:
            k = input("")

    tree = TrieTree()
    flag = tree.construct_tree("sensitive_words_lines.txt")
    if flag == -1:
        k = input("----- program end -----")
        while True:
            k = input("")

    result = tree.censor(text, "ignored_chars.txt")
    newlist = result["banned_words"]
    newlist2 = []
    for item in newlist:#提取列表列表
        newlist2.append(item[0])
    #print(newlist2)
    newlist2 = list(set(newlist2))
    strResult = 'Contains prohibited words:'

    strResult= strResult+ ' '.join(newlist2)

    print(strResult+"\n")
    return  strResult

if  __name__ == '__main__':
    run("text.txt")
