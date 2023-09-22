import json
import os


def parse_config(path: str) -> dict[str, str | int | list]:
    """Return a dict with specified config file keys and values. If file isn't found create a new one."""
    try:
        with open(path, 'r', encoding='UTF-8') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        config = {
            'token': '',
            'owner_id': 0,
            'chat_ids': [],
            'include_directories': [],
            'exclude_directories': [],
            'no_caption_directories': [],
            'kick_delay': 0,
            'messages_text': {
                'joined': ('Привет, {username}! Реши капчу, пожалуйста\n'
                           'В своём следующем сообщении напиши цифры от 1 до 9, соответствующие картинкам '
                           '(отсчёт начинается слева сверху)'),
                'answer': ('Твой ответ содержит {correct} правильных ответов. {congrats}\n'
                           'Правильные ответы: {answers}'),
                'no_nums': 'Ни одной цифры не написал...',
                'no_text': 'Это даже не текст...',
                '0_correct': 'Что-то грустно...',
                '1_correct': 'Ну хоть что-то...',
                '2_correct': 'Лучше, чем хоть что-то...',
                '3_correct': 'Неплохо!',
                '4_correct': 'Поздравляю!',
                'incorrect': 'Кажется ты решал как то не так...'
            }
        }

        with open(path, 'w', encoding='UTF-8') as config_file:
            json.dump(config, config_file, indent=4, ensure_ascii=False)

        raise FileNotFoundError(f'{os.path.basename(path)} file wasn\'t found. Fill the fields in the created file.')