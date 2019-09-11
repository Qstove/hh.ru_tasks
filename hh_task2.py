import itertools

def solve_puzzle(limitations):
    field = HhRuTask(limitations)
    field.solvePuzzle()
    return field.getFieldAsTuple()


def get_visible(line):
    count = 1
    highest = line[0]
    for i in range(1, len(line)):
        if line[i] > highest:
            count += 1
            highest = line[i]
    return count


def get_possible_perm(visCount):
    all = list(itertools.permutations([1, 2, 3, 4, 5, 6]))
    posib = get_perm_list(all, visCount)
    return posib


def get_2_cues_perm(arrA, countB):
    copyA = []
    for perm in arrA: copyA.append(perm[::-1])
    posib = get_perm_list(copyA, countB)
    #print('for Nr {} the sub count is {}'.format(countB, len(posib)))
    return posib


def get_perm_list(perm_array, visCount):
    if visCount == 0: return perm_array
    posib = []
    for perm in perm_array:
        if get_visible(perm) == visCount: posib.append(perm)
    return posib


class HhRuTask:

    def __init__(self, limitations):
        self._field = [[0] * 6 for ii in range(6)]
        self.height = len(self._field)
        self.width = len(self._field[0])
        self.perm_rows = []
        self.perm_columns = []
        self.possibilityField = [[[*range(1, 7)] for jj in range(6)] for kk in range(6)]
        self.iteration = 0

        self.limitations = limitations
        self.possiblePerms = []

        for i in range(7):
            p = get_possible_perm(i)
            self.possiblePerms.append(p)
        self.__setupLines()

        self.__total_row_perm = self.get_total_row_perms()
        self.__total_col_perm = self.get_total_col_perms()

    def get_total_row_perms(self):
        multi_row = 1
        for row in self.perm_rows:
            multi_row *= len(row)
        return multi_row

    def get_total_col_perms(self):
        multi_col = 1
        for col in self.perm_columns:
            multi_col *= len(col)
        return multi_col

    def getFieldAsTuple(self):
        tup = tuple(tuple(row) for row in self._field)
        return tup


# region iteration
    def solvePuzzle(self):
        solved = False
        while not solved:
            self.recalculatePossibilityField()
            self.filterLinesByPossibilityField()
            solved = self.checkProgress() == 1
            self.iteration += 1
        return self._field

    def recalculatePossibilityField(self):
        for y in range(self.height):

            for x in range(self.width):
                r = self.__calculateCellPosibilities(y, x)
                self.possibilityField[y][x] = r
                if len(r) == 1:
                    self._field[y][x] = r[0]

    #Uses the rows & columns to find/eliminate possibilities of the target cell
    def __calculateCellPosibilities(self, y, x):
        p_row = (z[x] for z in self.perm_rows[y])
        p_col = (z[y] for z in self.perm_columns[x])
        inter = set(p_row).intersection(p_col)
        old = self.possibilityField[y][x]
        inter = set(inter).intersection(old)
        return list(inter)

    def filterLinesByPossibilityField(self):
        for y in range(self.height):
            for x in range(self.width):
                posib = self.possibilityField[y][x]
                self.perm_rows[y] = [perm for perm in self.perm_rows[y] if perm[x] in posib]
                self.perm_columns[x] = [perm for perm in self.perm_columns[x] if perm[y] in posib]

    def checkProgress(self):
        new_row_perm = self.get_total_row_perms()
        row_progress = self.__total_row_perm / new_row_perm
        self.__total_row_perm = new_row_perm

        new_col_perm = self.get_total_col_perms()
        col_progress = self.__total_col_perm / new_col_perm
        self.__total_col_perm = new_col_perm
        return max(row_progress, col_progress)

# endregion

    def __setupLines(self):
        for x in range(6):
            nrX = self.limitations[17 - x]
            column = get_2_cues_perm(self.possiblePerms[nrX], self.limitations[x])
            self.perm_columns.append(column)

        for y in range(23, 17, -1):
            nrY = self.limitations[29 - y]
            row = get_2_cues_perm(self.possiblePerms[nrY], self.limitations[y])
            self.perm_rows.append(row)

inputData = input()
inputDataFormat = tuple(map(int, inputData.split(',')))
result = solve_puzzle(inputDataFormat)
outputData = []
for t in result: 
    for x in t: 
        outputData.append(x)

print(*outputData, sep = ",") 
