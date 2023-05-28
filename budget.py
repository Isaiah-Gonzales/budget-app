class Category:

  #initialize instance variable
  def __init__(self, name, ledger=None):
    self.name = name
    if ledger is None:
      ledger = []
    self.ledger = ledger

  #deposit: add amount with description
  def deposit(self, amount, description=""):
    deposit = {"amount": amount, "description": description}
    self.ledger.append(deposit)

  #find amounts in ledger and sum them to get the balance
  def get_balance(self):
    amounts = []
    balance = 0
    #find amount using colon in front of it and comma behind it
    for transaction in self.ledger:
      amount = transaction['amount']
      amounts.append(amount)
    for x in amounts:
      balance = balance + float(x)
    return balance

  #check if amount is greater than running balance
  def check_funds(self, amount):
    if self.get_balance() >= amount:
      return True
    else:
      return False

  #define withdraw method, uses check_funds methods before adding to ledger
  def withdraw(self, amount, description=None):
    if description is None:
      description = ""
    if self.check_funds(amount) is True:
      withdrawal = {"amount": -amount, "description": description}
      self.ledger.append(withdrawal)
      return True
    else:
      return False

#define transfer method, move money from one category to another

  def transfer(self, amount, destination):
    if self.check_funds(amount) is True:
      withdraw_description = "Transfer to " + destination.name
      self.withdraw(float(amount), withdraw_description)
      destination.deposit(amount, "Transfer from " + self.name)
      return True
    else:
      return False


#Define what should happen when the budget object is printed

  def __str__(self):
    #first, define title as self.name nested within asterisks
    number_lasterisks = 15 - (int(len(self.name) / 2))
    if (len(self.name) % 2) == 0:
      number_rasterisks = number_lasterisks
    else:
      number_rasterisks = number_lasterisks - 1
    lasterisks = []
    rasterisks = []
    counter = 0
    while counter < number_lasterisks:
      lasterisks.append("*")
      counter += 1
    counter = 0
    while counter < number_rasterisks:
      rasterisks.append("*")
      counter += 1
    title = str(''.join(lasterisks) + self.name + ''.join(rasterisks))

    #next, list items in ledger with formatting
    items = []
    for transaction in self.ledger:
      #find and define amounts from ledger, fix length to 7 characters
      amount = transaction['amount']
      amount = f'{float(amount):.02f}'
      if len(amount) > 7:
        amount = amount[0:6]
      #Fill amount with leading " ", until length is 7
      if len(amount) < 7:
        formatter = []
        counter = len(amount)
        while counter < 7:
          formatter.append(" ")
          counter += 1
        formatter.append(amount)
        amount = ''.join(formatter)
      #find and define descritpions from ledger, fix length to 23 characters
      description = transaction['description']
      if len(description) > 23:
        description = description[0:23]
      #Fill description with trailing " ", until length is 23
      if len(description) < 23:
        formatter = [description]
        counter = len(description)
        while counter < 23:
          formatter.append(" ")
          counter += 1
        description = ''.join(formatter)
      items.append(description + amount + "\n")
    item = ''.join(items)
    #return the formatted budget object
    formatted = title + "\n" + item + "Total: " + str(self.get_balance())
    return formatted


def create_spend_chart(categories):
  #function uses withdrawals and current balance to calc % spent, adds to list percents
  percents = []
  for category in categories:
    withdrawals = []
    nums = []
    for x in category.ledger:
      amount = x['amount']
      if amount < 0:
        withdrawals.append(amount)
    for x in withdrawals:
      num = float(x)
      nums.append(num)
    money_spent = sum(nums)
    total = abs(money_spent) + category.get_balance()
    percent_spent = 100 - (((total + money_spent) / (total)) * 100)
    rounded_percent = int(percent_spent / 10)
    percents.append(rounded_percent)
  
  #grapher function adds "o" if rounded percent is >= the tens place
  graph = []
  hundreds = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
  def grapher(num):
    if num == 10:
      tens = [str(num * 10) + "| "]
    elif num == 0:
      tens = ["  " + str(num * 10) + "| "]
    else:
      tens = [" " + str(num * 10) + "| "]
    #creates plot for category1, always happens
    if percents[0] >= num:
      tens.append("o")
      tens.append("\n")
    else:
      tens.append(" ")
      tens.append("\n")
    #creates plot for category2 if present
    if len(categories) >= 2:
      if percents[1] >= num:
        tens.remove("\n")
        tens.append("  o")
        tens.append("\n")
      else:
        tens.remove("\n")
        tens.append("   ")
        tens.append("\n")
    #creates plot for category3 if present
    if len(categories) >= 3:
      if percents[2] >= num:
        tens.remove("\n")
        tens.append("  o  ")
        tens.append("\n")
      else:
        tens.remove("\n")
        tens.append("     ")
        tens.append("\n")
    #creates plot for category4 if present
    if len(categories) == 4:
      if percents[3] >= num:
        tens.remove("\n")
        tens.append("  o")
        tens.append("\n")
      else:
        tens.remove("\n")
        tens.append("   ")
        tens.append("\n")
    ten = ''.join(tens)
    graph.append(ten)

  #go through each of the numbers in "hundreds" and create a plot using the grapher function
  for x in hundreds:
    grapher(x)
  plot = ''.join(graph)

  #printed appropriate number of dashes
  dashes = ["    ---"]
  if len(categories) == 2:
    dashes.append("----")
  if len(categories) == 3:
    dashes.append("-------")
  if len(categories) == 4:
    dashes.append("----------")
  dash = ''.join(dashes)

  names = []
  if len(categories) == 1:
    for x in categories[0].name:
      names.append(" " + x + " ")
      names.append("\n")

  if len(categories) ==2:
    firstname = cateogries[0].name
    secondname = categories[1].name
    longest = max(len(firstname, len(secondname)))
    while len(firstname) < longest:
      firstname += " "
    while len(secondname) < longest:
      secondname += " "
    for x,y in zip(firstname, secondname):
      names.append(" " + x + "  " + y + "  ")
      names.append("\n")
      
  if len(categories) ==3:
    firstname = categories[0].name
    secondname = categories[1].name
    thirdname = categories[2].name
    longest = max(len(firstname), len(secondname), len(thirdname))
    while len(firstname) < longest:
      firstname += " "
    while len(secondname) < longest:
      secondname += " "
    while len(thirdname) < longest:
      thirdname += " "
    for x,y,z in zip(firstname, secondname, thirdname):
      names.append("     " + x + "  "  + y + "  " + z + "  ")
      names.append("\n")

  if len(categories) ==4:
      firstname = cateogries[0].name
      secondname = categories[1].name
      thirdname = categories[2].name
      fourthname = categories[3].name
      longest = max(len(firstname, len(secondname), len(thirdname), len(fourthname)))
      while len(firstname) < longest:
        firstname += " "
      while len(secondname) < longest:
        secondname += " "
      while len(thirdname) < longest:
        thirdname += " "
      while len(fourthname) < longest:
        fourthname += " "
      for x,y,z,w in zip(firstname, secondname, thirdname,fourthname):
        names.append(" " + x + "  " + y + "  " + z + "  " + w + "  ")
        names.append("\n")
  names.pop()
  verticalnames = "".join(names)
  spendingcategories = "Percentage spent by category\n" + plot + dash + "\n" + verticalnames
  return spendingcategories
