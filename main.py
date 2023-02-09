from kivy.config import Config
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.app import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.garden.knob import  Knob
from kivy.uix.recycleview import RecycleView

from kivy.properties import StringProperty
from kivy.properties import ObjectProperty

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

class Setting:
    pl0_name = ''
    pl1_name = ''
    pl0_desc = ''
    pl1_desc = ''
    pl0_win_num = 0
    pl1_win_num = 0
    all_match_num = 0
    match0 = ''
    match1 = ''
    match2 = ''

    def __init__(self):
        with open('./json/setting.json', 'r') as json_file:
            setting_data = json.load(json_file)
        self.pl0_name = setting_data['user'][0]["0"]
        self.pl1_name = setting_data['user'][0]["1"]
        self.match0 = setting_data['match_type'][0]["0"]
        self.match1 = setting_data['match_type'][0]["1"]
        self.match2 = setting_data['match_type'][0]["2"]
        self.all_match_num = setting_data['match_result'][0]["all"]
        self.pl0_win_num = setting_data['match_result'][0]["pl0"]
        self.pl1_win_num = setting_data['match_result'][0]["pl1"]
        self.pl0_desc = setting_data['description'][0]["0"]
        self.pl1_desc = setting_data['description'][0]["1"]

        with open('./json/versus.json', 'r') as json_file:
            vs = json.load(json_file)

class Display(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Screen_One(Screen, Setting):
    pass

class PopupMenu(BoxLayout, Setting):
    popup_close = ObjectProperty(None)
    pl0_name = Setting.pl0_name
    pl1_name = Setting.pl1_name
    match0 = Setting.match0
    match1 = Setting.match1
    match2 = Setting.match2
    all_match_num = Setting.all_match_num
    pl0_win_num = Setting.pl0_win_num
    pl1_win_num = Setting.pl1_win_num


    def add_result(self):
        # 日付取得
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)
        d_week = '日月火水木金土日'  # インデックス0の'日'は使用されない
        idx = now.strftime('%u')  # '%u'では月曜日がインデックス'1'となる
        w = d_week[int(idx)]
        d = now.strftime('%Y年%m月%d日') + f'（{w}）'

        # 勝負に関するデータ取得
        self.all_match_num += 1
        if self.ids.match0.active == True :
            match_id = 0
        elif self.ids.match1.active == True :
            match_id = 1
        elif self.ids.match2.active == True :
            match_id = 2

        if self.ids.pl0.active == True :
            winner_id = 0
            self.pl0_win_num += 1
        elif self.ids.pl1.active == True :
            winner_id = 1
            self.pl1_win_num += 1

        # versus_jsonに保存
        add_vs = {"date":d , "match_id":match_id, "winner_id":winner_id}
        with open("./json/versus.json", 'r') as json_file:
            vs_data = json.load(json_file)
        vs_data["result"].append(add_vs)
        save_vs = {"result":vs_data["result"][-5:]}
        with open('./json/versus.json', 'w') as f:
            json.dump(save_vs, f)

        # setting_jsonに保存
        with open('./json/setting.json', 'r') as json_file:
            setting_data = json.load(json_file)
        setting_data['match_result'][0]["all"] = self.all_match_num
        setting_data['match_result'][0]["pl0"] = self.pl0_win_num
        setting_data['match_result'][0]["pl1"] = self.pl1_win_num
        save_setting = {"match_type":setting_data['match_type'], "user":setting_data['user'], "match_result":setting_data['match_result']}
        with open('./json/setting.json', 'w') as f:
            json.dump(save_setting, f)

class Screen_Two(Screen, Setting):
    pl0_text = StringProperty('')
    pl1_text = StringProperty('')
    match_text = StringProperty('')
    all_result_text = StringProperty('')
    result1_text_oldest = StringProperty('')
    result2_text = StringProperty('')
    result3_text = StringProperty('')
    result4_text = StringProperty('')
    result5_text_newest = StringProperty('')
    winner1_img = StringProperty('')
    winner2_img = StringProperty('')
    winner3_img = StringProperty('')
    winner4_img = StringProperty('')
    winner5_img = StringProperty('')
    winner1_color = ()
    winner2_color = ()
    winner3_color = ()
    winner4_color = ()
    winner5_color = StringProperty('')


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        vs_path = "./json/versus.json"
        with open(vs_path, 'r') as json_file:
            vs = json.load(json_file)
        
        match_type = [self.match0, self.match1, self.match2]

        for id, result in enumerate(vs["result"]):

            if id == 0 :
                if result["winner_id"] == 0 :
                    winner_name = self.pl0_name
                    self.winner1_img = 'pl0_blue.jpg'
                else:
                    winner_name = self.pl1_name
                    self.winner1_img = 'pl1_red.jpg'
                self.result1_text_oldest = f'{result["date"]} \n {match_type[result["match_id"]]}で{winner_name}が勝利！'
            elif id == 1 :
                if result["winner_id"] == 0 :
                    winner_name = self.pl0_name
                    self.winner2_img = 'pl0_blue.jpg'
                else:
                    winner_name = self.pl1_name
                    self.winner2_img = 'pl1_red.jpg'
                self.result2_text = f'{result["date"]} \n {match_type[result["match_id"]]}で{winner_name}が勝利！'
            elif id == 2 :
                if result["winner_id"] == 0 :
                    winner_name = self.pl0_name
                    self.winner3_img = 'pl0_blue.jpg'
                else:
                    winner_name = self.pl1_name
                    self.winner3_img = 'pl1_red.jpg'
                self.result3_text = f'{result["date"]} \n {match_type[result["match_id"]]}で{winner_name}が勝利！'
            elif id == 3 :
                if result["winner_id"] == 0 :
                    winner_name = self.pl0_name
                    self.winner4_img = 'pl0_blue.jpg'
                else:
                    winner_name = self.pl1_name
                    self.winner4_img = 'pl1_red.jpg'
                self.result4_text = f'{result["date"]} \n {match_type[result["match_id"]]}で{winner_name}が勝利！'
            elif id == 4 :
                if result["winner_id"] == 0 :
                    winner_name = self.pl0_name
                    self.winner5_img = 'pl0_blue.jpg'
                else:
                    winner_name = self.pl1_name
                    self.winner5_img = 'pl1_red.jpg'
                self.result5_text_newest = f'{result["date"]} \n {match_type[result["match_id"]]}で{winner_name}が勝利！'

        
        self.pl0_text = f'[color=#000000]{self.pl0_name}の勝利数：[/color][color=#0000FF]{self.pl0_win_num}[/color]'
        self.pl1_text = f'[color=#000000]{self.pl1_name}の勝利数：[/color][color=#FF0000]{self.pl1_win_num}[/color]'
        self.match_text = f'[color=#000000]総勝負数：{self.all_match_num}[/color]'
        self.all_result_text = self.match_text + '\n' + self.pl0_text + '\n' + self.pl1_text


    def popup_open(self):
        content = PopupMenu(popup_close=self.popup_close)
        self.popup = Popup(title='成績の追加', content=content, size_hint=(0.9, 0.5), auto_dismiss=True)
        self.popup.open()


    def popup_close(self):
        self.popup.dismiss()

