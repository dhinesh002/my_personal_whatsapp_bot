import pyautogui as pa
from time import sleep
import pyperclip as pc
import requests
import random
import psutil
from nsetools import Nse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os


QUOTE_KEY = 'quote'
STOP_KEY = 'bye'
SHUTDOWN_KEY = 'shutdown'


CHECK_NEW_MESSAGE_IN_SEC = 600


def convert(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)


battery = psutil.sensors_battery()
nse = Nse()

FOREX_CURRENCIES = ['EUR/USD', 'USD/JPY', 'GBP/USD', 'USD/TRY', 'USD/CHF', 'USD/CAD', 'EUR/JPY', 'AUD/USD', 'NZD/USD',
                    'EUR/GBP', 'EUR/CHF', 'AUD/JPY', 'GBP/JPY', 'CHF/JPY', 'EUR/CAD', 'AUD/CAD', 'CAD/JPY', 'NZD/JPY',
                    'AUD/NZD', 'GBP/AUD', 'EUR/AUD', 'GBP/CHF', 'EUR/NZD', 'AUD/CHF', 'GBP/NZD', 'USD/INR', 'USD/CNY',
                    'USD/SGD', 'USD/HKD', 'USD/DKK', 'GBP/CAD', 'USD/SEK', 'USD/RUB', 'USD/MXN', 'USD/ZAR', 'CAD/CHF',
                    'NZD/CAD', 'NZD/CHF', 'BTC/USD', 'BTC/EUR', 'ETH/USD']

