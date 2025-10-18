import tempfile
import os

from unittest import TestCase
from unittest.mock import patch


PRIMARY_TEST_DATA = """Academic Year,Roll Number,Official School Name,Address 1,Address 2,Address 3,Address 4,Eircode,School Latitude,School Longitude,School Planning area,County,Local Authority,Principal Name,Email,Phone,Ethos/Religion,Post Primary School Type,Irish Classification - Post Primary,School Gender - Post Primary,Pupil Attendance Type,Fee Paying School (Y/N),Island Location (Y/N),Gaeltacht Area Location (Y/N),DEIS (Y/N),FEMALE,MALE,Total 2024-2025
2024.0,60010P,Loreto Secondary School,Brick Lane,Balbriggan,Co Dublin,,K32R248,53.612259,-6.185114,Balbriggan,Dublin,Fingal County Council,MS. ANN M MCDONOUGH,office@loretobalbriggan.ie,018411594,CATHOLIC,Secondary,No subjects taught through Irish,Girls,Day,N,N,N,N,1232.0,,1232
2024.0,60021U,St Marys Secondary School,Main Street,Baldoyle,Dublin 13,,D13W208,53.396912,-6.127654,Donaghmede_Howth_D13,Dublin,Fingal County Council,MS. EDEL GREENE,info@stmarysbaldoyle.org,018325591,CATHOLIC,Secondary,No subjects taught through Irish,Mixed,Day,N,N,N,N,232.0,10.0,242
2024.0,60030V,Blackrock College,Blackrock College,Rock Road,Co. Dublin,,A94FK84,53.303651,-6.190339,Booterstown_Blackrock,Dublin,Dun Laoghaire Rathdown,MS. YVONNE MARKEY,ymarkey@blackrockcollege.com,012752100,CATHOLIC,Secondary,No subjects taught through Irish,Boys,Mixed,Y,N,N,N,,1053.0,1053
2024.0,60040B,Willow Park School,Rock Road,Blackrock,Co Dublin,,A94TW98,53.306045,-6.195357,Booterstown_Blackrock,Dublin,Dun Laoghaire Rathdown,MR. ALAN JAMES THOMAS ROGAN,arogan@willowparkschool.ie,012881651,CATHOLIC,Secondary,No subjects taught through Irish,Boys,Mixed,Y,N,N,N,,208.0,208
2024.0,60041D,Coláiste Eoin,Baile an Bhóthair,Bóthair Stigh Lorgan,Co. Átha Cliath,,A94E122,53.302626,-6.204946,Booterstown_Blackrock,Dublin,Dun Laoghaire Rathdown,MR. P.S DE POIRE,ce@eoiniosagain.ie,012884002,CATHOLIC,Secondary,All pupils taught all subjects through Irish,Boys,Day,N,N,N,N,,510.0,510
2024.0,60042F,Coláiste Íosagáin,Bóthar Stigh Lorgan,Baile an Bhóthair,An Charraig Dhubh,Co Átha Cliath,A94KV12,53.3024,-6.204077,Booterstown_Blackrock,Dublin,Dun Laoghaire Rathdown,MR. SEAN DELAP,eolas@eoiniosagain.ie,012884028,CATHOLIC,Secondary,All pupils taught all subjects through Irish,Girls,Day,N,N,N,N,488.0,,488
2024.0,60050E,Oatlands College,Mount Merrion,Co Dublin,,,A94HX38,53.292484,-6.202492,Dunlaoghaire,Dublin,Dun Laoghaire Rathdown,MS. CAROLINE GARRETT,cgarrett@oatlands.net,012888533,CATHOLIC,Secondary,No subjects taught through Irish,Boys,Day,N,N,N,N,,634.0,634
2024.0,60070K,Dominican College,Dominican College Sion Hill,Cross Avenue,Blackrock,Co Dublin,A94TP97,53.301595,-6.189684,Booterstown_Blackrock,Dublin,Dun Laoghaire Rathdown,MS. ORLA CONDREN,admin@sionhillcollege.ie,012886791,CATHOLIC,Secondary,No subjects taught through Irish,Girls,Day,N,N,N,N,508.0,,508
2024.0,60081P,Rockford Manor Secondary School,Stradbrook Rd,Blackrock,Co Dublin,,A94H294,53.287059,-6.163012,Dunlaoghaire,Dublin,Dun Laoghaire Rathdown,MS. MARY GALLAGHER,info@rockfordmanor.ie,01 2801522,CATHOLIC,Secondary,No subjects taught through Irish,Girls,Day,N,N,N,N,285.0,,285"""

