def load_questions(test_data):
    qus = {}
    num = 1
    for data in test_data["questions"]:
        qus[num] = data
        num += 1
    return qus