STOCK_CODES = ['IIFLWAM', 'RHFL', 'RAJMET', 'ICICIBANK', 'MAITHANALL', 'IOC', 'SATIA', 'WOCKPHARMA', 'TIRUMALCHM',
               'SGL', 'CROWN', 'CGPOWER', 'INFOBEAN', 'SOMATEX', 'FOCUS', 'FLEXITUFF', 'JKPAPER', 'ARVINDFASN',
               'INDIANHUME', 'DIL', 'RADAAN', 'PILANIINVS', 'OIL', 'MANAPPURAM', 'MENONBE', 'SPAL', 'SURANAT&P', 'TWL',
               'APOLLO', 'ALBERTDAVD', 'BLBLIMITED', 'HINDMOTORS', 'ALOKINDS', 'KEI', 'WORTH', 'ELECTHERM', 'HBSL',
               'ARIES', 'TARSONS', 'CINELINE', 'DCMSRIND', 'STEELXIND', 'NESTLEIND', 'HDFCBANK', '5PAISA', 'BORORENEW',
               'HAVISHA', 'TIIL', 'VIKASLIFE', 'NHPC', 'HLEGLAS', 'BBOX', 'BANG', 'V2RETAIL', 'SCHAND', 'SPENCERS',
               'JUBLINDS', 'GUFICBIO', 'JUBLFOOD', 'ZYDUSWELL', 'AUBANK', 'REMSONSIND', 'EMAMILTD', 'RANASUG',
               'EDUCOMP', 'POWERGRID', 'GULPOLY', 'ROLEXRINGS', 'VISHAL', 'VERANDA', 'CENTUM', 'EUROTEXIND',
               'MIRCELECTR', 'MRPL', 'NRBBEARING', 'NGIL', 'SUVIDHAA', 'TVTODAY', 'AIRAN', 'TANLA', 'FIBERWEB', 'IMFA',
               'ADROITINFO', 'MANYAVAR', 'AAKASH', 'ULTRACEMCO', 'BDL', 'UNIDT', 'UPL', 'CANTABIL', 'SJS', 'ELGIEQUIP',
               'INCREDIBLE', 'ORIENTABRA', 'SHARDACROP', 'VAKRANGEE', 'LINCOLN', 'PLASTIBLEN', 'PHOENIXLTD', 'ESCORTS',
               'ZENTEC', 'ARIHANTCAP', 'VALIANTORG', 'ASAL', 'HINDPETRO', 'TIMESGTY', 'MMFL', 'PASUPTAC', 'ZYDUSLIFE',
               'SPICEJET', 'NDRAUTO', 'GINNIFILA', 'NDTV', 'TTKHLTCARE', 'QUICKHEAL', 'SYMPHONY', 'WHEELS', 'PALREDTEC',
               'FINEORG', 'DFMFOODS', 'WENDT', 'BKMINDST', 'ALPA', 'SHANTI', 'SITINET', 'KANORICHEM', 'MANORG',
               'BALKRISIND', 'PANACEABIO', 'SHRIRAMPPS', 'DIAMONDYD', 'STERTOOLS', 'VSTTILLERS', 'NILAINFRA', 'AWL',
               'ALLCARGO', 'VIVIMEDLAB', 'DANGEE', 'DICIND', 'THERMAX', 'GLOBE', 'GALAXYSURF', 'ACE', 'REGENCERAM',
               'UNIONBANK', 'SCAPDVR', 'TEGA', 'GLENMARK', 'TANTIACONS', 'WELINV', 'ADL', 'BFINVEST', 'M&MFIN',
               'SANWARIA', 'HITECHCORP', 'PRECWIRE', 'JAMNAAUTO', 'BAFNAPH', 'JSWENERGY', 'INDIANCARD', 'MAHLIFE',
               'LUPIN', 'VASCONEQ', 'PILITA', 'MTEDUCARE', 'MARSHALL', 'NILKAMAL', 'BAYERCROP', 'COCHINSHIP', 'GICRE',
               'GAEL', 'DENORA', 'AJRINFRA', 'HCG', 'RBA', 'INFOMEDIA', 'SIYSIL', 'DEEPENR', 'MOIL', 'PANSARI', 'RITES',
               'TRIL', 'ZEELEARN', 'INDOBORAX', 'KHADIM', 'ZFCVINDIA', 'WEALTH', 'APCOTEXIND', 'GRAUWEIL', 'ICRA',
               'CLSEL', 'FCONSUMER', 'INDRAMEDCO', 'RADIOCITY', 'EXCELINDUS', 'FAIRCHEMOR', 'APOLLOTYRE', 'BAJAJCON',
               'GENCON', 'ARROWGREEN', 'SUPREMEIND', 'PRINCEPIPE', 'FUSION', 'KAUSHALYA', 'GOODYEAR', 'PFIZER', 'DEN',
               'HEIDELBERG', 'SUNDRMBRAK', 'PIXTRANS', 'SILGO', 'SHREYANIND', 'AEGISCHEM', 'SHIVATEX', 'ARSHIYA',
               'SILINV', 'SKMEGGPROD', 'VAIBHAVGBL', 'GODREJAGRO', 'POLYMED', 'MHLXMIRU', 'UNIINFO', 'DBL', 'EQUIPPP',
               'HESTERBIO', 'GROBTEA', 'ETHOSLTD', 'JSWHL', 'SELMC', 'NAGAFERT', 'BHAGERIA', 'MAHSCOOTER', 'EVERESTIND',
               'SUBCAPCITY', 'PAISALO', 'BAGFILMS', 'SHREYAS', 'LOTUSEYE', 'MASFIN', 'TRIDENT', 'KESORAMIND',
               'SURANASOL', 'SIMPLEXINF', 'NURECA', 'TATACOMM', 'MARINE', 'IGL', 'SHOPERSTOP', 'TVVISION', 'KAKATCEM',
               'RATEGAIN', 'DISHTV', 'DMART', 'SWANENERGY', 'KINGFA', 'MAHLOG', 'JAIPURKURT', 'RAILTEL', 'RELINFRA',
               'AVROIND', 'INOXWIND', 'OMAXE', 'DOLLAR', 'TMB', 'SMARTLINK', 'GENUSPOWER', 'JSLHISAR', 'ORIENTLTD',
               'ATLANTA', 'GREENLAM', 'MAGADSUGAR', 'MANINFRA', 'TOTAL', 'POWERINDIA', 'MONARCH', 'KIRLOSENG', 'KRBL',
               'EIHOTEL', 'BIL', 'KOTAKBANK', 'ISMTLTD', 'GRWRHITECH', 'SHAREINDIA', 'SHILPAMED', 'ISEC', 'VESUVIUS',
               'NIPPOBATRY', 'GPTINFRA', 'MAXHEALTH', 'CCL', 'CINEVISTA', 'WELENT', 'BURNPUR', 'GANECOS', 'NEXTMEDIA',
               'GENESYS', 'RANEHOLDIN', 'KSOLVES', 'SGIL', 'PANACHE', 'BHANDARI', 'DHANUKA', 'KRITI', 'GLOBAL',
               'SWSOLAR', 'HIKAL', 'HFCL', 'SIS', 'SHIVALIK', 'SABTN', 'NXTDIGITAL', 'IFBAGRO', 'DODLA', 'ASIANTILES',
               'SHANTIGEAR', 'DALMIASUG', 'DEVIT', 'ROML', 'UNIVPHOTO', 'WEWIN', 'MAXIND', 'JSWSTEEL', 'CENTENKA',
               'GRMOVER', 'IGPL', 'BOMDYEING', 'SFL', 'TRITURBINE', 'COFFEEDAY', 'BIRLAMONEY', 'PEL', 'PITTIENG',
               'SYNCOMF', 'KANANIIND', 'CHEMCON', 'NIITLTD', 'SPLIL', 'CONCOR', 'ARCHIDPLY', 'VINATIORGA', 'OBCL',
               'COFORGE', 'AVADHSUGAR', 'PERSISTENT', 'KAYA', 'INDSWFTLTD', 'NKIND', 'RML', 'INFIBEAM', 'APCL',
               'LUMAXTECH', 'AUROPHARMA', 'MOTILALOFS', 'BANDHANBNK', 'CALSOFT', 'ABB', 'GOLDIAM', 'HARDWYN',
               'NAHARSPING', 'MUKANDLTD', 'TV18BRDCST', 'SHRIPISTON', 'GSCLCEMENT', 'L&TFH', 'BAJAJHCARE', 'SUNDARMFIN',
               'HPAL', 'BRIGADE', 'COUNCODOS', 'MRO-TEK', 'SHYAMTEL', 'RITCO', 'TERASOFT', 'BIRLACABLE', 'GEEKAYWIRE',
               'PONNIERODE', 'ARVEE', 'CONTROLPR', 'HEXATRADEX', 'MOKSH', 'OAL', 'METALFORGE', 'TAKE', '21STCENMGM',
               'GILLETTE', 'SHREERAMA', 'EMUDHRA', 'TATACOFFEE', 'MALLCOM', 'RBL', 'VIJIFIN', 'CHALET', 'AARON',
               'MANAKCOAT', 'SRHHYPOLTD', 'ANANDRATHI', 'PNBHOUSING', 'AHLADA', 'JASH', 'MCLEODRUSS', 'FDC', 'LINC',
               'BBTCL', 'ACI', 'CERA', 'BIOFILCHEM', 'MMP', 'ANANTRAJ', 'HIRECT', 'KSCL', 'APTECHT', 'VLSFINANCE',
               'CAMLINFINE', 'INDOSTAR', 'ICEMAKE', 'MONTECARLO', 'DEEPAKFERT', 'CREATIVE', 'ORBTEXP', 'SUNDARMHLD',
               'WIPL', 'CENTEXT', 'KCP', 'URJA', 'BBTC', 'RAIN', 'SADBHIN', 'VISASTEEL', 'FINCABLES', 'SOUTHWEST',
               'NOCIL', 'PCBL', 'SAREGAMA', 'BHEL', 'AMBICAAGAR', 'NITINSPIN', 'SHRADHA', 'JUBLPHARMA', 'GLS',
               'NLCINDIA', 'BECTORFOOD', 'KDDL', 'SPORTKING', 'GABRIEL', 'PAR', 'ARMANFIN', 'ICICIGI', 'MANORAMA',
               'LOYALTEX', 'RPOWER', 'DCMSHRIRAM', 'REPCOHOME', 'TVSMOTOR', 'UNICHEMLAB', 'GEOJITFSL', 'LPDC',
               'SABEVENTS', 'DHRUV', 'TIRUPATIFL', 'IVC', 'VIKASECO', 'AETHER', 'ELECON', 'JINDWORLD', 'SAKAR',
               'SCHNEIDER', 'JPPOWER', 'SBIN', 'EIFFL', 'KANPRPLA', 'RNAVAL', 'BODALCHEM', 'APLLTD', 'BLUEDART', 'SIL',
               'SUNDRMFAST', 'PNB', 'JITFINFRA', 'PTC', 'RAJTV', 'ALKYLAMINE', 'SATIN', 'SPCENET', 'ZOMATO', 'CROMPTON',
               'SUNCLAYLTD', 'TCPLPACK', 'BARBEQUE', 'DNAMEDIA', 'BHARATWIRE', 'LFIC', 'KPITTECH', 'EPL', 'FMGOETZE',
               'RVNL', 'VISESHINFO', 'SARDAEN', 'KCPSUGIND', 'PANAMAPET', 'ORTINLAB', 'SHREECEM', 'PARADEEP',
               'RADHIKAJWE', 'IFGLEXPOR', 'GAYAHWS', 'WEIZMANIND', 'GULFOILLUB', 'SUTLEJTEX', 'RAJRATAN', 'MEDICO',
               'NAUKRI', 'SSWL', 'GRAVITA', 'WINDMACHIN', 'HINDOILEXP', 'VINYLINDIA', 'GULFPETRO', 'GODREJPROP',
               'VINNY', 'PREMIERPOL', 'SIKKO', 'MOLDTKPAC', 'JAGSNPHARM', 'CLNINDIA', 'GMBREW', 'VSSL', 'HINDCOMPOS',
               'NBIFIN', 'VSTIND', 'CLEAN', 'KIRLOSIND', 'MUNJALSHOW', 'DALBHARAT', 'E2E', 'HITECHGEAR', 'BPCL',
               'SUMMITSEC', 'ICIL', 'SBICARD', 'MOL', 'J&KBANK', 'UJJIVANSFB', 'ARENTERP', 'DLF', 'JTLIND',
               'BIRLACORPN', 'ZOTA', 'IL&FSENGG', 'SDBL', 'DHUNINV', 'VERTOZ', 'MATRIMONY', 'RAJSREESUG', 'PIDILITIND',
               'TASTYBITE', 'ASTERDM', 'AARVEEDEN', 'JKIL', 'TRENT', 'LAXMIMACH', 'MSUMI', 'DIXON', 'RATNAMANI',
               'INDORAMA', 'KARMAENG', 'SHIVAMILLS', 'MASKINVEST', 'REDINGTON', 'SWARAJENG', 'JBMA', 'MCDOWELL-N',
               'CHOICEIN', 'GANGESSECU', 'GREAVESCOT', 'CHOLAHLDNG', 'NARMADA', 'IRCON', 'UNITEDTEA', 'RUCHIRA',
               'BANKINDIA', 'SUPERSPIN', 'JYOTISTRUC', 'DRCSYSTEMS', 'WANBURY', 'HINDWAREAP', 'AMBER', 'PGEL', 'INDOCO',
               'SASTASUNDR', 'UNIVCABLES', 'DCAL', 'VOLTAS', 'JUBLINGREA', 'ASAHIINDIA', 'PGHH', 'MARKSANS',
               'INDTERRAIN', 'MFL', 'DPSCLTD', 'FEL', 'EXIDEIND', 'SAIL', 'TALBROAUTO', 'LIBAS', 'LIKHITHA',
               'BHARATGEAR', 'MARICO', 'DCI', 'BHAGYAPROP', 'KRITINUT', 'SBCL', 'HITECH', 'RVHL', 'BUTTERFLY',
               'SPENTEX', 'PRIVISCL', 'FIVESTAR', 'TCS', 'AURIONPRO', 'INOXLEISUR', 'APOLLOHOSP', 'FEDERALBNK',
               'DEVYANI', 'KAPSTON', 'TOKYOPLAST', 'STARTECK', 'RAMCOIND', 'DCW', 'BALLARPUR', 'SURYAROSNI', 'TARC',
               'GUJAPOLLO', 'PARAS', 'APOLLOPIPE', 'SAKHTISUG', 'WSTCSTPAPR', 'MINDTECK', 'PODDARMENT', 'UMESLTD',
               'KAMATHOTEL', 'VIDHIING', 'INDIAGLYCO', 'NACLIND', 'PRAJIND', 'INTENTECH', 'MOREPENLAB', 'CESC',
               'FOODSIN', 'OFSS', 'NOVARTIND', 'EMAMIPAP', 'UNOMINDA', 'FOSECOIND', 'OBEROIRLTY', 'TCI', 'PFS',
               'CEATLTD', 'GANDHITUBE', 'OMKARCHEM', 'M&M', 'THOMASCOOK', 'BANSWRAS', 'SMSPHARMA', 'GFLLIMITED',
               'GOACARBON', 'IITL', 'BEARDSELL', 'LICHSGFIN', 'TORNTPHARM', 'AKSHARCHEM', 'UNIENTER', 'SUNTV', 'BRNL',
               'COASTCORP', 'COSMOFIRST', 'CARYSIL', 'VIKASPROP', 'UNITECH', 'GRASIM', 'SEPOWER', 'MAWANASUG',
               'ABMINTLLTD', 'CASTROLIND', 'KREBSBIO', 'ASHAPURMIN', 'GRAPHITE', 'RESPONIND', 'BESTAGRO', 'MANGCHEFER',
               'ATUL', 'DIGISPICE', 'GPIL', 'SHAHALLOYS', 'GANESHBE', 'BPL', 'MIDHANI', 'JTEKTINDIA', 'IRISDOREME',
               'KAVVERITEL', 'SHYAMMETL', 'MAGNUM', 'KHAICHEM', 'LTI', 'AVTNPL', 'PALASHSECU', 'TARMAT', 'TATAMOTORS',
               'IVP', 'SHEMAROO', 'ASIANHOTNR', 'HDIL', 'MSTCLTD', 'SUNDARAM', 'ALLSEC', 'LOKESHMACH', 'PRITIKAUTO',
               'STAR', 'ANUP', 'MUKTAARTS', 'CELEBRITY', 'HERCULES', 'SPLPETRO', 'BALMLAWRIE', 'SUBEXLTD', 'DOLATALGO',
               'INDOTECH', 'LODHA', 'PATINTLOG', 'OCCL', 'VETO', 'DCBBANK', 'FLUOROCHEM', 'BALKRISHNA', 'EDELWEISS',
               'REFEX', 'RELAXO', 'BANARISUG', 'ASHOKLEY', 'ASTRAL', 'GODREJIND', 'LAMBODHARA', 'KHANDSE', 'KIRLOSBROS',
               'ORIENTBELL', 'GODREJCP', 'PFOCUS', 'BATAINDIA', 'BBL', 'PTL', 'SUMICHEM', 'WILLAMAGOR', 'ELECTCAST',
               'HERITGFOOD', 'WFL', 'PATANJALI', 'CRISIL', 'POWERMECH', 'KIRLFER', 'DCMFINSERV', '20MICRONS',
               'STEELCAS', 'IBREALEST', 'HATSUN', 'GARFIBRES', 'ONEPOINT', 'KSHITIJPOL', 'CGCL', 'HMVL', 'INVENTURE',
               'APEX', 'ASTRON', 'STYLAMIND', 'BHAGYANGR', 'VBL', 'SELAN', 'NUVOCO', 'IMPEXFERRO', 'TATVA', 'PATELENG',
               'BIKAJI', 'CANBK', 'MINDACORP', 'NEOGEN', 'VENUSREM', '4THDIM', 'AGARIND', 'LYKALABS', 'DCXINDIA',
               'LAGNAM', 'KHAITANLTD', 'MICEL', 'CHEMPLASTS', 'MAZDA', 'AUTOAXLES', 'PETRONET', 'BSOFT', 'BVCL',
               'SANDHAR', 'VADILALIND', 'GNA', 'BSE', 'CUB', 'PPL', 'TEJASNET', 'NATCOPHARM', 'DONEAR', 'GREENPANEL',
               'AAREYDRUGS', 'GRPLTD', 'PKTEA', 'YESBANK', 'PIONEEREMB', 'ECLERX', 'ASPINWALL', 'UJJIVAN', 'ALICON',
               'HCLTECH', 'TRACXN', 'ORIENTELEC', 'SIMBHALS', 'ESSEN-RE1', 'MCL', 'JAYSREETEA', 'BANARBEADS', 'VCL',
               'CHENNPETRO', 'GMMPFAUDLR', 'IONEXCHANG', 'SKIPPER', 'SURYALAXMI', 'LANCER', 'MANAKALUCO', 'UDAICEMENT',
               'INDIANB', 'AXITA', 'VIPCLOTHNG', 'ITDC', 'LTTS', 'CYBERTECH', 'MBAPL', 'MANALIPETC', 'NAVNETEDUL',
               'WONDERLA', 'VIJAYA', 'ADANIPOWER', 'LAURUSLABS', 'UCALFUEL', 'VISHWARAJ', 'RAMRAT', 'PDSL', 'KENNAMET',
               'VARROC', 'KMSUGAR', 'LAKPRE', 'SRF', 'POLYPLEX', 'NFL', 'MEDICAMEQ', 'LASA', 'ASIANPAINT', 'SREINFRA',
               'ADORWELD', 'SALZERELEC', 'RHIM', 'SARLAPOLY', 'GSFC', 'TECHNOE', 'SONATSOFTW', 'GLFL', 'SRTRANSFIN',
               'SJVN', 'KOTHARIPRO', 'SOBHA', 'TREEHOUSE', 'RUSHIL', 'GANESHHOUC', 'PREMIER', 'SPANDANA', 'GREENPOWER',
               'SAKUMA', 'INOXGREEN', 'TIMETECHNO', 'BANKBARODA', 'PUNJABCHEM', 'BLKASHYAP', 'SATINDLTD', 'AYMSYNTEX',
               'TORNTPOWER', 'AVANTIFEED', 'INDHOTEL', 'GODHA', 'ALKEM', 'EMKAY', 'INDNIPPON', 'MAHSEAMLES', 'IFCI',
               'HEADSUP', 'RUBYMILLS', 'HINDALCO', 'GVKPIL', 'PCJEWELLER', 'HTMEDIA', 'JINDALSAW', 'UCOBANK', 'GET&D',
               'DSSL', 'LCCINFOTEC', 'JWL', 'STARCEMENT', 'MADHUCON', 'VENUSPIPES', 'EXPLEOSOL', 'MBECL', 'ISFT',
               'PRAKASH', 'ADANIGREEN', 'CARTRADE', 'SAGCEM', 'GRSE', 'TAJGVK', 'THEINVEST', 'ADVENZYMES', 'UTTAMSUGAR',
               'CAPACITE', 'SADBHAV', 'BAJFINANCE', 'QUESS', 'UJAAS', 'TTML', 'COMPINFO', 'CORALFINAC', 'MAHASTEEL',
               'RPGLIFE', 'ORIENTPPR', 'RGL', 'SAPPHIRE', 'GOKEX', 'RTNPOWER', 'ITDCEM', 'DELPHIFX', 'HCL-INSYS',
               'DUCON', 'UTIAMC', 'IDEA', 'SANGINITA', 'KRIDHANINF', 'RELIGARE', 'BCG', 'GEECEE', 'ORIENTCEM',
               'MAHESHWARI', 'ANSALAPI', 'DYCL', 'SOUTHBANK', 'DBSTOCKBRO', 'EROSMEDIA', 'SANGHVIMOV', 'CSBBANK',
               'DATAPATTNS', 'PVR', 'SHYAMCENT', 'MMTC', 'AARTIDRUGS', 'CYIENT', 'INGERRAND', 'SEQUENT', 'TIPSFILMS',
               'GOKUL', 'APOLSINHOT', 'TINPLATE', 'MEP', 'IDFC', 'GREENPLY', 'ARVIND', 'ALANKIT', 'GMRINFRA', 'KILITCH',
               'BOROLTD', 'SANDESH', 'SHANKARA', 'MANGLMCEM', 'ASAHISONG', 'RCF', 'DEEPAKNTR', 'MODIRUBBER', 'NBCC',
               'SALONA', 'NCLIND', 'DATAMATICS', 'FLFL', 'UGARSUGAR', 'VISHNU', 'ENERGYDEV', 'TRF', 'ANTGRAPHIC',
               'XCHANGING', 'SIRCA', 'HUDCO', 'AWHCL', 'BALAJITELE', 'RUCHINFRA', 'TIPSINDLTD', 'ACC', 'HGS',
               'MUTHOOTCAP', 'TPLPLASTEH', 'EXCEL', 'GOENKA', 'KERNEX', 'RSYSTEMS', 'JOCIL', 'BOHRAIND', 'HLVLTD',
               'KEEPLEARN', 'JPASSOCIAT', 'AMBIKCO', 'NAVA', 'DEEPINDS', 'VIPIND', 'TBZ', 'BAJAJHLDNG', 'EASTSILK',
               'OMAXAUTO', 'OSWALAGRO', 'IOLCP', 'CUMMINSIND', 'APLAPOLLO', 'PIIND', 'ZENITHEXPO', 'SHREEPUSHK', 'IRFC',
               'IEX', 'FMNL', 'DMCC', 'MORARJEE', 'EICHERMOT', 'CONSOFINVT', 'GRANULES', 'EMIL', 'SMLT', 'GLAXO',
               'HGINFRA', 'HSCL', '3PLAND', 'NETWORK18', 'NATIONALUM', 'ZENSARTECH', 'PREMEXPLN', 'OILCOUNTUB',
               'HATHWAY', 'VTL', 'DAMODARIND', 'NSIL', 'PEARLPOLY', 'ATFL', 'ASHIMASYN', 'BINDALAGRO', 'SANOFI',
               'GLOBALVECT', 'ROUTE', 'CSLFINANCE', 'FINPIPE', 'NILASPACES', 'ABAN', 'EQUITASBNK', 'ASTRAZEN',
               'MAHINDCIE', 'THEMISMED', 'MITTAL', 'POKARNA', 'ABFRL', 'TATAMETALI', 'BAJAJHIND', 'BALPHARMA',
               'TFCILTD', 'HILTON', 'PVP', 'RIIL', 'WABAG', 'IIFL', 'KABRAEXTRU', 'A2ZINFRA', 'LSIL', 'HARSHA',
               'VIPULLTD', 'BHARTIARTL', 'NATHBIOGEN', 'KBCGLOBAL', 'SKFINDIA', 'CAPLIPOINT', 'ITC', 'KUANTUM',
               'PRAXIS', 'PRAENG', 'SECURCRED', 'MAHABANK', 'SUVENPHAR', 'KOLTEPATIL', 'TATACHEM', 'NAZARA', 'VRLLOG',
               'NGLFINE', 'IRB', 'INDIGO', 'IFBIND', 'AIAENG', 'RKEC', 'SHAILY', 'TIINDIA', 'EIDPARRY', 'SUPERHOUSE',
               'KALYANI', 'ERIS', 'ROLTA', 'RUSTOMJEE', 'PNCINFRA', 'RSWM', 'XPROINDIA', 'KOTARISUG', 'NAM-INDIA',
               'SCPL', 'UFLEX', 'PRESSMN', 'NAHARPOLY', 'RALLIS', 'CENTRUM', 'SUKHJITS', 'NEWGEN', 'GRINDWELL',
               'JINDRILL', 'MGEL', 'SUNPHARMA', 'REPL', 'DAAWAT', 'AARVI', 'MEDPLUS', 'SUDARSCHEM', 'BFUTILITIE',
               'YUKEN', 'FORTIS', 'NAGREEKCAP', 'PODDARHOUS', 'LALPATHLAB', 'PIONDIST', 'BCP', 'JKTYRE', 'SIEMENS',
               'ANDREWYU', 'FORCEMOT', 'SUPRIYA', 'PARAGMILK', 'ADANIPORTS', 'JAIBALAJI', 'TARAPUR', 'TI', 'MPSLTD',
               'GAYAPROJ', 'GUJGASLTD', 'HISARMETAL', 'MANUGRAPH', 'SEAMECLTD', 'SURYODAY', 'MOTHERSON', 'BCLIND',
               'RELIANCE', 'CRAFTSMAN', 'NUCLEUS', 'HPL', 'STARHEALTH', 'DHARSUGAR', 'MELSTAR', 'PPLPHARMA', 'TNPETRO',
               'ASALCBR', 'SMLISUZU', 'AGRITECH', 'JBFIND', 'BYKE', 'SANSERA', 'TDPOWERSYS', 'GATEWAY', 'GOLDTECH',
               'LT', 'SINTERCOM', 'INDOWIND', 'WELCORP', 'HINDCON', 'KKCL', 'NELCO', 'RENUKA', 'NITCO', 'PDMJEPAPER',
               'MEGASTAR', 'GICHSGFIN', 'EQUITAS', 'NIRAJISPAT', 'ARTNIRMAN', 'KOVAI', 'IPCALAB', 'GTLINFRA', 'JCHAC',
               'SUPREMEINF', 'MOLDTECH', 'CDSL', 'TOUCHWOOD', 'JINDALPHOT', 'TGBHOTELS', 'OMINFRAL', 'DREDGECORP',
               'ORCHPHARMA', 'BEPL', 'DELTAMAGNT', 'UNIVASTU', 'ANIKINDS', 'UBL', 'VIVIDHA', 'ICICIPRULI', 'SPECIALITY',
               'TCNSBRANDS', 'CHEVIOT', 'GUJRAFFIA', 'IGARASHI', 'RPPL', 'CHAMBLFERT', 'ALEMBICLTD', 'SPTL',
               'SUPREMEENG', 'NTPC', 'PAYTM', 'TNTELE', 'BSHSL', 'TRU', 'CARBORUNIV', 'MAANALU', 'AROGRANITE', 'SCI',
               'ORISSAMINE', 'SOFTTECH', 'TVSSRICHAK', 'AJOONI', 'SUNFLAG', 'GENUSPAPER', 'INSECTICID', 'REVATHI',
               'ALMONDZ', 'VIKASWSP', 'RANEENGINE', 'RKFORGE', 'GPPL', 'MAHEPC', 'JKCEMENT', 'NRAIL', '3IINFOLTD',
               'CREDITACC', 'ATULAUTO', 'DBREALTY', 'AHLUCONT', 'AXISCADES', 'MANAKSIA', 'CENTRALBK', 'GTPL', 'BEML',
               'IDBI', 'DLINKINDIA', 'WEBELSOLAR', 'PNBGILTS', 'HONAUT', 'PRUDENT', 'JISLDVREQS', 'SIGACHI', 'XELPMOC',
               'CUPID', 'TIDEWATER', 'AMDIND', 'TITAN', 'ZIMLAB', 'DHANI', '63MOONS', 'TEXRAIL', 'SVPGLOB', 'KOHINOOR',
               'ADSL', 'HAL', 'SASKEN', 'STCINDIA', 'WINDLAS', 'ONMOBILE', 'STEL', 'KSL', 'DELTACORP', 'KELLTONTEC',
               'MUNJALAU', 'CAPTRUST', 'RICOAUTO', 'AAVAS', 'SHIVAMAUTO', 'UFO', 'CORDSCABLE', 'SILVERTUC', 'APARINDS',
               'JPINFRATEC', 'MEDANTA', 'HDFCAMC', 'DYNAMATECH', 'CMSINFO', 'FILATEX', 'ESTER', 'TIL', 'CIGNITITEC',
               'WINPRO', 'MAPMYINDIA', 'PRSMJOHNSN', 'KAJARIACER', 'GALLANTT', 'KSB', 'SAFARI', 'JSWISPL', 'TIMKEN',
               'USHAMART', 'ZEEL', 'ALPSINDUS', 'SALSTEEL', 'BOSCHLTD', 'TECHM', 'GKWLIMITED', 'KALYANKJIL', 'SEJALLTD',
               'BLISSGVS', 'HINDNATGLS', 'KICL', 'FCSSOFT', 'DVL', 'LGBFORGE', 'MAYURUNIQ', 'STOVEKRAFT', 'CAMPUS',
               'AMARAJABAT', 'SHREDIGCEM', 'VOLTAMP', 'GUJALKALI', 'BLUESTARCO', 'COROMANDEL', 'GMDCLTD', 'KNRCON',
               'TATAPOWER', 'PPAP', 'IOB', 'IPL', 'JMCPROJECT', 'BAJAJFINSV', 'MGL', 'STLTECH', 'RAMCOCEM', 'MALUPAPER',
               'JINDALPOLY', 'AAATECH', 'AGROPHOS', 'CHEMFAB', 'KANSAINER', 'ONGC', 'NAHARCAP', 'SOMANYCERA',
               'KRISHANA', 'ELGIRUBCO', 'TCIEXP', 'HDFCLIFE', 'GIPCL', 'LINDEINDIA', 'WIPRO', 'ORIENTALTL', 'MCX',
               'NMDC', 'ITI', 'ANGELONE', 'RKDL', 'IZMO', 'APTUS', 'TATAELXSI', 'THOMASCOTT', 'NAHARINDUS', 'OLECTRA',
               'GRINFRA', 'HARRMALAYA', 'ARVSMART', 'ROSSELLIND', 'ASIANENE', 'PSPPROJECT', 'RAMANEWS', 'GOCLCORP',
               'METROPOLIS', 'ACEINTEG', 'VHL', 'ZODIACLOTH', 'ORIENTHOT', 'MANINDS', 'CEREBRAINT', 'SUPRAJIT',
               'RAJESHEXPO', 'RADICO', 'HECPROJECT', 'SANGAMIND', 'HAVELLS', 'GAIL', 'PRITI', 'HCC', 'AIROLAM',
               'JPOLYINVST', 'TTKPRESTIG', 'DREAMFOLKS', 'FIEMIND', 'ORICONENT', 'NIACL', 'KEYFINSERV', 'RAINBOW',
               'TAINWALCHM', 'RAYMOND', 'FCL', 'SREEL', 'RPPINFRA', 'CENTURYPLY', 'PSB', 'AARTISURF', 'GODFRYPHLP',
               'KEC', 'BCONCEPTS', 'REPRO', 'NAGREEKEXP', 'RAMASTEEL', 'SETCO', 'MADRASFERT', 'ADVANIHOTR', 'SPIC',
               'POLICYBZR', 'IMPAL', 'INDUSINDBK', 'BALRAMCHIN', 'COMPUSOFT', 'JUSTDIAL', 'IDFCFIRSTB', 'PRESTIGE',
               'KAYNES', 'DBCORP', 'IBULHSGFIN', 'MASTEK', 'DYNPRO', 'MITCON', 'OPTIEMUS', 'NECCLTD', 'HIL', 'FACT',
               'NH', 'ASHIANA', 'AJMERA', 'CAMS', 'HOMEFIRST', 'AMBUJACEM', 'BERGEPAINT', 'ROLLT', 'MFSL', 'TEXMOPIPES',
               'ROTO', 'MACPOWER', 'BAJAJELEC', 'MUTHOOTFIN', 'FAZE3Q', 'AGSTRA', 'RTNINDIA', 'ALPHAGEO', '3MINDIA',
               'CLEDUCATE', 'KOPRAN', 'INDIGOPNTS', 'GNFC', 'SMSLIFE', 'JYOTHYLAB', 'LYPSAGEMS', 'GEPIL', 'LIBERTSHOE',
               'SUBROS', 'TRIGYN', 'PENINLAND', 'DHAMPURSUG', 'NITIRAJ', 'KALPATPOWR', 'CONFIPET', 'NIBL', 'PFC',
               'ANDHRSUGAR', 'SBC', 'SOTL', 'PRICOLLTD', 'GSPL', 'NAVKARCORP', 'FSC', 'JAYAGROGN', 'ENDURANCE',
               'KALYANIFRG', 'ASHOKA', 'ONELIFECAP', 'HOVS', 'INDIAMART', 'ADANIENT', 'ANURAS', 'ACCELYA', 'EMMBI',
               'MTARTECH', 'TATAMTRDVR', 'INDBANK', 'WATERBASE', 'SYNGENE', 'VMART', 'TEXINFRA', 'BGRENERGY',
               'CARERATING', 'JISLJALEQS', 'MURUDCERA', 'NECLIFE', 'WESTLIFE', 'HEG', 'RPSGVENT', 'ZENITHSTL', 'HNDFDS',
               'DCM', 'GHCL', 'ORTEL', 'ADFFOODS', 'SWELECTES', 'ROSSARI', 'DBOL', 'KITEX', 'SBILIFE', 'TNPL', 'MTNL',
               'BEDMUTHA', 'VINEETLAB', 'SANCO', 'IWEL', 'AUTOIND', 'ANMOL', 'CREST', 'LEMONTREE', 'PENIND',
               'HIMATSEIDE', 'SYRMA', 'BHAGCHEM', 'AGI', 'NCC', 'BSL', 'METROBRAND', 'AJANTPHARM', 'MEGASOFT', 'RECLTD',
               'GATI', 'SETUINFRA', 'SESHAPAPER', 'KPIGREEN', 'SEPC', 'ARCHIES', 'SCHAEFFLER', 'LAOPALA', 'MAXVIL',
               'SAGARDEEP', 'VIMTALABS', 'VENKEYS', 'LAXMICOT', 'MIRZAINT', 'MODISONLTD', 'ARTEMISMED', 'ESSARSHPNG',
               'JBCHEPHARM', 'NORBTEAEXP', 'MANAKSTEEL', 'PRIMESECU', 'ADANITRANS', 'BRITANNIA', 'INDOTHAI',
               'JKLAKSHMI', 'LOVABLE', 'EIMCOELECO', 'NEULANDLAB', 'PARSVNATH', 'DRREDDY', 'DHANBANK', 'EMAMIREAL',
               'ENIL', 'RSSOFTWARE', 'GTL', 'NDL', 'BALAMINES', 'MADHAV', 'TATACONSUM', 'JETAIRWAYS', 'UNITEDPOLY',
               'SALASAR', 'UMANGDAIRY', 'SHAKTIPUMP', 'DPABHUSHAN', 'INDSWFTLAB', 'PARACABLES', 'AKG', 'JAICORPLTD',
               'SILLYMONKS', 'ONWARDTEC', 'LGBBROSLTD', 'MBLINFRA', 'HEROMOTOCO', 'ZODIAC', 'TATASTEEL', 'SUMEETINDS',
               'CREATIVEYE', 'CIPLA', 'ENGINERSIN', 'SHALBY', 'EKC', 'CYBERMEDIA', 'CENTURYTEX', 'PRAKASHSTL',
               'KOKUYOCMLN', 'SAKSOFT', 'AKSHAR', 'JSL', 'HPIL', 'ICDSLTD', 'LXCHEM', 'ABCAPITAL', 'JAYNECOIND',
               'AKASH', 'TTL', 'AARTIIND', 'AMRUTANJAN', 'TREJHARA', 'GOCOLORS', 'WHIRLPOOL', 'AKZOINDIA', 'S&SPOWER',
               'SUMIT', 'MANGALAM', 'WELSPUNIND', 'WALCHANNAG', 'AKSHOPTFBR', 'ATGL', 'NDGL', 'VEDL', 'FINOPB', 'CCHHL',
               'CANFINHOME', 'EVEREADY', 'RAMCOSYS', 'ASTEC', 'MARUTI', 'THANGAMAYL', 'AMJLAND', 'EASEMYTRIP', 'SUZLON',
               'ALKALI', 'KRSNAA', 'CAREERP', 'ARIHANTSUP', 'SYMBOL', 'IIFLSEC', 'TIJARIA', 'INTLCONV', 'SANGHIIND',
               'DCMNVL', 'ZUARIIND', 'INDOAMIN', 'TATAINVEST', 'DGCONTENT', 'NYKAA', 'KOTHARIPET', 'ABSLAMC',
               'INDIACEM', 'HARIOMPIPE', 'MHRIL', 'GANGAFORGE', 'TATASTLLP', 'HMT', 'INFY', 'SRPL', 'JMFINANCIL',
               'HERANBA', 'POONAWALLA', 'SHARDAMOTR', 'PRECAM', 'RBLBANK', 'GESHIP', 'SOLARINDS', 'GLOBUSSPR', 'SUVEN',
               'JAGRAN', 'KARURVYSYA', 'GILLANDERS', 'HDFC', 'TFL', 'SAMBHAAV', 'VARDHACRLC', 'KPRMILL', 'VAISHALI',
               'DELHIVERY', 'HINDZINC', 'HEMIPROP', 'INSPIRISYS', 'GOKULAGRO', 'JHS', 'NELCAST', 'SOMICONVEY',
               'UMAEXPORTS', 'UGROCAP', 'DECCANCE', 'HBLPOWER', 'ASTRAMICRO', 'COALINDIA', 'JMA', 'OSIAHYPER', 'RAMKY',
               'CUBEXTUB', 'LUMAXIND', 'BIRLATYRE', 'KIRIINDUS', 'BEL', 'HAPPSTMNDS', 'VISAKAIND', 'MAHAPEXLTD', 'FSL',
               'JETFREIGHT', 'ANKITMETAL', 'DABUR', 'SONAMCLOCK', 'RUPA', 'KTKBANK', 'ESABINDIA', 'AXISBANK',
               'NATNLSTEEL', 'NIRAJ', 'BANCOINDIA', 'BAJAJ-AUTO', 'PURVA', 'SERVOTECH', 'GLAND', 'DIVISLAB', 'MAZDOCK',
               'PAGEIND', 'BHARATFORG', 'INDUSTOWER', 'GOODLUCK', 'PGHL', 'KIOCL', 'POLYCAB', 'GMRP&UI', 'INTELLECT',
               'TECHIN', 'JAYBARMARU', 'SECURKLOUD', 'SHRENIK', 'YAARI', 'AURUM', 'AMIORG', 'STARPAPER', 'VARDMNPOLY',
               'INDLMETER', 'MERCATOR', 'BHARATRAS', 'NOIDATOLL', 'VASWANI', 'INEOSSTYRO', 'NAVINFLUOR', 'VINDHYATEL',
               'BROOKS', 'LATENTVIEW', 'SUULD', 'ANDHRAPAP', 'RMCL', 'SHALPAINTS', 'HINDUNILVR', 'MARALOVER',
               'STEELCITY', 'DWARKESH', 'KRITIKA', 'CHOLAFIN', 'SOLARA', 'AFFLE', 'SNOWMAN', 'RAMAPHO', 'ARSSINFRA',
               'SHK', 'TEAMLEASE', 'SUNTECK', 'TVSELECT', 'PRECOT', 'SONACOMS', 'TRIVENI', 'MRF', 'AHLEAST', 'PNC',
               'CMICABLES', 'SPMLINFRA', 'MOHITIND', 'MPHASIS', 'MARATHON', 'DTIL', 'GOLDENTOBC', 'BALAXI', 'NESCO',
               'GSS', 'HINDCOPPER', 'IRIS', 'CHEMBOND', 'VGUARD', 'CTE', 'KIMS', 'FELDVR', 'GAL', 'COLPAL', 'LICI',
               'EIHAHOTELS', 'MSPL', 'ISGEC', 'KECL', 'BANKA', 'DPWIRES', 'RELCHEMQ', 'ABBOTINDIA', 'GOYALALUM', 'BLS',
               'HONDAPOWER', 'IRCTC', 'ROHLTD', 'ACCURACY', 'SIGIND', 'ZUARI', 'ZEEMEDIA', 'ELDEHSG', 'AUSOMENT',
               'IL&FSTRANS', 'HUHTAMAKI', 'BIGBLOC', 'KAMDHENU', 'BIOCON', 'SMCGLOBAL', 'PROZONINTU', 'TEMBO', 'PGIL',
               'LUXIND', 'BASF', 'SPARC', 'THYROCARE', 'JINDALSTEL', 'BASML', 'EXXARO', 'HUBTOWN', 'IMAGICAA',
               'MOTOGENFIN']