class Screen_Three(Screen, Setting):
    cl_input = None
    vs_input = None


    def ch_pl_name(self):
        with open('./json/setting.json', 'r') as json_file:
            setting_data = json.load(json_file)
        pl_input = self.ids.pl_inp.text

        #名前未入力、変更対象プレイヤー未選択の処理
        if (self.ids.pl0_name.active==False) and (self.ids.pl1_name.active==False):
            print("変更対象のプレイヤーの選択なし")
            self.ids.pl_inp.text = "変更対象のプレイヤーを選択してください"

        elif (pl_input == "") or (pl_input == "変更対象のプレイヤーを選択してください") or (pl_input == "名前を入力してください") or (pl_input == "変更が完了しました!"):
            print("値なし")
            self.ids.pl_inp.text = "名前を入力してください"

        else :
            if self.ids.pl0_name.active == True :
                print(setting_data['user'][0]["0"])
                setting_data['user'][0]["0"] = pl_input
            elif self.ids.pl1_name.active == True :
                setting_data['user'][0]["1"] = pl_input

            save_setting = {"user":setting_data['user'], "description":setting_data['description'], "match_type":setting_data['match_type'], "match_result":setting_data['match_result']}
            with open('./json/setting.json', 'w') as f:
                json.dump(save_setting, f)
            self.ids.pl_inp.text = "変更が完了しました!"


    def add_description(self):
        with open('./json/setting.json', 'r') as json_file:
            setting_data = json.load(json_file)
        desc_input = self.ids.desc_inp.text

        #紹介文未入力、変更対象プレイヤー未選択の処理
        if (self.ids.pl0_desc.active==False) and (self.ids.pl1_desc.active==False):
            print("変更対象のプレイヤーの選択なし")
            self.ids.desc_inp.text = "変更対象のプレイヤーを選択してください"

        elif (desc_input == "") or (desc_input == "変更対象のプレイヤーを選択してください") or (desc_input == "紹介文を入力してください") or (desc_input == "変更が完了しました!"):
            print("値なし")
            self.ids.desc_inp.text = "紹介文を入力してください"

        else :
            if self.ids.pl0_desc.active == True :
                setting_data['description'][0]["0"] = desc_input
            elif self.ids.pl1_desc.active == True :
                setting_data['description'][0]["1"] = desc_input

            save_setting = {"user":setting_data['user'], "description":setting_data['description'], "match_type":setting_data['match_type'], "match_result":setting_data['match_result']}
            with open('./json/setting.json', 'w') as f:
                json.dump(save_setting, f)
            self.ids.desc_inp.text = "変更が完了しました!"


    def change_vs_type(self):
        with open('./json/setting.json', 'r') as json_file:
            setting_data = json.load(json_file)
        vs_input = self.ids.vs_inp.text

        #紹介文未入力、変更対象プレイヤー未選択の処理
        if (self.ids.vs0.active==False) and (self.ids.vs1.active==False) and (self.ids.vs2.active==False):
            print("変更対象の勝負の選択なし")
            self.ids.vs_inp.text = "変更対象の勝負を選択してください"

        elif (vs_input == "") or (vs_input == "変更対象の勝負を選択してください") or (vs_input == "追加する勝負名を入力してください") or (vs_input == "変更が完了しました!") :
            print("値なし")
            self.ids.vs_inp.text = "追加する勝負名を入力してください"

        else :
            if self.ids.vs0.active == True :
                setting_data['match_type'][0]["0"] = vs_input
            elif self.ids.vs1.active == True :
                setting_data['match_type'][0]["1"] = vs_input
            elif self.ids.vs2.active == True :
                setting_data['match_type'][0]["2"] = vs_input

            save_setting = {"user":setting_data['user'], "description":setting_data['description'], "match_type":setting_data['match_type'], "match_result":setting_data['match_result']}
            with open('./json/setting.json', 'w') as f:
                json.dump(save_setting, f)
            self.ids.vs_inp.text = "変更が完了しました!"

class VsApp(App):
    def __init__(self, **kwargs):
        super(VsApp, self).__init__(**kwargs)
        self.title = 'Versus'


if __name__ == '__main__':
    VsApp().run()