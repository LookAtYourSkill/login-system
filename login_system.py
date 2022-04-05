import socket
import json
from textwrap import dedent
import time

from utils import get_hashed_password, check_password
# TODO: IP Check einführen, dass man nur noch 1 Account pro IP haben kann


def run():
    with open('data.json', 'r', encoding='UTF-8') as data_file:
        data = json.load(data_file)

    print(dedent(
        """
        <###########################################################>
        <##>Welcome to the Simple Login System by LookAtYourSkill<##>
        <###########################################################>
        Was möchtest du machen:
            -> login
            -> register
            -> change
            -> beenden
        """
    ))
    while True:
        what = input(
            data["texts"]["what.message"]
        )
        if str(what) == 'login':
            user_login()
        elif str(what) == 'register':
            register()
        elif str(what) == 'change':
            change_status()
        elif str(what) == 'beenden':
            print(
                data["texts"]["5sec.message"]
            )
            time.sleep(5)
            break


def user_login():
    with open('data.json', 'r', encoding='UTF-8') as data_file:
        data = json.load(data_file)

    login = input(
        data["texts"]["login.message"]
    )

    if str(login) == 'Nein' or str(login) == 'nein':
        with open('accounts.json', 'r', encoding='UTF-8') as login_system_data:
            login_data = json.load(login_system_data)

        username = input(
            data["texts"]["username.message"]
        )

        if str(username) not in login_data["accounts"]:
            try:
                login_data["accounts"][str(username)] = {}
                login_data["accounts"][str(username)]["Name"] = str(username)
                login_data["accounts"][str(username)]["Passwort"] = None
                login_data["accounts"][str(username)]["Backup_Unhashed_Passwort"] = None
                login_data["accounts"][str(username)]["Permission"] = data["perms"]["user.permission"]
                login_data["accounts"][str(username)]["IP"] = socket.gethostbyname(
                    socket.gethostname()
                )

                with open('accounts.json', 'w', encoding='UTF-8') as dump_file:
                    json.dump(login_data, dump_file, indent=4)
            except TypeError:
                print(
                    data["texts"]["error.json.message"]
                )

            if not login_data["accounts"][str(username)]["Passwort"]:
                normal_password = input(
                    data["texts"]["password.message"]
                )
                hashed_password = get_hashed_password(
                    normal_password.encode('UTF-8')
                )

                try:
                    login_data["accounts"][str(username)]["Backup_Unhashed_Passwort"] = str(normal_password)
                    login_data["accounts"][str(username)]["Passwort"] = str(hashed_password)

                    with open(
                        'accounts.json',
                        'w',
                        encoding='UTF-8'
                    ) as dump_file:
                        json.dump(login_data, dump_file, indent=4)
                except TypeError:
                    print(
                        data["texts"]["error.json.message"]
                    )

                print(
                    data["texts"]["register.successful.message"]
                )
                print(
                    data["texts"]["5sec.message"]
                )
                time.sleep(5)

            else:
                print(
                    'Etwas ist Fehlgeschlagen! Versuche es erneut!'
                )
        else:
            print(
                'Der Nutzername ist bereits vergeben!'
            )

    elif str(login) == 'Ja' or str(login) == 'ja':
        with open('accounts.json', 'r', encoding='UTF-8') as login_system_data:
            login_data = json.load(login_system_data)

        username = input(data["texts"]["username.message"])
        if str(username) in login_data["accounts"]:
            print(
                f'Nutzername "{str(username)}" wurde erfolgreich gefunden!'
            )
            normal_password = input(
                data["texts"]["password.message"]
            )
            try:

                if check_password(
                    normal_password.encode('UTF-8'),
                    str(login_data["accounts"][str(username)]["Passwort"]).encode('UTF-8')[2:][:60]
                ):
                    print(
                        f'Du wurdest erfolgreich als "{str(username)}" angemeldet!'
                    )
                    print(
                        data["texts"]["5sec.message"]
                    )
                    time.sleep(5)
                else:
                    print(
                        data["texts"]["error.password.message"]
                    )
            except TypeError:
                print(
                    data["texts"]["error.encode.message"]
                )
            except ValueError:
                print(
                    data["texts"]["error.salt.message"]
                )
        else:
            print(
                'Nutzername konnte nicht gefunden werden!'
            )
    else:
        print(
            'Falsche Eingabe! Bitte beachte die Nachricht des Programms!'
        )


