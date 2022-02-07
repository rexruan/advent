
"""
You find the original question here:
https://adventofcode.com/2021/day/25
"""

class Sea:

    def __init__(self, input):
        """
        input is lines of strings
        """
        self.sea = [list(line.strip()) for line in input]
        self.rows = len(self.sea)
        self.columns = len(self.sea[0])
        self.step = 0
      
    def _step(self):
      
        moved = False
        sea = [
          [ '.' for _ in range(self.columns) ] \
          for _ in range(self.rows)
        ]

        for cucumber in ['>', 'v']:
            for ri, row in enumerate(self.sea):
                for ci, cell in enumerate(row):
                    if cucumber == cell == '>':
                        next_index = ci + 1 if ci + 1 < self.columns else 0
                        if row[next_index] == '.':
                            sea[ri][next_index] = cell
                            moved = True
                        else:
                            sea[ri][ci] = cell
                    elif cucumber == cell == 'v':
                        next_index = ri + 1 if ri + 1 < self.rows else 0
                        if sea[next_index][ci] == '>' or self.sea[next_index][ci] == 'v':
                            sea[ri][ci] = cell
                        else:
                            sea[next_index][ci] = cell
                            moved = True
        
        self.sea = sea
        self.step += 1
        return moved
    
    def run(self):
        moving = True
        while moving:
            moving = self._step()


def main():
    with open('input', 'r') as f:
        lines = f.readlines()
        sea = Sea(lines)
        sea.run()
        print(sea.step)


if __name__ == '__main__':
    main()
    
    