def locked(boxes, goals, walls):
    for box in boxes:
        if box not in goals:
            grid = ((box[0] - 1, box[1] - 1), (box[0] - 1, box[1] + 0), (box[0] - 1, box[1] + 1),
                    (box[0] + 0, box[1] - 1), (box[0] + 0, box[1] + 0), (box[0] + 0, box[1] + 1),
                    (box[0] + 1, box[1] - 1), (box[0] + 1, box[1] + 0), (box[0] + 1, box[1] + 1))

            # Corner 0
            if grid[0] in boxes + walls:
                if grid[3] in boxes + walls:
                    if grid[1] in boxes + walls:
                        return True
            elif grid[0] in walls:
                if grid[5] in walls and grid[1] in boxes:
                    return True
                if grid[7] in walls and grid[3] in boxes:
                    return True
            else:
                if grid[3] in walls and grid[1] in walls:
                    return True

            # Corner 2
            if grid[2] in boxes + walls:
                if grid[1] in boxes + walls:
                    if grid[5] in boxes + walls:
                        return True
            elif grid[2] in walls:
                if grid[7] in walls and grid[5] in boxes:
                    return True
                if grid[3] in walls and grid[1] in boxes:
                    return True
            else:
                if grid[1] in walls and grid[5] in walls:
                    return True

            # Corner 8
            if grid[8] in boxes + walls:
                if grid[5] in boxes + walls:
                    if grid[7] in boxes + walls:
                        return True
            elif grid[8] in walls:
                if grid[3] in walls and grid[7] in boxes:
                    return True
                if grid[1] in walls and grid[5] in boxes:
                    return True
            else:
                if grid[5] in walls and grid[7] in walls:
                    return True

            # Corner 6
            if grid[6] in boxes + walls:
                if grid[7] in boxes + walls:
                    if grid[3] in boxes + walls:
                        return True
            elif grid[6] in walls:
                if grid[1] in walls and grid[3] in boxes:
                    return True
                if grid[5] in walls and grid[7] in boxes:
                    return True
            else:
                if grid[7] in walls and grid[3] in walls:
                    return True
    
    return False