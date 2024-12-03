import requests
import json
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO

def load_image(url): # функция возвращает эскиз изображения, полученный по переданной в функцию ссылке
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        img = Image.open(image_data)
        img.thumbnail((80, 80), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        mb.showerror("Ошибка",f"Ошибка при загрузке изображения!\n Проверьте подключение к сети!\n\n {e}")
        im_label.config(image="")
        return None

def update_labels(event): # функция обновляет метки с логотипом и выводом курса криптовалюты
    name = combobox.get()
    if name in ccur_names:
        img = load_image(images[name])
        output_label.config(text="")
        if img:
            im_label.config(image=img)
            im_label.image = img
    else:
        output_label.config(text=f"Валюта {name} не найдена.")
        im_label.config(image="")
        mb.showerror("Ошибка", f"Валюта {name} не найдена.")
                    # отправляет get-запрос, соответствующий выбранной криптовалюте
# и возвращает курс выбранной валюты к доллару в нужную метку
def exchange():
    name = combobox.get()
    if name:
        if name in ccur_names:
            try:
                rsp = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ccur_id[name]}&vs_currencies=usd")
                rsp.raise_for_status()
                data = rsp.json()
                exchange_rate = data[ccur_id[name]]['usd']
                output_label.config(text=f"{ccur_id[name]} to usd exchange rate: {exchange_rate:.1f}")
            except Exception as e:
                mb.showerror("Ошибка", f"Похоже, нет соединения. Ошибка!\n\n {e}.")
        else:
            mb.showerror("Ошибка", f"Валюта {name} не найдена.")
    else:
        mb.showwarning("Внимание","Выберите код валюты")
flag = 0
 # Отправляем get-запрос, чтобы получить идентификаторы доступных криптовалют и ссылки на их логотипы
try:
    d=requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd")
    lst = d.json()
    ccur_names = []  # список имен доступных криптовалют
    ccur_id = {}  # словарь, где ключами являются названия криптовалют, а значениями их идентификаторы
    images = {}  # словарь, где ключами являются названия криптовалют, а значениями ссылки на их логотипы

    for i in lst:
        ccur_names.append(i["name"])
        ccur_id[i["name"]] = i["id"]
        images[i["name"]] = i["image"]
except Exception as e:
    mb.showerror("Ошибка",f"Данные не загружены. Нет доступа к нужному ресурсу.\n\n{e}")
    flag = 1 # Если данные не загрузились, надо закрыть основное окно

# В начало списка добавлено значение 'PickMeIamFake' с целью изучения реакции программы на ошибки
Ccur_names = ['PickMeIamFake','Bitcoin', 'Ethereum', 'Tether', 'Solana',
              'BNB', 'XRP', 'Dogecoin', 'USDC', 'Cardano',
              'Lido Staked Ether', 'TRON', 'Avalanche',
              'Toncoin', 'Wrapped stETH', 'Shiba Inu',
              'Stellar', 'Wrapped Bitcoin', 'Polkadot',
              'Chainlink', 'WETH', 'Bitcoin Cash', 'Sui',
              'Pepe', 'NEAR Protocol', 'LEO Token', 'Uniswap',
              'Litecoin', 'Wrapped eETH', 'Aptos', 'Internet Computer',
              'Hedera', 'USDS', 'Ethereum Classic', 'Cronos', 'POL (ex-MATIC)',
              'Render', 'Bittensor', 'Ethena USDe', 'Artificial Superintelligence Alliance',
              'Kaspa', 'Arbitrum', 'Celestia', 'Dai', 'Filecoin', 'Stacks',
              'WhiteBIT Coin', 'VeChain', 'MANTRA', 'Bonk', 'OKB', 'Cosmos Hub',
              'Aave', 'dogwifhat', 'Optimism', 'Immutable', 'Monero', 'Mantle', 'Fantom',
              'Injective', 'Sei', 'Algorand', 'The Graph', 'Bitget Token', 'Binance-Peg WETH',
              'FLOKI', 'First Digital USD', 'Ethena', 'Theta Network', 'Rocket Pool ETH',
              'THORChain', 'Worldcoin', 'Coinbase Wrapped BTC', 'Mantle Staked Ether',
              'Pyth Network', 'Maker', 'Brett', 'Renzo Restaked ETH', 'Raydium', 'Ondo',
              'GALA', 'Lido DAO', 'Jupiter', 'Solv Protocol SolvBTC', 'The Sandbox', 'Gate',
              'KuCoin', 'Bitcoin SV', 'Arweave', 'Flow', 'Quant', 'Starknet', 'BitTorrent', 'Beam',
              'Tezos', 'Polygon', 'Marinade Staked SOL', 'Flare',
              'Popcat', 'EOS']

root = Tk()
root.title("Курсы обмена криптовалют.")
root.geometry("500x400")

Label(text="Выберите криптовалюту. Сначала PickMeIamFake", bg = "yellow", fg ="brown").pack(padx = 10, pady = 10)
Label(text="Протестируйте программу при подключенной сети и при отсутствии соединения", bg = "yellow", fg ="brown").pack(padx = 10, pady = 10)
# Создаем combobox и передаем туда список названий криптовалют, полученный в результате обработки get-запроса
combobox = ttk.Combobox(values = Ccur_names)
combobox.pack(padx = 10, pady = 10)

# Создаем метку для вывода логотипа криптовалюты
im_label = ttk.Label()
im_label.pack(padx = 10, pady = 10)

# Создаем метку для вывода результата работы программы
output_label = ttk.Label()
output_label.pack(padx = 10, pady = 10)

# При выборе значений в combobox метки будут обновляться
combobox.bind("<<ComboboxSelected>>", update_labels)

Button(text=f"Получить курс обмена к доллару", command = exchange).pack(padx = 10, pady =10)

if flag == 1: root.destroy()
root.mainloop()