SECONDARY_TEST_DATA = """Total Enrolment in Mainstream National Schools for the 2024/2025 school year (enrolment is as of 30th September 2024),Unnamed: 1,Unnamed: 2,Unnamed: 3,Unnamed: 4,Unnamed: 5,Unnamed: 6,Unnamed: 7,Unnamed: 8,Unnamed: 9,Unnamed: 10,Unnamed: 11,Unnamed: 12,Unnamed: 13,Unnamed: 14,Unnamed: 15,Unnamed: 16,Unnamed: 17,Unnamed: 18,Unnamed: 19,Unnamed: 20,Unnamed: 21,Unnamed: 22,Unnamed: 23,Unnamed: 24,Unnamed: 25
Academic Year (Enrolment),Roll Number,Official Name,Address (Line 1),Address (Line 2),Address (Line 3),Address (Line 4),County Description,Eircode,School Latitude,School Longitude,School Planning Area,Email,Phone No.,Principal Name,Local Authority Description,School Type,School Level,DEIS (Y/N),Irish Classification Description,Gaeltacht Indicator (Y/N),Island (Y/N),Ethos Description,Female,Male,Enrolment per Return
2024,00359V,ST. LOUIS GIRLS NATIONAL SCHOOL,Park Road,Monaghan,,,Monaghan,H18HK31,54.245607,-6.976626,Monaghan,principal@stlouisgns.com,04781305,Marietta Graham Reynolds (acting),Monaghan County Council,Ordinary,Senior,Y,No subjects through Irish,N,N,Catholic,201,,201
2024,00373P,DERAVOY NATIONAL SCHOOL,Deravoy,Emyvale,Co. Monaghan,,Monaghan,H18PY11,54.356397,-7.024314,Monaghan,deravoyns@gmail.com,04787755,Sheenagh Currie,Monaghan County Council,Ordinary,All Through,Y,No subjects through Irish,N,N,Catholic,32,43,75
2024,00467B,BALLINSPITTLE N S,Ballycatten,Ballinspittle,Co. Cork,,Cork,P17FN27,51.664166,-8.596099,Kinsale,secretary@ballinspittlens.ie,0214778239,Mrs. Sheila Wall,Cork County Council,Ordinary,All Through,N,No subjects through Irish,N,N,Catholic,90,94,184
2024,00512D,MIDLETON CONVENT N S,Midleton,Co. Cork,,,Cork,P25R248,51.908214,-8.164152,Midleton_Carrigtwohill,scoilbhridemidleton@gmail.com,0214631593,Seamus O'Connor,Cork County Council,Ordinary with Special Classes,All Through,N,No subjects through Irish,N,N,Catholic,241,47,288
2024,00538V,CLOCHAR DAINGEAN,An Phríomhsráid Uachtarach,Daingean Uí Chúis,Co. Chiarraí,,Kerry,V92AD76,52.142211,-10.270384,Dingle,bscd01@gmail.com,0669151154,Micheál Ó Muircheartaigh,Kerry County Council,Ordinary,All Through,N,All subjects through Irish,Y,N,Catholic,110,28,138
2024,00606M,MONARD N S,Monard,Solohead,Co. Tipperary,,Tipperary,E34VF97,52.510934,-8.224356,Tipperary,info@monardns.com,06247557,Mary O'Dwyer,Tipperary (Sr) County Council,Ordinary,All Through,N,No subjects through Irish,N,N,Catholic,56,52,108
2024,00651R,BORRIS MXD N S,Lower Main Street,Borris,Co. Carlow,,Carlow,R95RH6F,52.599655,-6.920434,Borris,pcoady@borrisns.com,0599773402,Pat Coady,Carlow County Council,Ordinary,All Through,N,No subjects through Irish,N,N,Catholic,94,104,198
2024,00697S,ST BRIGIDS MXD N S,Beechpark Lawn,Castleknock,Dublin 15,,Dublin,D15P820,53.375089,-6.362184,Castleknock_D15,principal@saintbrigids.ie,018214040,Nicola Fay,Fingal County Council,Ordinary with Special Classes,All Through,N,No subjects through Irish,N,N,Catholic,410,468,878"""


class SchoolsTest(TestCase):
    def setUp(self):
        self.primary_temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=".csv", mode="w", encoding="utf-8"
        )
        self.primary_temp_file.write(PRIMARY_TEST_DATA)
        self.primary_temp_file_path = self.primary_temp_file.name
        self.primary_temp_file.close()

        self.secondary_temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=".csv", mode="w", encoding="utf-8"
        )
        self.secondary_temp_file.write(SECONDARY_TEST_DATA)
        self.secondary_temp_file_path = self.secondary_temp_file.name
        self.secondary_temp_file.close()

    def tearDown(self):
        for fp in [self.primary_temp_file_path, self.secondary_temp_file_path]:
            if os.path.exists(fp):
                os.remove(fp)

    def test_get_near(self):
        with (
            patch(
                "irish_property_analysis.settings.PRIMARY_SCHOOLS_DATA_LOCATION",
                self.primary_temp_file_path,
            ),
            patch(
                "irish_property_analysis.settings.SECONDARY_SCHOOLS_DATA_LOCATION",
                self.secondary_temp_file_path,
            ),
        ):
            from irish_property_analysis.schools import schools

            self.assertEqual(len(schools.get_near(0, 0, radius_km=99999)), 17)

            self.assertEqual(
                len(schools.get_near(53.612259, -6.185114, radius_km=0.01)), 1
            )

    def test_get_score(self):
        with (
            patch(
                "irish_property_analysis.settings.PRIMARY_SCHOOLS_DATA_LOCATION",
                self.primary_temp_file_path,
            ),
            patch(
                "irish_property_analysis.settings.SECONDARY_SCHOOLS_DATA_LOCATION",
                self.secondary_temp_file_path,
            ),
        ):
            from irish_property_analysis.schools import schools

            self.assertEqual(
                schools.get_score(0, 0, radius_km=99999),
                17,
            )

            self.assertEqual(
                schools.get_score(53.612259, -6.185114, radius_km=0.01),
                1,
            )
