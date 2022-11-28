from kivy.config import Config
from kivy.app import App
from kivy.app import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.garden.knob import  Knob
from kivy.uix.recycleview import RecycleView

from kivy.properties import StringProperty

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

import json
import datetime

Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')

# フォント・画像の設定
resource_add_path('./font')
LabelBase.register(DEFAULT_FONT, 'NotoSansJP-Black.otf') 
resource_add_path('./image')
resource_add_path('./json')

class Display(BoxLayout):
    with open('./json/setting.json', 'r') as json_file:
        setting_data = json.load(json_file)
    
    with open('./json/versus.json', 'r') as json_file:
        vs = json.load(json_file)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

 
class Screen_One(Screen):
    pass
 
class Screen_Two(Screen):
    shige_win_num = 0
    hina_win_num = 0
    all_match_num = 0
    shige_text = StringProperty('')
    hina_text = StringProperty('')
    match_text = StringProperty('')
    all_result_text = StringProperty('')
    result1_text_oldest = StringProperty('')
    result2_text = StringProperty('')
    result3_text = StringProperty('')
    result4_text = StringProperty('')
    result5_text_newest = StringProperty('')
    source = StringProperty('saru.png')
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        vs_path = "./json/versus.json"
        with open(vs_path, 'r') as json_file:
            vs = json.load(json_file)
        
        self.all_match_num = len(vs["result"])
        match_type = ['あっち向いてホイ', '指スマ', '大富豪']

        for id, result in enumerate(vs["result"]):

            if result["winner_id"] == 0 :
                self.hina_win_num += 1
                winner_name = 'Player0'
            else:
                self.shige_win_num += 1
                winner_name = 'Player1'
            
            if id == 0 :
                self.result1_text_oldest = f'{result["date"]} \n {match_type[result["match_id"]]}で{winner_name}が勝利！'
            elif id == 1 :
                self.result2_text = f'{result["date"]} \n {match_type[result["match_id"]]}で{winner_name}が勝利！'
            elif id == 2 :
                self.result3_text = f'{result["date"]} \n {match_type[result["match_id"]]}で{winner_name}が勝利！'
            elif id == 3 :
                self.result4_text = f'{result["date"]} \n {match_type[result["match_id"]]}で{winner_name}が勝利！'
            elif id == 4 :
                self.result5_text_newest = f'{result["date"]} \n {match_type[result["match_id"]]}で{winner_name}が勝利！'

        
        self.shige_text = f'[color=#000000]しげの勝利数：[/color][color=#0000FF]{self.shige_win_num}[/color]'
        self.hina_text = f'[color=#000000]ひなこちゃんの勝利数：[/color][color=#FF0000]{self.hina_win_num}[/color]'
        self.match_text = f'[color=#000000]総勝負数：{self.all_match_num}[/color]'
        self.all_result_text = self.match_text + '\n' + self.hina_text + '\n' + self.shige_text

        if self.shige_win_num < self.hina_win_num:
            self.source = 'inu.png'

    def button_clicked(self):
        print(self.ids)
        self.ids.view_label2.text = '私の勝ちだ！！'

class Screen_Three(Screen):
    pass

class VsApp(App):
    def __init__(self, **kwargs):
        super(VsApp, self).__init__(**kwargs)
        self.title = 'Versus'


if __name__ == '__main__':
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    d_week = '日月火水木金土日'  # インデックス0の'日'は使用されない
    idx = now.strftime('%u')  # '%u'では月曜日がインデックス'1'となる
    w = d_week[int(idx)]
    d = now.strftime('%Y年%m月%d日') + f'（{w}）'
    print(d)  # 2021年11月04日（木）

    setting_path = "./json/setting.json"
    VsApp().run()