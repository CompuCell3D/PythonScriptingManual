def areCellsDifferent(self, _cell1, _cell2):
    if (_cell1 and _cell2 and _cell1.this != _cell2.this) or \
            (not _cell1 and _cell2) or (_cell1 and not _cell2):
        return 1
    else:
        return 0
