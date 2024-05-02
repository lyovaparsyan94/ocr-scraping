def remove_substrings(self, names):
    candidate1 = ''
    candidate2 = ''
    for word in names:
        for similar_word in names:
            if similar_word in word:
                candidate2 = similar_word
                if candidate2 != word:
                    candidate1 = word
                    if candidate1 != '' or candidate2 != '':
                        if len(candidate2) >= len(candidate1) > 0 and candidate1 in candidate2:
                            names.remove(candidate1)
                            self.remove_substrings(names)
                        elif len(candidate1) >= len(candidate2) > 0 and candidate2 in candidate1:
                            names.remove(candidate2)
                            self.remove_substrings(names)
    if candidate1 == '' or candidate2 == '':
        return names