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
from bs4 import BeautifulSoup

class NullProvide(object):

    def __init__(self, account_key, string_dates=False):
        soup = BeautifulSoup(urllib2.urlopen('http://www.zerocater.com/menu/%s/' % account_key).read())
        self.meals = []

        for menu in soup.findAll('div', 'menu'):
            def parse_date():
                time_raw = menu.find('div', 'header-time').text.split()
                year, month, day = map(int, menu.attrs['data-date'].split('-'))
                hour, minute = map(int, time_raw[-2].split(':'))
                hour += 12 if time_raw[-1] == 'p.m.' and hour != 12 else 0
                out = datetime.datetime(year, month, day, hour, minute)
                return str(out) if string_dates else out

            self.meals.append({'name': menu.find('div', 'detail-view-header').text.strip(),
                               'restaurant': menu.find('div', 'vendor').text.strip(),
                               'date': parse_date()})


if __name__ == '__main__':
    import sys
    import json
    if len(sys.argv) != 2:
        print 'usage: %s account_key' % sys.argv[0]
        sys.exit(1)
    print json.dumps(NullProvide(sys.argv[1], string_dates=True).meals, indent=4, sort_keys=True)

