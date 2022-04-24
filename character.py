# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re


class CHAR(object):
    def __init__(self):
        self.char_name = ''
        self.HP = 15000  # 生命值
        self.atk = 1600  # 攻击力
        self.DEF = 800  # 防御力
        self.crit_rate = 50.0  # 暴击率
        self.crit_dmg = 100.0  # 暴击伤害
        self.all_dmg = 46.6    # 全伤害加成
        self.bonus_list = {}  # 伤害增益表
        self.skills = {}  # 技能倍率表


    def setCharName(self, char_name):
        """
        set the name of a character
        """
        self.char_name = char_name
        self.skills = {}


    def setAttributes(self, atk=1600.0, crit_rate=50.0, crit_dmg=100.0, HP=15000.0, DEF=800.0, all_dmg=46.6):
        """
        Set the attributes of the character
        """
        self.HP = HP
        self.atk = atk
        self.DEF = DEF
        self.crit_rate = crit_rate
        self.crit_dmg = crit_dmg
        self.all_dmg = all_dmg


    def getSkillList(self):
        """
        Get the skill list and all the skill ratios from the Wiki online.
        return: 
            dict {skill_name: {part_name: [ratios]}}
        """
        if self.skills:
            return self.skills
        url = 'https://wiki.biligame.com/ys/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/55.0.2883.87 Safari/537.36'}
        r = requests.get(url + self.char_name, headers = headers)

        soup = BeautifulSoup(r.text,'html.parser')

        for i, skill_div in enumerate(soup.find_all('div',class_ = 'r-skill-bg')):
            skill_name = skill_div.div.text[2:]
            table = skill_div.find('table')
            skill_ratio = {}
            for j, tr in enumerate(table.find_all('tr')):
                part_ratio = []
                for k, td in enumerate(tr.find_all('td')):
                    if td.text != '' and td.text != "'":
                        part_ratio.append(td.text)
                # 剔除非伤害部分
                if part_ratio and part_ratio[0].find('伤害') > 0:
                    skill_ratio[part_ratio[0]] = part_ratio[1:]
            if skill_ratio:
                self.skills[skill_name] = skill_ratio
        
        return self.skills
        

    def addBonus(self, bonus_type, bonus_ratio):
        """
        add a bonus to the bonus_list.
        para: 
            bonus_type: 'A', 'E' or 'Q'
            bonus_ratio: a float for the ratio
        """
        if bonus_type not in self.bonus_list:
            self.bonus_list[bonus_type] = 0.0
        self.bonus_list[bonus_type] = self.bonus_list[bonus_type] + bonus_ratio
        
        # print(self.bonus_list)


    def computeDamage(self, skill, level, is_crit='E'):
        """
        Conpute the damage of the skill of the level.
        para:
            skill(str): 'A' for normal atk; 'E' for skill E; 'Q' for skill Q.
            level(int): the level of the skill.
            is_crit(str): 'C' for critical damage; 'NC' for not; 'E' and others 
                for expactation of the damage.
        return: 
            a dict showing the damage of every part of the skill.
        """
        A = self.atk
        if is_crit == 'C':
            B = 1.0 + self.crit_dmg / 100.0
        elif is_crit == 'NC':
            B = 1.0
        else:
            B = 1.0 + self.crit_rate * self.crit_dmg / 10000.0
        C = 1.0
        for bonus_type,bonus_value in self.bonus_list.items():
            # print('bonus:',bonus)
            # print(bonus[0].find(skill))
            if bonus_type.find(skill) >= 0:
                C = C + bonus_value / 100.0
        # print('C = ',C)
        # C = C + self.bonus_list[skill] / 100.0
        C = C + self.all_dmg / 100.0
        names = list(self.getSkillList().keys())
        name_of = {}
        name_of['A'] = names[0]
        name_of['E'] = names[1]
        name_of['Q'] = names[2]

        def change_str(s):
            # print(s)
            pattern = re.compile(r'\d+\.\d+%|\d+%')
            L = pattern.findall(s)
            for a in L:
                D = float(a[:-1]) / 100.0
                s = s.replace(a,str(int(A*B*C*D)))
            # print(s)
            return s

        ans = {}
        for name, ratios in self.getSkillList()[name_of[skill]].items():
            D_str = ratios[level - 1]
            ans[name] = change_str(D_str)

        return ans

    
    def display(self,damage_dict:dict):
        """
        transform the damage dictionary to a string for display
        """
        s = ''
        for skill_name, skill_damage in damage_dict.items():
            s = '{0}{1}: {2}\n'.format(s, skill_name, skill_damage)
        return s
    
    def b_display(self):
        """
        return a string containing all bonuses
        """
        s = '伤害加成:\n'
        d_skill = {'A':'普通攻击','E':'元素战技','Q':'元素爆发'}
        for skill_name, skill_damage in self.bonus_list.items():
            s = '{0}{1}: {2}\n'.format(s, d_skill[skill_name], skill_damage)
        return s

if __name__ == '__main__':
    c = CHAR()
    c.setCharName('雷电将军')
    c.setAttributes(2160,78.8,197.2)
    c.addBonus('A', 30) 
    c.addBonus('A', 46.6)
    c.addBonus('Q', 18)
    print(c.display(c.computeDamage('A', 1, 'C')))
    print(c.b_display())
    