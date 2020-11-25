import docker
from datetime import datetime

client = docker.from_env()
containers = client.containers.list()

output = []

for item in containers:
  container = client.containers.get(item.id)
  cname = container.attrs['Name'][1:]
  res = container.exec_run('java ru.CryptoPro.JCP.tools.License', stderr=True, stdout=True)
  if (res[0] == 0):
    validity = res[1].split("\n")
    date = datetime.strptime(validity[6][16:], "%b %d, %Y")
    cur_date = datetime.now()
    if (cur_date < date):
      state = 'Valid'
    else:
      state = 'Expired'
    output.append('{cname}: {date} - {state}'.format(cname=cname, date=date.strftime('%Y-%m-%d'), state=state))

print('\n'.join(output))
