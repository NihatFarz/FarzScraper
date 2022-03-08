import requests
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import pickle, pyfiglet
from colorama import init, Fore
import os, random
from time import sleep

init()

lg = Fore.LIGHTGREEN_EX
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
r = Fore.RED
n = Fore.RESET
colors = [lg, r, w, cy, ye]

def banner():
    f = pyfiglet.Figlet(font='slant')
    banner = f.renderText('Telegram')
    print(f'{random.choice(colors)}{banner}{n}')
    print(r+'  Versiya: 1.1 | Owner: Nihat 「 FARZ 」'+n+'\n')


def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

while True:
    clr()
    #print(r)
    banner()
    #print(n)
    print(lg+'[1] Yeni hesablar əlavə edin'+n)
    print(lg+'[2] Bütün qadağan edilmiş hesabları filtrləyin'+n)
    print(lg+'[3] Bütün hesabların siyahısına baxın'+n)
    print(lg+'[4] Xüsusi hesabları silin'+n)
    #print(lg+'[5] Update your Genisys'+n)
    print(lg+'[5] Çıxış')
    a = int(input(f'\nSeçiminiz: {r}'))
    if a == 1:
        with open('vars.txt', 'ab') as g:
            newly_added = []
            while True:
                a = int(input(f'\n{lg}API ID: {r}'))
                b = str(input(f'{lg}API Hash: {r}'))
                c = str(input(f'{lg}Telefon Nömrəniz: {r}'))
                p = ''.join(c.split())
                pickle.dump([a, b, p], g)
                newly_added.append([a, b, p])
                ab = input(f'\nDaha çox hesab əlavə etmək istəyirsiniz?[y/n]: ')
                if 'y' in ab:
                    pass
                else:
                    print('\n'+lg+'[i] Bütün hesabları vars.txt də saxlanıldı'+n)
                    g.close()
                    sleep(3)
                    clr()
                    print(lg + '[*] Yeni hesablardan daxil olunur...\n')
                    for added in newly_added:
                        c = TelegramClient(f'sessions/{added[2]}', added[0], added[1])
                        try:
                            c.start()
                            print(f'n\n{lg}[+] Daxil oldunuz - {added[2]}')
                            c.disconnect()
                        except PhoneNumberBannedError:
                            print(f'{r}[!] {added[2]} qadağandır! 2-ci seçimdən istifadə edərək onu çıxardın')
                            continue
                        print('\n')
                    input(f'\n{lg}Əsas menyuya keçmək üçün enter düyməsini basın...')
                    break
        g.close()
    elif a == 2:
        accounts = []
        banned_accs = []
        h = open('vars.txt', 'rb')
        while True:
            try:
                accounts.append(pickle.load(h))
            except EOFError:
                break
        h.close()
        if len(accounts) == 0:
            print(r+'[!] Heç bir hesab yoxdur! Zəhmət olmasa bir hesab əlavə edin və yenidən cəhd edin')
            sleep(3)
        else:
            for account in accounts:
                api_id = int(account[0])
                api_hash = str(account[1])
                phone = str(account[2])
                client = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
                client.connect()
                if not client.is_user_authorized():
                    try:
                        client.send_code_request(phone)
                        client.sign_in(phone, input('[+] Kodu daxil edin: '))
                    except PhoneNumberBannedError:
                        print(r+str(phone) + ' qadağandır!'+n)
                        banned_accs.append(account)
            if len(banned_accs) == 0:
                print(lg+'Qadağan edilmiş hesablar yoxdur')
                input('\nƏsas menyuya keçmək üçün enter düyməsini basın')
            else:
                for m in banned_accs:
                    accounts.remove(m)
                with open('vars.txt', 'wb') as k:
                    for a in accounts:
                        Id = a[0]
                        Hash = a[1]
                        Phone = a[2]
                        pickle.dump([Id, Hash, Phone], k)
                k.close()
                print(lg+'[i] Bütün qadağan olunmuş hesablar silindi'+n)
                input('\nƏsas menyuya keçmək üçün enter düyməsini basın')
    elif a == 3:
        display = []
        j = open('vars.txt', 'rb')
        while True:
            try:
                display.append(pickle.load(j))
            except EOFError:
                break
        j.close()
        print(f'\n{lg}')
        print(f'API ID  |            API Hash              |    Nömrə')
        print(f'==========================================================')
        i = 0
        for z in display:
            print(f'{z[0]} | {z[1]} | {z[2]}')
            i += 1
        print(f'==========================================================')
        input('\nƏsas menyuya keçmək üçün enter düyməsini basın')

    elif a == 4:
        accs = []
        f = open('vars.txt', 'rb')
        while True:
            try:
                accs.append(pickle.load(f))
            except EOFError:
                break
        f.close()
        i = 0
        print(f'{lg}[i] Silmək üçün hesabı seçin\n')
        for acc in accs:
            print(f'{lg}[{i}] {acc[2]}{n}')
            i += 1
        index = int(input(f'\n{lg}[+] Seçiminiz: {n}'))
        phone = str(accs[index][2])
        session_file = phone + '.session'
        if os.name == 'nt':
            os.system(f'del sessions\\{session_file}')
        else:
            os.system(f'rm sessions/{session_file}')
        del accs[index]
        f = open('vars.txt', 'wb')
        for account in accs:
            pickle.dump(account, f)
        print(f'\n{lg}[+] Hesab Silindi{n}')
        input(f'{lg}Əsas menyuya keçmək üçün enter düyməsini basın{n}')
        f.close()
    elif a == 5:
        clr()
        banner()
        quit()
