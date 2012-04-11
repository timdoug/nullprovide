''' nullprovide
Copyright (c) 2012, timdoug (me@timdoug.com)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the timdoug, Bump Technologies, Inc., nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import urllib2
import datetime
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup

class NullProvide(object):

    __MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
    MONTHS = dict(zip(__MONTHS, range(1, len(__MONTHS)+1)))

    unescape_html = staticmethod(lambda s: HTMLParser.unescape.__func__(HTMLParser, s))

    @classmethod
    def __parse_date(cls, meal, meal_date, string_output):
        # Don't use strptime() here because it depends on locale.
        month_raw, day_raw = meal_date.split()
        month, day = cls.MONTHS[month_raw], int(day_raw)
        raw_time = meal.find('span', 'collapser-controller').text.split(':')
        hour, minute = int(raw_time[0]), int(raw_time[1][0:2])
        hour += 12 if 'p.m.' in raw_time[1] and hour != 12 else 0
        out = datetime.datetime(2012, month, day, hour, minute, 0)
        return str(out) if string_output else out

    @classmethod
    def __parse_restaurant(cls, meal):
        # "...now you have two problems."
        r = meal.p.text
        return cls.unescape_html(r[r.index('from')+4:r.rindex('for')].strip())

    def __init__(self, account_name, string_dates=False):
        soup = BeautifulSoup(urllib2.urlopen('http://www.zerocater.com/' + account_name).read())
        self.meals = []
        for meal_group in soup.findAll('div', 'meal_group new-context'):
            meal_date = meal_group.span.text
            for meal in meal_group.findAll('div', 'meal_item'):
                self.meals.append({'name': self.unescape_html(meal.strong.text),
                                   'date': self.__parse_date(meal, meal_date, string_dates),
                                   'restaurant': self.__parse_restaurant(meal),
                                   'num_people': int(meal.find('span', 'num_people').text.split()[1]),
                                  })


if __name__ == '__main__':
    import sys
    import json
    if len(sys.argv) != 2:
        print 'usage: %s account_name' % sys.argv[0]
        sys.exit(1)
    print json.dumps(NullProvide(sys.argv[1], string_dates=True).meals, indent=4, sort_keys=True)

