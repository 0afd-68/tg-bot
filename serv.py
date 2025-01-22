import csv

# consts
DOMEN = "https:/sokrat.ru/"
PATHWITHFILES = "sokrat"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~!*'();:@&=+$,"
MAX_URL_LEN = 8
CSV_FILE = 'data.csv'


def filewriteredirect(file,longurl:str):
    prepare = '<meta http-equiv="refresh" content="0;URL='+longurl+'"/>'
    file.write(prepare)



# генератор уникальных ключей, для того чтобы ссылки не повторялись и не было такой что ты по другой ссылке перешел
def generate(a:str,index:int = 1):
    try:
        if a[-index]==ALPHABET[-1]:
            a= a[:len(a)-index] + ALPHABET[0] + a[len(a) - (index - 1):]
            return generate(a, index + 1)
        elif a[-index]!=ALPHABET[-1]:
            for i in range(len(ALPHABET) - 1):
                if ALPHABET[i]==a[-index]:
                    a= a[:len(a)-index] + ALPHABET[i + 1] + a[len(a) - (index - 1):]
                    break
            return a
    except IndexError:
        return ALPHABET[0] + a[::]




# добавляет 2 ссылки в csv файл: длинную версию и короткую. Функция нужна для того чтобы запоминать обилие ссылок, которое возможно будет поступать на бота
def add_to_csv(file_name, *args):
    """Добавляет два элемента в CSV файл."""
    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file,delimiter='|')
        writer.writerow([s for s in args])
    print(f'Добавлено: {args[0]}, в {file_name}')





# ищет в csv файле по укороченной ссылке исходную, чтобы потом перенаправить на сайт
def search_in_csv(file_name, search_elem):
    """Ищет первый элемент в CSV файле по второму элементу."""
    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file,delimiter = '|')
        for row in reader:
            if len(row) >= 2 and row[1] == search_elem:
                return row[0]  # Возвращаем первый элемент
    return None  # Если не найдено



def search_for_stats(file_name, chatid:int):
    alllinks = []
    """Ищет первый элемент в CSV файле по второму элементу."""
    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file,delimiter = '|')
        for row in reader:
            if len(row) >= 3 and int(row[2])==chatid:
                b = [row[0],row[1]]
                alllinks.append(b)  # Возвращаем первый элемент
    return alllinks  # Если не найдено


def statists(chatid:int):
    a = search_for_stats(CSV_FILE,chatid)
    return a



# мозги этой проги, открывает файл в котором находится последний ключ для короткой ссылки(он нужен для того чтобы не в оперативке держать этот)
# потом эта функция генерирует уникальный ключ для ссылки и добавляет его в нашу бд data.csv
def create_uniqueurl(longurl:str,chatid:str):
    f = open("lastkey.txt",)
    shortlink = generate(f.read())
    f.close()
    print(longurl,shortlink)
    f = open("lastkey.txt","w")
    f.write(shortlink)
    shorturl =DOMEN+shortlink
    redir = open(PATHWITHFILES+"/"+shortlink+".html","w+")
    filewriteredirect(redir,longurl)
    add_to_csv(CSV_FILE,longurl,shorturl,chatid)
    return shorturl
