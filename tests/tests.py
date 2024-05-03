DOCTOR_PATTERN_LIST: list = [
    # r"Dr\s+(\w+\s+\w+)",                                    #
    r"A/PROF\s+(\w+\s+\w+)",
    r"([A-Z][a-z]+ [A-Z][a-z]+) \(Prov",
    # r"Dr\s+[A-Za-z]+\s+[A-Za-z]+",
    # r'Dr\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)?',
    # r'Dr\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)?(?:\s+[A-Z][a-z]+)?',
    r'Dr\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:-[A-Z][a-z]+)?',
]