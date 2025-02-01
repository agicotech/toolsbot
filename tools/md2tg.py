import re

def markdown_to_html(text):
    # Обрабатываем блоки кода
    def code_block_replace(match):
        lang = match.group(1) or ''
        code = match.group(2).strip()
        if lang:
            return f'<pre><code class="language-{lang}">\n{code}\n</code></pre>'
        return f'<pre>\n{code}\n</pre>'
    
    text = re.sub(r'```(\w*)\n?([\s\S]*?)\n?```', code_block_replace, text)
    
    # Обрабатываем встроенный код
    text = re.sub(r'`([^`\n]+)`', r'<code>\1</code>', text)
    
    # Обрабатываем жирный, курсивный, подчеркнутый и зачеркнутый текст
    text = re.sub(r'\*\*([^*\n]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*([^*\n]+)\*', r'<i>\1</i>', text)
    text = re.sub(r'__([^_\n]+)__', r'<u>\1</u>', text)
    text = re.sub(r'~~([^~\n]+)~~', r'<s>\1</s>', text)
    
    # Обрабатываем ссылки
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    
    # Обрабатываем заголовки
    for i in range(6, 0, -1):
        text = re.sub(f'^{"#"*i}\\s+(.+)$', f'<b>\\1</b>', text, flags=re.MULTILINE)
    
    # Обрабатываем горизонтальные линии
    #text = re.sub(r'^-{3,}$|^_{3,}$|^\*{3,}$', '<hr>', text, flags=re.MULTILINE)
    
    # Обрабатываем списки
    text = re.sub(r'^\s*[-*+]\s+(.+)$', r'• \1', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+(.+)$', r'• \1', text, flags=re.MULTILINE)
    
    # Обрабатываем цитаты
    text = re.sub(r'^>\s*(.+)$', r'<blockquote>\n\1\n</blockquote>', text, flags=re.MULTILINE)
    text = text.replace('</blockquote>\n<blockquote>\n', '')
    # Удаляем лишние пробелы в начале и конце строк
    text = '\n'.join(line.strip() for line in text.split('\n'))
    
    return text

if __name__ == '__main__':
    # Пример использования
    markdown_text = """
# Заголовок

Это *курсив*, а это **жирный** текст.
Это __подчеркнутый__ и ~~зачеркнутый~~ текст.

## Подзаголовок

1. Первый элемент списка
2. Второй элемент списка

[Ссылка на Google](https://www.google.com)
[Упоминание пользователя](tg://user?id=123456789)

`print("Hello, World!")`

```python
def example():
    return "This is a multi-line code block"
```

> Это цитата
> Вторая строка цитаты

---

Конец документа.
"""

    print(markdown_to_html(markdown_text))