from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make2d(list, ln):
    return [list[i*ln:i*ln+ln] for i in range((len(list)+ln-1)//ln)]

def inlbuttonblock(values, maxwidth = 2):
    def button(text, value):
        if value.startswith('ln:'):
            return InlineKeyboardButton(text=text, url=value[3:])
        elif value.startswith('http'):
            return InlineKeyboardButton(text=text, url=value)
        else:
            return InlineKeyboardButton(text=text, callback_data=value)
    if type(values) is dict:
        return InlineKeyboardMarkup(
            inline_keyboard = make2d(
                [button(i, v) for i, v in values.items()],
                maxwidth))
    else:
        return InlineKeyboardMarkup(
            inline_keyboard = make2d(
                [button(i, i) for i in values],
                maxwidth))
    
def urlbuttonblock(values, maxwidth = 2):
    return InlineKeyboardMarkup(
        inline_keyboard = make2d(
            [InlineKeyboardButton(text= i, callback_data= i, url=v) for i, v in values.items()],
            maxwidth))


class inlbuttonrow(InlineKeyboardBuilder):
    def __init__(self, btns = None):
        self.size = 0
        super().__init__()
        if btns is not None:
            self.add(btns)

    def add(self, btns):
        self.size += len(btns)
        if isinstance(btns, dict):
            return super().add(*(InlineKeyboardButton(text=text, callback_data=cbd) for text, cbd in btns))
        elif isinstance(btns, list):
            return super().add(*((InlineKeyboardButton(text=text, callback_data=text) 
                                 if type(text) == str else text) for text in btns))
    def __call__(self):
        return self.as_markup()


    def clean(self) -> None:
        self.size = 0
        return super().clean()