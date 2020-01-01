import unittest
from Gloss import Gloss
class TestGloss(unittest.TestCase):
    def test_gloss(self):
        gloss = Gloss()
        result = gloss.fetchGlosses('よく晴れた夜空')
        self.assertEqual(len(result), 3)

    def test_clean_gloss(self):
        gloss = Gloss()
        result = gloss.fetchGlosses('よく晴れた夜空')
        clean1 = gloss.clean_gloss_front(result[0])
        self.assertEqual('よく - nicely; properly; well; skillfully; skilfully; (2) (uk) frequently; often; (3) (uk) I\'m glad that you ...; thank you for ...; KD', clean1)
        clean2 = gloss.clean_gloss_front(result[1])
        self.assertEqual('晴れ - clear weather; fine weather; (adj-no,n) (2) (ant: 褻) formal; ceremonial; public; (3) cleared of suspicion; (P);  《verb stem》 晴れる : 晴れる(P); 霽れる 【はれる】 ; (v1,vi) (1) to clear up; to clear away; to be sunny; to stop raining; (2) to refresh (e.g. spirits); (3) (See 疑いが晴れる) to be cleared (e.g. of a suspicion); (4) to be dispelled; to be banished; (P); ED', clean2)
        clean3 = gloss.clean_gloss_front(result[2])
        self.assertEqual("夜空 - night sky; (P); ED; Name(s):  【やくう】 (f) Yakuu 【よぞら】 (f) Yozora  SrcHNA", clean3)