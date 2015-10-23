from termcolor import colored

def matrix(row, col, value):
    l = list()
    for j in xrange(row):
        l.append([value] * col)
    return l

class Path:
    def __init__(self, letter, location, path=None):
        if path is not None:
            self.word_part = "%s%s" % (path.word_part, letter)
            self.path = list(path.path)
        else:
            self.word_part = letter
            self.path = list()
        self.path.append(location)

    def __repr__(self):
        return "{word:%s, path:%s}" % (self.word_part, self.path)

class Board:
    def __init__(self, board, dictionary):
        index = 4
        self.mat = list()
        self.dictionary = dictionary
        self._create_subwords()
        for i in xrange(4):
            start = index * (i+1)
            self.mat.append(list(board[start-4:start]))

    def solve(self):
        sols = list()
        for i in xrange(0, len(self.mat)):
            for j in xrange(0, len(self.mat)):
                used = matrix(len(self.mat), len(self.mat[0]), False)
                used[i][j] = True
                path = Path(self.mat[i][j], (i, j))
                sols.extend(self._solve(i, j, path, used))
        return sols

    def display(self, path):
        spaces = set(path.path)
        print(path.word_part)
        for i in xrange(len(self.mat)):
            for j in xrange(len(self.mat)):
                if (i, j) in spaces:
                    print(colored(self.mat[i][j].upper(), 'red')),
                else:
                    print(self.mat[i][j]),
            print("")
        print("")


    def _get_directions(self, row, col):
        retval = list()
        for i in xrange(-1,2):
            for j in xrange(-1,2):
                if i == 0 and j == 0:
                    continue
                new_row = row + i
                new_col = col + j
                if new_row < 0 or new_row >= len(self.mat):
                    continue
                if new_col < 0 or new_col >= len(self.mat[0]):
                    continue
                retval.append((new_row,new_col))
        return retval

    def _solve(self, row, col, path, used):
        retval = set()
        if path.word_part not in self.subwords:
            return retval
        if path.word_part in self.dictionary:
            retval.add(path)
        directions = self._get_directions(row,col)
        for new_row, new_col in directions:
            if used[new_row][new_col]:
                continue
            letter = self.mat[new_row][new_col]
            new_path = Path(letter, (new_row, new_col), path)
            used[new_row][new_col] = True
            retval.update(self._solve(new_row, new_col, new_path, used))
            used[new_row][new_col] = False
        return retval

    def _create_subwords(self):
        self.dictionary = set(filter(lambda x: len(x) >= 3, self.dictionary))
        self.subwords = set()
        for word in self.dictionary:
            for i in xrange(1, len(word)+1):
                self.subwords.add(word[0:i])


if __name__ == "__main__":
    dictionary = [x.strip() for x in open("dictionary.txt").readlines()]
    board = Board("twyrenphgscroznse", dictionary)
    paths = board.solve()
    paths = sorted(paths, key=lambda x: len(x.word_part), reverse=True)
    for path in paths:
        board.display(path)