def register():
    with open('accounts.json', 'r', encoding='UTF-8') as login_system_file:
        login_data = json.load(login_system_file)

    with open('data.json', 'r', encoding='UTF-8') as data_file:
        data = json.load(data_file)

    username = input(
        data["texts"]["username.message"]
    )

    if str(username) in login_data["accounts"]:
        print('Ein Account mit dem Namen existiert bereits!')

    elif str(username) not in login_data["accounts"]:
        print('Nutzername verfügbar und wurde gesichert!')

        try:
            login_data["accounts"][str(username)] = {}
            login_data["accounts"][str(username)]["Name"] = str(username)
            login_data["accounts"][str(username)]["Passwort"] = None
            login_data["accounts"][str(username)]["Permission"] = data["perms"]["user.permission"]
            login_data["accounts"][str(username)]["IP"] = socket.gethostbyname(
                socket.gethostname()
            )
            with open('accounts.json', 'w', encoding='UTF-8') as dump_file:
                json.dump(login_data, dump_file, indent=4)
        except TypeError:
            print(
                data["texts"]["error.json.message"]
            )

        password = input(
            data["texts"]["password.message"]
        )
        hashed_password = get_hashed_password(
            str(password).encode('UTF-8')
        )

        if not login_data["accounts"][str(username)]["Passwort"]:
            login_data["accounts"][str(username)]["Passwort"] = str(hashed_password)

            with open('accounts.json', 'w', encoding='UTF-8') as dump_file:
                json.dump(login_data, dump_file, indent=4)
            print(
                data["texts"]["register.successful.message"]
            )
            print(
                data["texts"]["5sec.message"]
            )
            time.sleep(5)
        else:
            print(
                'Dieser Account besitzt bereits ein Passwort!'
            )
    else:
        print(
            'Unbekannter Fehler!'
        )


def change_status():
    with open('accounts.json', 'r', encoding='UTF-8') as login_system_data:
        login_data = json.load(login_system_data)

    with open('data.json', 'r', encoding='UTF-8') as data_file:
        data = json.load(data_file)

    username = input(data["texts"]["username.message"])
    if str(username) not in login_data["accounts"]:
        print(
            data["texts"]["error.username_not_found.message"]
        )

    else:
        if login_data["accounts"][str(username)]["Permission"] == data["perms"]["user.permission"]:
            print(
                f'Derzeit sind deine Permission auf "{login_data["accounts"][str(username)]["Permission"]}" gesetzt!'
            )
            universal = input(
                f'Bitte gib das Universal Passwort ein, um deine Permission auf "{data["perms"]["admin.permission"]}" zu ändern!\n'
                'Passwort: '
            )

            if str(universal) == data["admin_perms"]["universal_password"]:
                login_data["accounts"][str(username)]["Permission"] = data["perms"]["admin.permission"]

                with open('accounts.json', 'w', encoding='UTF-8') as dump_file:
                    json.dump(login_data, dump_file, indent=4)

                print(
                    f'Deine Permission wurden Erfolgreich auf "{login_data["accounts"][str(username)]["Permission"]}" geändert!'
                )
            else:
                print(
                    'Anscheinend war das "Universal Passwort" falsch! Deine Permission wurden nicht geändert!'
                )
        else:
            print(
                f'Deine Permission sind bereits auf "{login_data["accounts"][str(username)]["Permission"]}"!'
            )
            user = input(
                'Falls du deine Permission allerdings wieder zu "user" ändern willst, \n'
                '   -> kannst du einfach "Ja" in die Konsole schreiben!\n'
                '   -> Falls nicht, kannst du "Nein" in die Konsole schreiben!\n'
                'Deine Antwort: '
            )

            if str(user) == 'Ja' or str(user) == 'ja':
                login_data["accounts"][str(username)]["Permission"] = data["perms"]["user.permission"]
                with open('accounts.json', 'w', encoding='UTF-8') as dump_file:
                    json.dump(login_data, dump_file, indent=4)

                print(
                    f'Deine Permission wurden Erfolgreich zu "{login_data["accounts"][str(username)]["Permission"]}" geändert!'
                )

            elif str(user) == 'Nein' or str(user) == 'nein':
                login_data["accounts"][str(username)]["Permission"] = data["perms"]["admin.permission"]
                print(
                    f'An deinem Permission hat sich nichts geändert! Sie sind auf "{login_data["accounts"][str(username)]["Permission"]}" gesetzt!'
                )
            else:
                print(
                    'Bitte verwende "Ja" oder "Nein", etwas anderes wird nicht erkannt!'
                )
                return


if __name__ == '__main__':
    run()
