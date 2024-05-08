def exam_evaluations(answers: list, coefficient_number: int) -> tuple[float, int, int, int]:
    true_answers_count = answers.count(True)
    false_answers_count = answers.count(False)
    none_answers_count = answers.count(None)

    how_many_to_decrease_from_true_answers = false_answers_count // coefficient_number
    true_answers_count -= how_many_to_decrease_from_true_answers

    percentage = (100 * true_answers_count / len(answers))

    return percentage, true_answers_count, false_answers_count, none_answers_count
