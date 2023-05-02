from vocabulary.lib.parsing_dict import *

if __name__ == '__main__':
    args = parse_args()

    if args.user_name is None:
        user = input('you may specify user for tracking progress (press enter to skip): ')
        args.user_name = user if user != '' else None

    print(f'logged as {args.user_name}')

    dictionary = parse_dictionary(args)

    db_path = os.path.join('vocabulary', 'db', 'translation_exercise_results.csv')
    db_handler = TranslationExerciseDBHandler(db_path)

    rng = default_rng()

    print(f'number of words in dictionary: {dictionary.length()}', end='\n\n')
    # todo print number of translations ?

    user_input = 'y'
    while user_input.lower() != 'n' and dictionary is not None and dictionary.length() > 0:
        if args.user_name is not None:
            random_word_with_translation = dictionary.smart_random_dict_entry_with_translation(db_handler,
                                                                                               user=args.user_name,
                                                                                               rng=rng)  # todo in the future parameterize it ?
        else:
            random_word_with_translation = dictionary.random_entry_with_translation(rng)

        entry = random_word_with_translation.entry
        word_pl = random_word_with_translation.translation

        word_original = entry.head.base

        print(word_pl)

        answer = input('translation: ')

        is_correct = weak_equals(answer, word_original)

        if is_correct:
            print('correct')
            if args.remove:
                dictionary.remove_single_translation(entry, word_pl)
                if dictionary.length() % 10 == 0:
                    print(f'{dictionary.length()} words left in dict')
        else:
            print(f'wrong. correct answer is "{word_original}" ({entry.example})')
            # todo if another translation from dict was given print it's meaning - not that easy. it may be in original dict but not after some removals
            # actually sp,e translations may unequivocal (np. także -> etiam, quoque)

        if args.user_name is not None:
            db_handler.update_db(user=args.user_name, word_pl=word_pl,
                                 lang=args.language, translation=word_original,
                                 was_correct=is_correct)

        print('')

        # todo ask about all possible forms and translations

    print('terminating..')