letters = {
    'а' : 'a',
    'б' : 'b',
    'в' : 'v',
    'г' : 'g',
    'д' : 'd',
    'е' : 'e',
    'ё' : 'e',
    'ж' : 'zh',
    'з' : 'z',
    'и' : 'i',
    'й' : 'i',
    'к' : 'k',
    'л' : 'l',
    'м' : 'm',
    'н' : 'n',
    'о' : 'o',
    'п' : 'p',
    'р' : 'r',
    'с' : 's',
    'т' : 't',
    'у' : 'u',
    'ф' : 'f',
    'х' : 'h',
    'ц' : 'ts',
    'ч' : 'ch',
    'ш' : 'sh',
    'щ' : 'sch',
    'ъ' : '',
    'ь' : '',
    'ы' : 'y',
    'э' : 'e',
    'ю' : 'yu',
    'я' : 'ia',
}


def transform_to_eng(text: str):
    text = text.replace(' ', '-').lower()
    slug_string = ''
    for ch in text:
        slug_string += letters.get(ch, ch)
    return slug_string
