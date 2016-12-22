"""
day1
"""

from seq import Op, Seq

DATA = "L5, R1, R4, L5, L4, R3, R1, L1, R4, R5, L1, L3, R4, L2, L4, R2, L4, L1, R3, R1, R1, L1, R1, L5, R5, R2, L5, R2, R1, L2, L4, L4, R191, R2, R5, R1, L1, L2, R5, L2, L3, R4, L1, L1, R1, R50, L1, R1, R76, R5, R4, R2, L5, L3, L5, R2, R1, L1, R2, L3, R4, R2, L1, L1, R4, L1, L1, R185, R1, L5, L4, L5, L3, R2, R3, R1, L5, R1, L3, L2, L2, R5, L1, L1, L3, R1, R4, L2, L1, L1, L3, L4, R5, L2, R3, R5, R1, L4, R5, L3, R3, R3, R1, R1, R5, R2, L2, R5, L5, L4, R4, R3, R5, R1, L3, R1, L2, L2, R3, R4, L1, R4, L1, R4, R3, L1, L4, L1, L5, L2, R2, L1, R1, L5, L3, R4, L1, R5, L5, L5, L1, L3, R1, R5, L2, L4, L5, L1, L1, L2, R5, R5, L4, R3, L2, L1, L3, L4, L5, L5, L2, R4, R3, L5, R4, R2, R1, L5"

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def day1(data):

    # Move 
    def move(state, instruction):
        position, orientation = state
        direction, distance = instruction
        rotation = 3 if direction == 'L' else 1
        new_orientation = DIRECTIONS[(DIRECTIONS.index(orientation) + rotation) % 4]
        new_position = (
            position[0] + new_orientation[0] * distance,
            position[1] + new_orientation[1] * distance,
        )
        print(position, orientation, direction, distance, new_position, new_orientation)
        return new_position, new_orientation

    initial_state = ((0, 0), (0, 1))

    # Parse serialized data into instructions.
    state = (
        Seq(data.split(', '))
            .map(lambda arg: (arg[0], int(arg[1:])))
            .fold_left(initial_state, move)
    )
    position, orientation = state
    print('distance {0}'.format(abs(position[0]) + abs(position[1])))

if __name__ == '__main__':
    day1(DATA)
