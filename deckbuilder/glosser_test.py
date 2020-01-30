import unittest
from deckbuilder.Gloss import Gloss
class TestGloss(unittest.TestCase):
    def test_gloss(self):
        gloss = Gloss()
        result = gloss.fetch_glosses('よく晴れた夜空')
        self.assertEqual(len(result), 3)

    def test_clean_gloss_front(self):
        gloss = Gloss()

        text1 = ' 夜空 【よぞら】 	(n) night sky; (P); ED; Name(s):  【やくう】 (f) Yakuu 【よぞら】 (f) Yozora  SrcHNA '
        clean1 = gloss.clean_front(text1)
        self.assertEqual('夜空 - night sky; (P); ED; Name(s):  【やくう】 (f) Yakuu 【よぞら】 (f) Yozora  SrcHNA', clean1)

        text2 = ' 晴れ : 晴れ(P); 晴; 霽れ 【はれ】 	(n,adj-no) (1) (See 快晴・かいせい) clear weather; fine weather;'
        clean2 = gloss.clean_front(text2)
        self.assertEqual('晴れ - clear weather; fine weather;', clean2)

    def test_clean_front_particle(self):
        gloss = Gloss()
        text = "帝国の from 帝国 【ていこく】 (n) (1) empire; (adj-no) (2) imperial; (P); ED"
        text = gloss.remove_dict_annotations(text)
        text = gloss.clean_front(text)
        text = gloss.clean_verb_stem(text)
        text = gloss.clean_back(text)
        text = gloss.remove_furigana(text)

        self.assertEqual("帝国 - empire;  (2) imperial", text)

    def test_clean_front_particle2(self):
        gloss = Gloss()
        text = "異形の from : 異形; 異型 【いけい】 (n,adj-no) atypical appearance; atypicality; heteromorphy; 【いぎょう】 ; (adj-no,adj-na,n) fantastic; grotesque; strange-looking; suspicious-looking; ED "
        text = gloss.remove_dict_annotations(text)
        text = gloss.clean_front(text)
        text = gloss.clean_verb_stem(text)
        text = gloss.clean_back(text)
        text = gloss.remove_furigana(text)

        self.assertEqual("異形 - atypical appearance; atypicality; heteromorphy;  ;  fantastic; grotesque; strange-looking; suspicious-looking", text)

    def test_clean_front_retain_brace(self):
        gloss = Gloss()
        text = "改ページ : 改ページ; 改頁 【かいページ】 	 {comp} repagination; new page; form feed; page break;"
        text = gloss.remove_dict_annotations(text)
        text = gloss.clean_front(text)
        text = gloss.clean_verb_stem(text)
        text = gloss.clean_back(text)
        text = gloss.remove_furigana(text)

        self.assertEqual("改ページ - {comp} repagination; new page; form feed; page break", text)

    def test_clean_verb_stem_withnumbers(self):
        gloss = Gloss()
        result = gloss.clean_verb_stem('《verb stem》 晴れる : 晴れる(P); 霽れる 【はれる】 ; (v1,vi) (1) to clear up')
        self.assertEqual('(1) to clear up', result)

    def test_clean_verb_stem_withoutnumbers(self):
        gloss = Gloss()
        inputText = '《verb stem》 晴れる : 晴れる(P); 霽れる 【はれる】 ; (v1,vi) to clear up'
        #need to clear junk like '(P)' so we find the actual text start
        inputText = gloss.remove_dict_annotations(inputText)
        result = gloss.clean_verb_stem(inputText)
        self.assertEqual('to clear up', result)

    def test_clean_gloss_back(self):
        gloss = Gloss()

        text1 = ' thank you for ...; KD '
        clean1 = gloss.clean_back(text1)
        self.assertEqual(' thank you for ...', clean1)

        text2 = '(4) to be dispelled; to be banished; (P); ED '
        text2 = gloss.remove_dict_annotations(text2)
        clean2 = gloss.clean_back(text2)
        self.assertEqual('(4) to be dispelled; to be banished', clean2)

        text3 = ' 夜空 【よぞら】 	(n) night sky; (P); ED; Name(s):  【やくう】 (f) Yakuu 【よぞら】 (f) Yozora  SrcHNA '
        text3 = gloss.remove_dict_annotations(text3)
        clean3 = gloss.clean_back(text3)
        self.assertEqual(' 夜空 【よぞら】 	 night sky', clean3)

    def test_cleanall_1(self):
        gloss = Gloss()

        text = ' よく  	(adv) (1) nicely; properly; well; skillfully; skilfully; (2) (uk) frequently; often; (3) (uk) I\'m glad that you ...; thank you for ...; KD '
        clean = gloss.remove_dict_annotations(text)
        clean = gloss.clean_front(clean)
        clean = gloss.clean_verb_stem(clean)
        clean = gloss.clean_back(clean)

        self.assertEqual('よく - nicely; properly; well; skillfully; skilfully; (2)  frequently; often; (3)  I\'m glad that you ...; thank you for ...', clean)

    def test_cleanall_2(self):
        gloss = Gloss()

        text = ' 晴れ : 晴れ(P); 晴; 霽れ 【はれ】 	(n,adj-no) (1) (See 快晴・かいせい) clear weather; fine weather; (adj-no,n) (2) (ant: 褻) formal; ceremonial; public; (3) cleared of suspicion; (P);  《verb stem》 晴れる : 晴れる(P); 霽れる 【はれる】 ; (v1,vi) (1) to clear up; to clear away; to be sunny; to stop raining; (2) to refresh (e.g. spirits); (3) (See 疑いが晴れる) to be cleared (e.g. of a suspicion); (4) to be dispelled; to be banished; (P); ED '
        clean = gloss.remove_dict_annotations(text)
        clean = gloss.clean_front(clean)
        clean = gloss.clean_verb_stem(clean)
        clean = gloss.clean_back(clean)

        self.assertEqual('晴れ - clear weather; fine weather;  (2) (ant: 褻) formal; ceremonial; public; (3) cleared of suspicion;   (1) to clear up; to clear away; to be sunny; to stop raining; (2) to refresh (e.g. spirits); (3) (See 疑いが晴れる) to be cleared (e.g. of a suspicion); (4) to be dispelled; to be banished', clean)

    def test_cleanall_3(self):
        gloss = Gloss()

        text = ' 夜空 【よぞら】 	(n) night sky; (P); ED; Name(s):  【やくう】 (f) Yakuu 【よぞら】 (f) Yozora  SrcHNA '
        clean = gloss.remove_dict_annotations(text)
        clean = gloss.clean_front(clean)
        clean = gloss.clean_verb_stem(clean)
        clean = gloss.clean_back(clean)

        self.assertEqual('夜空 - night sky', clean)

    def test_get_readings(self):
        gloss = Gloss()

        text = "頭 【あたま(P); かしら(P)】 (n) (1) head; (2) hair (on one's head); (3) (あたま only) mind; brains; intellect; (4) leader; chief; boss; captain; (5) top; tip; (6) beginning; start; (7) (あたま only) head; person; (8) (かしら only) top structural component of a kanji; (9) (あたま only) (col) {mahj} (See 雀頭・ジャントー) pair; (P); 【とう】 ; (ctr) counter for large animals (e.g. head of cattle); counter for insects in a collection; counter for helmets, masks, etc.; (P);  : 頭; 首 【こうべ; かぶり(頭); ず(頭); つむり(頭); つむ(頭); つぶり(頭)(ok); かぶ(頭)(ok)】 ; (n) head; : ど頭; 頭 【どたま】 ; (n) (uk) (derog) head; dome; bean; nob; noggin; 【かぶし】 ; (n) (arch) (uk) shape of one's head; 【がしら】 ; (suf) (1) (after a noun) top of ...; head of ...; (2) (after the -masu stem of a verb) the moment that ...;"

        readings = gloss.get_readings(text)
        self.assertEqual(6, len(readings))
        self.assertEqual('頭 【あたま(P); かしら(P)】', readings[0])
        self.assertEqual('【とう】', readings[1])
        self.assertEqual('頭; 首 【こうべ; かぶり(頭); ず(頭); つむり(頭); つむ(頭); つぶり(頭)(ok); かぶ(頭)(ok)】', readings[2])
        self.assertEqual('ど頭; 頭 【どたま】', readings[3])
        self.assertEqual('【かぶし】', readings[4])
        self.assertEqual('【がしら】', readings[5])

    def test_generate_alt_readings(self):
        gloss = Gloss()
        text = "頭 【あたま(P); かしら(P)】 (n) (1) head; (2) hair (on one's head); (3) (あたま only) mind; brains; intellect; (4) leader; chief; boss; captain; (5) top; tip; (6) beginning; start; (7) (あたま only) head; person; (8) (かしら only) top structural component of a kanji; (9) (あたま only) (col) {mahj} (See 雀頭・ジャントー) pair; (P); 【とう】 ; (ctr) counter for large animals (e.g. head of cattle); counter for insects in a collection; counter for helmets, masks, etc.; (P);  : 頭; 首 【こうべ; かぶり(頭); ず(頭); つむり(頭); つむ(頭); つぶり(頭)(ok); かぶ(頭)(ok)】 ; (n) head; : ど頭; 頭 【どたま】 ; (n) (uk) (derog) head; dome; bean; nob; noggin; 【かぶし】 ; (n) (arch) (uk) shape of one's head; 【がしら】 ; (suf) (1) (after a noun) top of ...; head of ...; (2) (after the -masu stem of a verb) the moment that ...;"

        text = gloss.remove_dict_annotations(text)
        readings = gloss.get_readings(text)
        altreadings = gloss.generate_alt_readings(readings)

        self.assertEqual('頭 【あたま かしら】 | 【とう】 | 頭; 首 【こうべ; かぶり(頭); ず(頭); つむり(頭); つむ(頭); つぶり(頭)(ok); かぶ(頭)(ok)】 | ど頭; 頭 【どたま】 | 【かぶし】 | 【がしら】</br>', altreadings)

    def test_generate_alt_readings_withparticle(self):
        gloss = Gloss()

        text = '帝国の from 帝国 【ていこく】 (n) (1) empire; (adj-no) (2) imperial; (P); ED'
        text = gloss.remove_dict_annotations(text)
        readings = gloss.get_readings(text)
        altreadings = gloss.generate_alt_readings(readings)
        self.assertEqual('帝国 【ていこく】</br>', altreadings)

    def test_generate_alt_readings_noreading(self):
        gloss = Gloss()

        text = "ここから (exp) from here; KD"
        readings = gloss.get_readings(text)
        altreadings = gloss.generate_alt_readings(readings)
        self.assertEqual(0, len(altreadings))

    @unittest.skip("this would look nicer but I don't actually care")
    def test_get_readings_cleaned(self):
        gloss = Gloss()

        text = gloss.remove_dict_annotations("頭 【あたま(P); かしら(P)】 (n) (1) head;")

        readings = gloss.get_readings(text)
        self.assertEqual('頭 【あたま; かしら】', readings[0])

    def test_remove_furigana(self):
        gloss = Gloss()

        text = "頭 【あたま(P); かしら(P)】 (n) (1) head; (2) hair (on one's head); (3) (あたま only) mind; brains; intellect; (4) leader; chief; boss; captain; (5) top; tip; (6) beginning; start; (7) (あたま only) head; person; (8) (かしら only) top structural component of a kanji; (9) (あたま only) (col) {mahj} (See 雀頭・ジャントー) pair; (P); 【とう】 ; (ctr) counter for large animals (e.g. head of cattle); counter for insects in a collection; counter for helmets, masks, etc.; (P);  : 頭; 首 【こうべ; かぶり(頭); ず(頭); つむり(頭); つむ(頭); つぶり(頭)(ok); かぶ(頭)(ok)】 ; (n) head; : ど頭; 頭 【どたま】 ; (n) (uk) (derog) head; dome; bean; nob; noggin; 【かぶし】 ; (n) (arch) (uk) shape of one's head; 【がしら】 ; (suf) (1) (after a noun) top of ...; head of ...; (2) (after the -masu stem of a verb) the moment that ...;"

        clean = gloss.remove_furigana(text)
        self.assertEqual("頭  (n) (1) head; (2) hair (on one's head); (3) (あたま only) mind; brains; intellect; (4) leader; chief; boss; captain; (5) top; tip; (6) beginning; start; (7) (あたま only) head; person; (8) (かしら only) top structural component of a kanji; (9) (あたま only) (col) {mahj} (See 雀頭・ジャントー) pair; (P);  ; (ctr) counter for large animals (e.g. head of cattle); counter for insects in a collection; counter for helmets, masks, etc.; (P);  : 頭; 首  ; (n) head; : ど頭; 頭  ; (n) (uk) (derog) head; dome; bean; nob; noggin;  ; (n) (arch) (uk) shape of one's head;  ; (suf) (1) (after a noun) top of ...; head of ...; (2) (after the -masu stem of a verb) the moment that ...;", clean)

    def test_clean_front_no_tabs(self):
        gloss = Gloss()
        text = '衛星 【えいせい】 (n) (1) {astron} (natural) satellite; moon; (2) (See 人工衛星) (artificial) satellite; (P); ED Name(s): 【えいせい】 (u) Eisei '

        clean = self.clean_all(gloss, text)

        self.assertEqual('衛星 - {astron} (natural) satellite; moon; (2) (See 人工衛星) (artificial) satellite', clean)

    def clean_all(self, gloss, text):
        clean = gloss.remove_dict_annotations(text)
        clean = gloss.clean_front(clean)
        clean = gloss.clean_verb_stem(clean)
        clean = gloss.clean_back(clean)
        clean = gloss.remove_furigana(clean)
        return clean

    def test_leading_text(self):
        gloss = Gloss()

        text = " Possible inflected verb or adjective: (passive)<br>描く : 描く(P); 画く 【えがく(P); かく】 	(v5k,vt) (1) (See 書く・2) to draw; to paint; to sketch; (2) (えがく only) to depict; to describe; (3) to picture in one's mind; to imagine; (4) to form a certain shape (e.g. path of an action, appearance of an object, etc.); (P); ED "

        clean = self.clean_all(gloss, text)
        self.assertEqual("描く - to draw; to paint; to sketch; (2) (えがく only) to depict; to describe; (3) to picture in one's mind; to imagine; (4) to form a certain shape (e.g. path of an action, appearance of an object, etc.)", clean)

    def test_should_ignore_gloss(self):
        gloss = Gloss()
        gloss.ignore_set.add("生活")
        text = "生活 【せいかつ】 (n,vs) living; life (one's daily existence); livelihood; (P); ED "
        shouldIgnore = gloss.is_known_word(text)
        self.assertTrue(shouldIgnore)

    def test_populate_ignore_set_jlpt(self):
        gloss = Gloss()
        frequency = [{'word': 'tst', 'jlpt': 'N2', 'frequency': 1},
                     {'word': 'tst2', 'jlpt': 'N4', 'frequency': 1}]
        gloss.populate_ignore_set(frequency, 3, 100)
        self.assertEqual('tst', gloss.ignore_set.pop())
        self.assertEqual(len(gloss.ignore_set), 0)
