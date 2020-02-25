from cmp.pycompiler import Terminal, Sentence, Grammar, Symbol


class TrieNode:

    def __init__(self, value, terminating=False):
        self.value = value
        self.children = {}
        self.terminating = terminating


class Trie:

    def __init__(self):
        self.root = TrieNode(' ')

    def insert(self, sentence: Sentence):
        root = self.root
        for symbol in sentence:
            if symbol not in root.children:
                root.children[symbol] = TrieNode(symbol)
            root = root.children[symbol]
        root.terminating = True

    def search_prefix(self):
        root = self.root
        if len(root.children) == 1:
            prefix = Sentence()
            root = list(root.children.values())[0]
            while True:
                prefix += root.value
                if len(root.children) > 1 or len(root.children) == 0:
                    break
                root = list(root.children.values())[0]
            if root.terminating:
                return
            return prefix
        else:
            return


if __name__ == '__main__':
    trie = Trie()
    G = Grammar()
    E = G.NonTerminal('E', True)
    T, F, X, Y = G.NonTerminals('T F X Y')
    plus, minus, star, div, opar, cpar, num = G.Terminals('+ - * / ( ) num')

    E %= T + X
    X %= plus + T + X | minus + T + X | G.Epsilon
    T %= F + Y
    Y %= star + F + Y | div + F + Y | G.Epsilon
    F %= num | opar + E + cpar
    trie.insert(Sentence(E, T))
    trie.insert(Sentence(E, T, F))
    trie.insert(Sentence(E, T, X))
    print(trie.search_prefix())
