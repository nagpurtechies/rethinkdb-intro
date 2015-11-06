from faker import Factory
import rethinkdb as r
import pytz
import time

conn = r.connect(host='localhost',
                 port=28015,
                 db='chatrethink')

conn.repl()

faker = Factory.create()

messages = []

start = time.time()

for x in range(10000):
    username = faker.first_name().lower()
    text = faker.sentence()
    # RethinkDB requires datetime objects to have tzinfo
    added = pytz.utc.localize(faker.date_time_this_century())
    messages.append({'by': username,
                     'text': text,
                     'added': added})

r.table('messages').insert(messages).run()

end = time.time()
print(end-start)
print("{} inserts per second".format(100000/(end-start)))
