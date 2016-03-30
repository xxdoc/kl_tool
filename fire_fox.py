# -*- coding: utf-8 -*-
from marionette import Marionette

client = Marionette('localhost', port=2828)
client.start_session()

def main():
    url = 'http://25wx.kkyoo.com/dev_wx/wsp/index.php?r=web/livestream&id=3359'
    client.navigate(url)
    input_box = client.find_element('id', 'aodianyun-dms-text')
    input_box

if __name__ == '__main__':
    main()
