from functools import lru_cache

def score(file1: str, file2: str) -> float:
    files = FilePair(file1, file2)
    return files.levenshtein() / len(files)
class FilePair:
    def __init__(self, filename1: str, filename2: str):
        self.file1 = open(filename1)
        self.s1 = self.file1.read()
        self.file2 = open(filename2)
        self.s2 = self.file2.read()
        # you really shouldn't store massive strings in memory
        # ideally, we would access files in chunks
        # well, that's a TODO

    def __len__(self):
        return max(len(self.s1), len(self.s2))
    def __getitem__(self, i) -> str:
        if i == 0:
            if not self.s1:
                s1 = self.file1.read()
            return s1
        elif i == 1:
            if not self.s2:
                s2 = self.file2.read()
            return s2

    def levenshtein(self) -> int:
        n, m = len(self.s1), len(self.s2)
        d = []
        for i in range(n):
            d.append([])
            for j in range(m):
                d[-1].append(0)
                if i == 0 and j == 0:
                    d[i][j] = 0
                elif j == 0:
                    d[i][j] = i
                elif i == 0:
                    d[i][j] = j
                else:
                    if self.s1[i] == self.s2[j]:
                        d[i][j] = min(
                            d[i][j - 1] + 1,
                            d[i - 1][j] + 1,
                            d[i - 1][j - 1]
                        )
                    else:
                        d[i][j] = min(
                            d[i][j - 1] + 1,
                            d[i - 1][j] + 1,
                            d[i - 1][j - 1] + 1
                        )
        return d[n - 1][m - 1]


    @lru_cache(None)
    def _levenshtein_recursion_(self, i, j) -> int:
        if i == 0 and j == 0:
            return 0
        elif j == 0:
            return i
        elif i == 0:
            return j
        else:
            if self.s1[i] == self.s2[j]:
                return min(
                    self._levenshtein_recursion_(i, j - 1) + 1,
                    self._levenshtein_recursion_(i - 1, j) + 1,
                    self._levenshtein_recursion_(i - 1, j - 1)
                )
            else:
                return min(
                    self._levenshtein_recursion_(i, j - 1) + 1,
                    self._levenshtein_recursion_(i - 1, j) + 1,
                    self._levenshtein_recursion_(i - 1, j - 1) + 1
                )
    # this consumes an awful lot of memory