QUOTE_API = "https://type.fit/api/quotes"
QUOTES = requests.get("https://type.fit/api/quotes").json()

CHATTING = True

while CHATTING:
    sleep(5)
    share = pa.locateOnScreen('share.png', confidence=0.9)
    pa.moveTo(share[0], share[1])
    sleep(2)
    pa.moveRel(0, -40)
    s = pa.position()

    if battery.percent < 10:
        time = convert(battery.secsleft)
        pa.moveTo(share[0] + 100, share[1] + 10, duration=1)
        pa.click()
        pa.typewrite(
            f"hey bro Your battery percentage is {battery.percent}\n power plugged :{battery.power_plugged}\n "
            f"Battery left:{time}\n can i turn off PC(key:shutdown)")
        sleep(300)

    # ________checking for new messages__________#

    if pa.pixelMatchesColor(s[0], s[1], (255, 255, 255), tolerance=10):
        pa.rightClick()
        pa.moveRel(20, -190, 2)
        pa.doubleClick()
        sleep(2)
        message = []
        msg = pc.paste()
        message.append(msg)

        if SHUTDOWN_KEY == message[0]:
            pa.moveTo(share[0] + 100, share[1] + 10, duration=2)
            pa.doubleClick()
            pa.typewrite("bye bye ")
            os.system("shutdown /s /t 1")

        # ________checking for quote_______________#

        if QUOTE_KEY in message[0]:
            print('match')
            pa.moveTo(share[0] + 100, share[1] + 10, duration=2)
            pa.doubleClick()
            random_number = random.randint(0, 1643)
            pa.typewrite(f"{QUOTES[random_number]['text']} - {QUOTES[random_number]['author']}")
            pa.press('enter')

        # ________checking to stop the script_________#

        if STOP_KEY in message[0]:
            sleep(5)
            CHATTING = False

        # _________checking for stockcodes_____________#

        for code in STOCK_CODES:
            if code == message[0].lower() or code == message[0].upper():
                totalsell_q = nse.get_quote(message[0])['totalSellQuantity']  # NOQA
                company_name = nse.get_quote(message[0])['companyName']
                day_high = nse.get_quote(message[0])['dayHigh']
                base_price = nse.get_quote(message[0])['basePrice']
                sell_quantity = nse.get_quote(message[0])['sellQuantity1']
                pchange = nse.get_quote(message[0])['pChange']    # NOQA
                total_traded_value = nse.get_quote(message[0])['totalTradedValue']
                average_price = nse.get_quote(message[0])['averagePrice']
                open = nse.get_quote(message[0])['open']    # NOQA
                close_price = nse.get_quote(message[0])['closePrice']
                change = nse.get_quote(message[0])['change']
                last_price = nse.get_quote(message[0])['lastPrice']
                pa.moveTo(share[0] + 100, share[1] + 10, duration=2)
                pa.click()
                pa.typewrite(
                    f"Name:{company_name}\n OpenPrice:{open}\n LastPrice:{last_price}\n Change:{change}\n"
                    f"AveragePrice:{average_price}\n TotalTradedValue:{total_traded_value}\n pchange:{pchange}\n"
                    f"SellQuality:{sell_quantity}\n DayHigh:{day_high}\n BasePrice:{base_price}\n"
                    f"TotalSellQuantity:{totalsell_q}\n ")

        if message[0].upper() in FOREX_CURRENCIES:
            ser_obj = Service("C:/New folder/chromedriver.exe")
            driver = webdriver.Chrome(service=ser_obj)
            driver.get(url="https://in.investing.com/currencies/streaming-forex-rates-majors")

            currency_name_list = []
            for i in range(1, 40 + 2):
                currency_name = driver.find_element(By.XPATH, f'//*[@id="js-main-container"]/section[1]/div/section[2]/section/div[1]/div/table/tbody/tr[{i}]/td[3]/a')  # NOQA
                currency_name_list.append(currency_name.text)

            bid_price_list = []
            for i in range(1, 40 + 2):
                bid_price = driver.find_element(By.XPATH, f'//*[@id="js-main-container"]/section[1]/div/section[2]/section/div[1]/div/table/tbody/tr[{i}]/td[4]/span')   # NOQA
                bid_price_list.append(bid_price.text)

            ask_price_list = []
            for i in range(1, 40 + 2):
                ask_price = driver.find_element(By.XPATH, f'//*[@id="js-main-container"]/section[1]/div/section[2]/section/div[1]/div/table/tbody/tr[{i}]/td[5]/span')   # NOQA
                ask_price_list.append(ask_price.text)

            high_price_list = []
            for i in range(1, 40 + 2):
                high_price = driver.find_element(By.XPATH, f'//*[@id="js-main-container"]/section[1]/div/section[2]/section/div[1]/div/table/tbody/tr[{i}]/td[6]/span')   # NOQA
                high_price_list.append(high_price.text)

            low_price_list = []
            for i in range(1, 40 + 2):
                low_price = driver.find_element(By.XPATH, f'//*[@id="js-main-container"]/section[1]/div/section[2]/section/div[1]/div/table/tbody/tr[{i}]/td[7]/span')   # NOQA
                low_price_list.append(low_price.text)

            change_price_list = []
            for i in range(1, 40 + 2):
                change_price = driver.find_element(By.XPATH, f'//*[@id="js-main-container"]/section[1]/div/section[2]/section/div[1]/div/table/tbody/tr[{i}]/td[8]/span')   # NOQA
                change_price_list.append(change_price.text)

            change_percentage_list = []
            for i in range(1, 40 + 2):
                change_percentage = driver.find_element(By.XPATH, f'//*[@id="js-main-container"]/section[1]/div/section[2]/section/div[1]/div/table/tbody/tr[{i}]/td[9]/span')  # NOQA
                change_percentage_list.append(change_percentage.text)

            time_list = []
            for i in range(1, 40 + 2):
                time = driver.find_element(By.XPATH, f'//*[@id="js-main-container"]/section[1]/div/section[2]/section/div[1]/div/table/tbody/tr[{i}]/td[10]/time')   # NOQA
                time_list.append(time.text)
            driver.quit()
            sleep(10)
            pa.moveTo(share[0] + 100, share[1] + 10, duration=2)
            pa.doubleClick()
            index = currency_name_list.index(message[0])
            pa.typewrite(f"Currency Name:{currency_name_list[index]}\n Bid Price:{bid_price_list[index]}\n"
                         f" Ask Price:{ask_price_list[index]}\n High Price:{high_price_list[index]}\n "
                         f"Low Price:{low_price_list[index]}\n Change:{change_price_list[index]}\n "
                         f"Change in %:{change_percentage_list[index]}\n Time:{time_list[index]}\n ")

    else:
        sleep(CHECK_NEW_MESSAGE_IN_SEC)