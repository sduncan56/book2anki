import unittest
from Gloss import Gloss
class TestGloss(unittest.TestCase):
    def test_gloss(self):
        gloss = Gloss()
        result = gloss.fetchGlosses('よく晴れた夜空')
        self.assertEqual(len(result), 3)

    def test_clean_gloss_front(self):
        gloss = Gloss()

        text1 = ' 夜空 【よぞら】 	(n) night sky; (P); ED; Name(s):  【やくう】 (f) Yakuu 【よぞら】 (f) Yozora  SrcHNA '
        clean1 = gloss.clean_front(text1)
        self.assertEqual('夜空 - night sky; (P); ED; Name(s):  【やくう】 (f) Yakuu 【よぞら】 (f) Yozora  SrcHNA', clean1)

        text2 = ' 晴れ : 晴れ(P); 晴; 霽れ 【はれ】 	(n,adj-no) (1) (See 快晴・かいせい) clear weather; fine weather;'
        clean2 = gloss.clean_front(text2)
        self.assertEqual('晴れ - clear weather; fine weather;', clean2)

        text3 = ' 夜空 【よぞら】 	(n) night sky; (P);'
        clean3 = gloss.clean_front(text3)
        self.assertEqual('夜空 - night sky; (P);', clean3)

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

        self.assertEqual('よく - nicely; properly; well; skillfully; skilfully; (2) (uk) frequently; often; (3) (uk) I\'m glad that you ...; thank you for ...', clean)

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