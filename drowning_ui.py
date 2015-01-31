from pyGTrends import pyGTrends
import time
from random import randint
import csv

from pythonosc import osc_message_builder
from pythonosc import udp_client


import sys, os

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format


# 1 listener for everything.
# recieve search:
# /search/'STRING 1,STRING 2'

# 1 sender:
# /player1/progress/ 
# /player1/reset/


google_username = 'misterdeluge@gmail.com'
google_password = 'DigitalDeluge'
csv_path = 'csv/'

if not os.path.exists(csv_path):
    os.makedirs(csv_path)

#connect to Google
connector = pyGTrends(google_username, google_password)

players = [{'id': 1,
            'ip': '10.0.1.11',
            # 'ip': '192.168.1.73',
            'port': 5001,
           },
           {'id': 2,
            'ip': '192.168.1.70',
            'port': 5001,
           }]

while True:
  terms = ['','']
  scores = [0,0]
  os.system('clear')
  cprint(figlet_format('#drowning', font='weird'),
         'blue')
  rows, cols = os.popen('stty size', 'r').read().split()
  footer = 'streaming live @ drowning.ngrok.com'

  padding = int(cols) - len(footer) - 15
  print(' '*padding + footer)

  for index, player in enumerate(players):
    term = None
    while not term:
      term = input('>>> Player %s search term: ' % player['id'])
    print('\n')
    terms[index] = term




  print("------------------------------------------------------------------------------------------")
  #make request
  query = ','.join(terms)
  connector.request_report(query)
  print("------------------------------------------------------------------------------------------")

  #download file
  filename = '-'.join(terms)
  connector.save_csv(csv_path, filename)

  csv_file = open(csv_path + filename + '.csv')
  reader = csv.reader(csv_file)

  for row in reader:
      if row and row[0].startswith('2014'):
          scores[0] += int(row[1])
          scores[1] += int(row[2])

  scores[0] = scores[0] / 52
  scores[1] = scores[1] / 52


  print('\n--- "' + terms[0] + '" scored ' + str(scores[0]))
  print('\n--- "' + terms[1] + '" scored ' + str(scores[1]))
  print('\n')

  winner = 0
  if(scores[0] > scores[1]):
    winner = 1
  elif(scores[0] < scores[1]):
    winner = 2

  if winner == 0:
    cprint(figlet_format('A TIE!', font='poison'),
           'green')
  else:
    cprint(figlet_format('Player %s WINS' % winner, font='poison'),
           'green')

  # NOTE THE REVERSED SCORES
  for (player, score, term) in zip(players, reversed(scores), terms):
    address = '/progress'
    client = udp_client.UDPClient(player['ip'], player['port'])

    msg = osc_message_builder.OscMessageBuilder(address=address)
    msg.add_arg(score)
    msg.add_arg(term)
    msg = msg.build()
    client.send(msg)

  reset = input('')
  if reset == '*':
    for player in players:
      address = '/reset'
      client = udp_client.UDPClient(player['ip'], player['port'])
      msg = osc_message_builder.OscMessageBuilder(address=address)
      msg = msg.build()
      client.send(msg)
