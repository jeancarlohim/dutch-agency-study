#!/usr/bin/env python3
"""Mechanical keyword rules — step 1 of the mapping run (Aug 7, 2026).

Every rule here is a direct reading of a membership rule in one of the seven
JC-APPROVED bucket lists (outputs/2026-08-04-vocab-derivation/APPROVED-*.md).
No bucket is invented here. Anything the rules cannot place with a clear
winner is handed to the Sonnet tail pass; anything the tail pass cannot place
becomes "unknown".

Dutch glues words together (bedrijfsfilm, jubileumboek, klantportaal), so most
stems are matched as substrings on purpose. Short stems that would collide
(seo, sea, ads, ux, pr, it) keep their word boundaries.

Scoring, identical for every keyword axis:
  * each pattern carries a weight: 3 = decisive term, 2 = strong, 1 = weak
  * a bucket's score is the HIGHEST weight it matched (not the sum, so a
    bucket does not win by piling up generic words)
  * highest score wins
  * ties are resolved by the axis' own documented tie-break (see each axis)
  * no match at all -> ambiguous -> tail pass
"""
import re

AXES = ['clients_business', 'what_they_sell', 'problem_they_fix',
        'platform_or_channel', 'clients_money_model', 'clients_size',
        'where_clients_are']

# measures.py axis key  <->  focus-type name used everywhere JC reads
AXIS_KEY = {
    'clients_business': 'industry', 'what_they_sell': 'craft',
    'problem_they_fix': 'job', 'platform_or_channel': 'channel',
    'clients_money_model': 'model', 'clients_size': 'stage',
    'where_clients_are': 'geo',
}
SOURCE_FIELD = {
    'clients_business': 'sector_raw', 'what_they_sell': 'delivered_raw',
    'problem_they_fix': 'problem_raw', 'platform_or_channel': 'channel_evidence',
    'clients_money_model': 'model_evidence', 'clients_size': 'stage_evidence',
    'where_clients_are': 'geo_evidence',
}
CLAIM_FIELD = {
    'clients_business': 'claim_industry', 'what_they_sell': 'claim_craft',
    'problem_they_fix': 'claim_job', 'platform_or_channel': 'claim_channel',
    'clients_money_model': 'claim_model', 'clients_size': 'claim_stage',
    'where_clients_are': 'claim_geo',
}
UNKNOWN = 'unknown'

# ====================================================================== 1/7
# client's business (industry) — 17 buckets. Tie-break: first mentioned wins.
IND = {
 'Construction, real estate & housing': [
   (3, r'bouwbedrijf|bouwer|bouwsector|bouwbranche|bouwmarkt|bouwmateria|bouwgroothandel|aannemer|installatiebedrijf|installatiebranche|installateur|vastgoed|makelaar|makelaardij|real estate|woningcorporatie|woningbouw|woningmarkt|housing|architect|architectuur|interieurbouw|schroeffundering|construction|renovatie|verbouwing|dakdekker|dakwerk|loodgieter|stukadoor|schilder|glaszetter|tegelzetter|klusbedrijf|stoffeerder|vloerenlegger|vloeren bij|timmer|kozijn|badkamer|keukenzaak|keukenbranche|tuinaanleg|hovenier|zonwering|zonnepaneel|zonnepanelen|warmtepomp|isolatie|infrastructuur|civiele|grondverzet|projectontwikkelaar|property|verhuurmakelaar|bouwtoelevering'),
   (2, r'\bwonen\b|woning|huisvesting|gebouw|interieur|meubel|\bbouw\b|\binfra\b'),
 ],
 'Retail & e-commerce (general consumer goods)': [
   (3, r'e-?commerce|webshop|webwinkel|online winkel|online store|online retail|retailer|retailbranche|retailsector|\bretail\b|detailhandel|winkelketen|warenhuis|groothandel|distributeur|importeur|wholesale|consumer-?goods|consumentenelektronica|speelgoed|woonwinkel|woonbranche|home ?& ?living|home deco|tuincentrum|bouwmarkt|dierenwinkel|drogist|supermarkt|cadeau|kadowinkel|boekhandel|juwelier|sportwinkel|outdoorwinkel|babyartikelen|hygiene-?product'),
   (2, r'\bwinkel|verkoop van producten|consumentenproduct|merchandise|\bshop\b'),
 ],
 'Government & public sector': [
   (3, r'overheid|gemeente|provincie|ministerie|rijksoverheid|waterschap|publieke sector|public sector|\bgovernment\b|semi-?overheid|politie|brandweer|defensie|belastingdienst|\buwv\b|sociaal domein|rijkswaterstaat|omgevingsdienst|veiligheidsregio|ambtenaren|beleidsmakers|provinciehuis'),
   (2, r'publieke dienstverlening|bestuurlijk|\bpubliek\b'),
 ],
 'Manufacturing & industrial': [
   (3, r'industrie|industrieel|\bindustry\b|maakindustrie|fabrikant|fabriek|productiebedrijf|manufacturing|machinebouw|machinefabriek|metaalbewerking|metaalindustrie|\bstaal\b|staalbouw|kunststof|plastics|chemie|chemisch|technische bedrijven|technische organisaties|technisch bedrijf|toeleverancier|\boem\b|hightech|halfgeleider|semiconductor|prefab|betonfabriek|verpakkingsindustrie|scheepsbouw|maritieme industrie|aerospace|luchtvaartindustrie|aluminium|transformator|lasbedrijf|spuitgiet|matrijzen'),
   (2, r'\btechniek\b|installatietechniek|elektrotechniek|\bproductie\b'),
 ],
 'Hospitality, tourism, sports & recreation': [
   (3, r'horeca|\bhotel|restaurant|\bcaf[eé]\b|brasserie|catering|strandtent|strandpaviljoen|beachclub|discotheek|toerisme|tourism|vakantie|recreatie|recreatief|camping|bungalow|attractiepark|pretpark|dierentuin|leisure|sportschool|sportclub|sportvereniging|sportbranche|fitness|\bgym\b|golfbaan|golfclub|zwembad|wellness|sauna|reisorganisatie|reisbureau|\btravel\b|\breizen\b|congres|beursorganisat|evenementenbureau|evenementenlocatie|festival|escape ?room|bowling|\bevents?\b|hospitality|gastvrijheid'),
   (2, r'\bsport\b|uitgaan|dagje uit|verblijf|\bhoreca'),
 ],
 'Education & childcare': [
   (3, r'onderwijs|\bschool|scholen|schoolbestuur|basisschool|middelbare|\bmbo\b|\bhbo\b|universiteit|hogeschool|opleidingsinstituut|opleidingscentrum|opleider|e-?learning|kinderopvang|kinderdagverblijf|kindcentr|\bbso\b|peuterspeelzaal|childcare|education|academy|academie|studenten|leerlingen|docenten|leraren|bijles|cursusaanbieder|rijschool|theorieplatform|theoriecursus|driving-?theory|wetenschappelijk|onderzoeksprogramma|kennisinstituut|bibliotheek'),
   (2, r'trainingsbureau|\bcursus'),
 ],
 'Healthcare & care': [
   (3, r'\bzorg\b|zorgorganisat|zorginstelling|zorggroep|zorgaanbieder|zorgverlener|gezondheidszorg|healthcare|ziekenhuis|huisarts|tandarts|fysio|ergotherapie|logopedie|podotherapie|psycholoog|therapeut|apotheek|apotheken|medisch|farmaceut|\bfarma|pharma|\bggz\b|ouderenzorg|thuiszorg|verpleeg|kliniek|\bclinic|revalidatie|jeugdzorg|gehandicaptenzorg|welzijn|pati[eë]nt|\bdental|audicien|optiek|opticien|dierenarts|veterinair|hulpmiddelen voor'),
   (2, r'behandelingen|praktijk voor|\bzorg'),
 ],
 'Software, IT & telecom': [
   (3, r'\bsaas\b|software|it-?bedrijf|it-?dienstverlener|it-?branche|it-?sector|it-?leverancier|\bict\b|technologiebedrijf|technology company|telecom|hostingpartij|hostingprovider|\bcloud\b|app-?bouwer|cyber ?security|datacenter|internetprovider|e-?mailprovider|domeinregistratie|digital product|platformbedrijf|softwarehuis|developer tool'),
   (2, r'\bit\b|\btech\b|digitale dienstverlener|online platform'),
 ],
 'Business & professional services': [
   (3, r'zakelijke dienstverlening|professional services|advocaat|advocaten|juridisch|notaris|accountant|accountancy|administratiekantoor|boekhoud|fiscaal|consultancy|consultant|adviesbureau|advieskantoor|ingenieursbureau|architectenbureau|makelaarskantoor|onderzoeksbureau|zakelijke diensten|schoonmaakbedrijf|facilitair|beveiligingsbedrijf|beveiligingsbranche|\bbeveiliging\b|vertaalbureau|incassobureau|bureau voor'),
   (2, r'dienstverlen|\badvies\b|\bcoach|\btrainer\b|\bconsult'),
 ],
 'Food, beverage & agriculture': [
   (3, r'\bfood\b|foodservice|food-and-beverage|levensmiddel|\bvoeding|voedsel|bakkerij|slagerij|brouwerij|bierbrouwer|\bbier\b|wijnhandel|wijnhuis|\bdrank|zuivel|\bkaas\b|\bvlees\b|visserij|agrar|landbouw|akkerbouw|tuinbouw|glastuinbouw|veehouderij|kwekerij|kweker|agrifood|agricultuur|horticulture|banket|chocolade|\bkoffie|\bthee\b|maaltijd|snack|ingredi[eë]nt'),
   (2, r'\beten\b|\bfood'),
 ],
 'Transport, logistics & automotive': [
   (3, r'transport|logistiek|logistics|expediteur|\bvervoer|taxibedrijf|\btaxi\b|touringcar|verhuisbedrijf|koerier|warehousing|magazijn|\bhaven\b|scheepvaart|rederij|luchtvaart|\bairline|automotive|autobedrijf|autodealer|garagebedrijf|garagehouder|dealerbedrijf|\btruck|heftruck|\bbanden\b|fietsenwinkel|fietsmerk|mobiliteit|openbaar vervoer|\bspoor\b|jachten|\bjacht\b'),
   (2, r'\bauto\b|automerk|distributiecentrum'),
 ],
 'Fashion, beauty & personal goods': [
   (3, r'\bfashion|modemerk|modezaak|modebranche|modelabel|\bkleding|schoenen|lingerie|sieraden|jewel|horloge|\bbeauty|cosmetica|huidverzorging|haircare|\bkapper|kapsalon|barbier|nagelstudio|schoonheidssalon|parfum|make-?up|damesmode|herenmode|textiel|accessoires|\bbrillen|eyewear|persoonlijke verzorging'),
   (2, r'lifestyle|interieuraccessoires'),
 ],
 'Media, culture & entertainment': [
   (3, r'\bmedia\b|mediabedrijf|uitgever|uitgeverij|publisher|omroep|televisie|\btv\b|\bradio\b|filmhuis|bioscoop|cultuur|cultureel|\bculture\b|\bkunst|theater|schouwburg|\bpodium|muziek|\bband\b|artiest|entertainment|\bgames?\b|gaming|streaming|podcast|\bkrant|magazine|journalis|nieuwsplatform|nieuwssite|reclamebureau|creatief bureau|designbureau|designstudio|fotograaf|influencer|\bcreator\b|comedian'),
 ],
 'Finance & insurance': [
   (3, r'financieel|financi[eë]le|financial|\bbank\b|banking|verzekeraar|verzekering|\binsurer|\binsurance|assuranti|hypothe|pensioen|\bbelegg|investeer|investment|vermogensbeheer|kredietverlener|leasemaatschappij|\bincasso\b|fintech|betaaldienst|betaalprovider|crypto|accountantskantoor'),
   (2, r'geldzaken|financi[eë]le dienstverlening'),
 ],
 'Staffing, recruitment & HR': [
   (3, r'uitzendbureau|uitzend|detacher|recruitment|recruiter|werving en selectie|arbeidsbemiddeling|payroll|\bhr\b|human resources|headhunt|staffing|banenmarkt|zzp-?platform|interimbureau|interim management|talentbureau|personeelsdienst|personeel vindt|arbeidsmarkt'),
 ],
 'Energy, utilities & environment': [
   (3, r'energiebedrijf|energieleverancier|energiesector|energiemarkt|energietransitie|energiegebruiker|\benergy\b|duurzame energie|zonne-?energie|windpark|windenergie|netbeheerder|nutsbedrijf|waterbedrijf|waterleiding|\bafval|recycling|circulaire economie|\bmilieu|klimaat|warmtenet|gasnet|utilities|laadpaal|laadpalen|groene stroom'),
   (2, r'verduurzam|\bco2\b|sustainab|\benergie\b'),
 ],
 'Nonprofits, charities & associations': [
   (3, r'non-?profit|non-?for-?profit|goede doel|goededoelen|charit|stichting|vereniging|verenigingen|brancheorganisatie|belangenorganisatie|\bngo\b|\bfonds\b|fondsenwerving|donateur|vrijwilliger|maatschappelijke organisatie|\bkerk\b|religieus|foundation|kinderrechtenorganisatie|natuurorganisatie|dierenbescherming|salvation army|goed doel'),
   (2, r'ledenorganisatie|co[oö]peratie|maatschappelijk'),
 ],
}

# ====================================================================== 2/7
# what they sell (craft) — 18 buckets. Tie-break: first mentioned wins.
CRAFT = {
 'Website & webdesign': [
   (3, r'website|webdesign|web ?design|webontwikkeling|webdevelopment|web ?development|corporate site|bedrijfssite|landingspagina|landing ?page|one-?pager|wordpress|webflow|drupal|umbraco|typo3|craft ?cms|\bcms\b|content management systeem|webhosting|domeinregistratie|domeinnaam|site ?redesign|nieuwe site\b|websiteontwerp|siteontwerp|webbouw'),
   (2, r'\bsite\b|\bweb\b|development|hosting|migratie van .{0,20}domein'),
 ],
 'Webshop & e-commerce': [
   (3, r'webshop|webwinkel|e-?commerce|online winkel|online store|online shop\b|shopify|woocommerce|magento|shopware|lightspeed|commercetools|prestashop|bigcommerce|ccv ?shop|shopmigratie|productfeed'),
 ],
 'Branding & huisstijl': [
   (3, r'branding|brandmanual|brand ?(identity|design|strategy|book|guide|positioning|narrative|launch|platform)|huisstijl|merkidentiteit|merkstrategie|merkpositionering|merkarchitectuur|merkontwikkeling|merknaam|merkbelofte|merkverhaal|corporate identity|visuele identiteit|beeldmerk|woordmerk|naamgeving|\bnaming\b|restyl|styleguide|stijlgids|brand ?story|logo(?!p)'),
   (2, r'\bmerk\b|positionering|identiteit'),
 ],
 'Employer branding & recruitment': [
   (3, r'employer ?branding|werkgeversmerk|arbeidsmarktcommunicatie|wervingscampagne|wervingsvideo|wervingssite|wervingsmiddel|recruitment ?(marketing|campagne|site|video)|vacaturesite|vacaturepagina|vacaturecampagne|vacaturevideo|personeelswerving|werken ?bij|arbeidsmarkt ?campagne'),
 ],
 'SEO & vindbaarheid': [
   (3, r'\bseo\b|zoekmachine ?optimalisatie|zoekmachineoptimalisatie|zoekmachine ?optimisatie|search ?engine ?optimi|linkbuilding|link ?building|organische vindbaarheid|organische zichtbaarheid|organische groei|organische posities|organisch verkeer|organische verkeer|vindbaarheid in google|technische seo|answer ?engine'),
   (2, r'vindbaarheid'),
 ],
 'Online adverteren (paid ads)': [
   (3, r'\bsea\b|google ?ads|adwords|ad ?grants|meta ?ads|facebook ?ads|instagram ?ads|linkedin ?ads|tiktok ?ads|paid ?(ads|social|search|advertising|media)|online adverteren|adverteren op|display ?(advertising|campagne|banner)|programmatic|retargeting|remarketing|advertentiecampagne|advertentiebeheer|advertentiemanagement|search ?advertising|shopping ?campagne|bing ?ads|affiliate marketing|betaald verkeer|media-?inkoop|mediainkoop'),
   (2, r'\badvertising\b|\bads\b|advertenties|advertentie\b|campagnebudget'),
 ],
 'Campagnes & creatieve concepten': [
   (3, r'campagne|creatief concept|creative concept|conceptontwikkeling|conceptcreatie|reclamecampagne|\bactivatie|brand ?activation|creatieve strategie|creatieve regie|\bcommercial\b|reclame-?uiting'),
   (2, r'\bconcept|denkwerk|\bcreatie\b|maakwerk'),
 ],
 'Social media content & beheer': [
   (3, r'social ?media|socialmedia|sociale media|community ?management|instagram ?(content|feed|account)|linkedin ?(content|beheer)|social ?content|organisch social|\bsocials\b'),
   (2, r'\bsocial\b'),
 ],
 'Content & copywriting': [
   (3, r'copywriting|copywriter|tekstschrijven|teksten schrijven|\bteksten\b|redactie|contentmarketing|content ?(marketing|strategie|creatie|productie|plan|kalender)|\bblog|storytelling|webteksten|seo-?teksten|whitepaper|artikelen|\bcontent\b'),
 ],
 'Video, animatie & fotografie': [
   (3, r'video|animatie|animation|\bfilm|motion ?(design|graphics)|fotografie|photography|\bfoto|3d ?(visualisatie|render|animatie)|\bdrone|audioproductie|podcast|videoclip|aftermovie|livestream'),
 ],
 'Grafisch ontwerp, drukwerk & print': [
   (3, r'drukwerk|\bprint|flyer|poster|brochure|\bfolder|magazine|jaarverslag|jubileumboek|fotoboek|\bboek(je|en)?\b|visitekaartje|briefpapier|grafisch ontwerp|grafisch design|grafisch vormgever|communicatie grafisch|graphic ?design|graphics ?design|\bdtp\b|vormgeving|\bopmaak\b|illustratie|verpakkingsontwerp|packaging|labelontwerp|\bsigning\b|bewegwijzering|beursstand|spandoek|belettering|infographic|factsheet'),
   (2, r'\bontwerp\b|\bdesign\b'),
 ],
 'Apps & maatwerk platforms': [
   (3, r'\bapps?\b|mobiele app|web ?app|applicatie|maatwerk ?(software|platform|systeem|applicatie|oplossing)|custom ?(software|development|platform)|softwareontwikkeling|platformontwikkeling|porta(a)?l|intranet|koppeling|integratie|\bapi\b|configurator|booking ?engine|\bpwa\b|\bar\b|\bvr\b|augmented|virtual reality|interactives|digitale tool|dashboard'),
   (2, r'maatwerk|\bsysteem\b|\bplatform\b|\bsoftware\b'),
 ],
 'UX/UI & interface design': [
   (3, r'\bux\b|\bui\b|ux/?ui|user ?experience|user ?interface|interface ?(design|ontwerp)|interaction ?design|usability|prototyp|wireframe|design ?system|journey ?mapping|klantreis'),
 ],
 'E-mailmarketing, automation & funnels': [
   (3, r'e-?mail ?(marketing|campagne|flow|automation)|mailmarketing|nieuwsbrie(f|ven)|\bmailing|marketing ?automation|automation ?flow|\bfunnel|lead ?nurturing|klaviyo|mailchimp|activecampaign|hubspot|\bcrm\b|salesforce|pipedrive|whatsapp ?marketing|\bsms\b'),
 ],
 'Online marketing, performance & CRO': [
   (3, r'online marketing|digital marketing|digitale marketing|performance marketing|growth marketing|\bcro\b|conversie ?optimalisatie|conversieratio|conversion ?rate|a/?b ?test|web ?analytics|google ?analytics|data-?analyse|tracking|tag ?manager|meten en optimaliseren|marketingpartner|full-?service marketing'),
   (2, r'marketing|optimalisatie'),
 ],
 'Strategie & advies': [
   (3, r'strategie|strategy|strategisch|\badvies\b|consultancy|consulting|\bonderzoek|\bresearch\b|marktonderzoek|doelgroeponderzoek|workshop|\btraining|roadmap|mediaplan|communicatieplan|marketingplan|\baudit\b|persona|begeleiding|sparringpartner'),
   (2, r'\bplan\b'),
 ],
 'PR & influencer marketing': [
   (3, r'\bpr\b|public ?relations|persbericht|perswoordvoering|publiciteit|media ?relations|free ?publicity|influencer|ambassadeurscampagne|earned ?media'),
 ],
 'Outcome-verkoop (leads, omzet, groei)': [
   (3, r'lead ?(generatie|generation|gen)\b|leadgeneratie|leadgeneration|meer ?(omzet|klanten|aanvragen|leads|boekingen|verkoop)|omzetgroei|omzetverhoging|groeipartner|klanten leveren|new ?business|demand ?generation'),
 ],
}

# ====================================================================== 3/7
# problem they fix (job) — 16 buckets. Long narrative text; ties -> tail pass.
JOB = {
 'Meer leads, aanvragen & verkoop': [
   (3, r'meer ?(leads|aanvragen|klanten|omzet|verkoop|boekingen|offerte|reserveringen|afspraken|opdrachten)|leadgeneratie|nauwelijks aanvragen|te weinig ?(klanten|aanvragen|leads|omzet|opdrachten)|salesfunnel vullen|pipeline gevuld|winkeltraffic|meer verkopen|omzet ?(verhogen|vergroten)|nieuwe klanten ?(werven|aantrekken|binnenhalen)|klanten aan te trekken|opdrachten binnen te halen|koude acquisitie|nieuwe business|conversie verhogen'),
   (2, r'\bleads\b|meer conversie|\bacquisitie\b|meer rendement'),
 ],
 'Beter vindbaar in Google': [
   (3, r'(beter|hoger|goed) ?(vindbaar|scoren|ranken)|vindbaarheid ?(verbeteren|vergroten)|vindbaarheid in google|zoekmachine|\bseo\b|organische ?(posities|vindbaarheid|zichtbaarheid)|organisch verkeer|posities? ?(verloren|terugwinnen)|hoger in google|gevonden worden|niet ?(goed )?vindbaar'),
   (2, r'vindbaar'),
 ],
 'Naamsbekendheid & zichtbaarheid': [
   (3, r'naamsbekendheid|merkbekendheid|bekendheid ?(vergroten|cre[eë]ren|opbouwen|genereren)|meer bekendheid|op de radar|zichtbaarheid ?(vergroten|verbeteren)|online zichtbaarheid|online aanwezigheid|meer gezien worden|op de kaart zetten|onder de aandacht (te )?brengen|brand ?awareness|top ?of ?mind|profileren'),
   (2, r'zichtbaarder|bekender worden|\bbekendheid\b'),
 ],
 'Website verouderd of nieuw nodig': [
   (3, r'(website|site) ?(was|is) ?(verouderd|gedateerd|niet meer van deze tijd|aan vervanging toe|toe aan)|verouderde ?(website|site)|nieuwe website|website ?(voldeed niet|schoot tekort|liep achter|onoverzichtelijk|niet gebruiksvriendelijk|niet responsive|traag|optimaliseren)|digitale inhaalsprong|website ?(vernieuwen|herbouwen|opnieuw)|geen ?(fatsoenlijke )?website|cms ?(was|is) ?(lastig|verouderd)|schiet je huidige website tekort'),
   (2, r'website tekort|frisse (uitstraling|look)'),
 ],
 'Webshop & online verkoop': [
   (3, r'webshop|webwinkel|online ?(verkopen|verkoop|bestellen)|e-?commerce ?(platform|ambitie|omzet)|shopmigratie|bestelproces|orderwaarde|marketplace ?ambitie|verkopen via ?(bol|amazon)'),
 ],
 'Merk, huisstijl & verhaal': [
   (3, r'huisstijl|nieuwe huisstijl|merk ?(positionering|identiteit|verhaal|belofte|strategie)|positionering|positioneren|rebranding|identiteit ?(niet|onduidelijk|aanscherpen|versterken)|hoe vertel|verhaal ?(vertellen|helder)|complexiteit terug|onderscheidend vermogen|visuele identiteit|uitstraling|vertellen wat wij doen|eenduidige manier'),
   (2, r'\bmerk\b|\bstijl\b'),
 ],
 'Personeel werven & werkgeversmerk': [
   (3, r'personeel ?(werven|tekort|vinden)|vacature|nieuwe ?(collega|medewerkers|monteurs|verpleegkundigen|toppers)|arbeidsmarkt|krapte op de arbeidsmarkt|sollicitanten|werkgeversmerk|employer ?branding|wervingsuitdaging|werving van ?(personeel|medewerkers)|aantrekkelijk ?(als )?werkgever|lerarentekort|personeelstekort|werven van jongeren voor'),
 ],
 'Leden, leerlingen & donateurs werven': [
   (3, r'(leerlingen|studenten|deelnemers|leden|donateurs|vrijwilligers|ambassadeurs|abonnees|cursisten|verenigingen) ?(werven|aantrekken|binden|behouden|laten groeien|bereiken)|werven ?(van )?(nieuwe )?(leerlingen|studenten|deelnemers|leden|donateurs|vrijwilligers)|meer ?(leerlingen|studenten|leden|donateurs|vrijwilligers|deelnemers)|aanmeldingen stimuleren|ledenwerving|instroom van (leerlingen|studenten)|toekomstige leerlingen|ouders overtuigen|community .{0,20}laten groeien'),
 ],
 'Bewustwording & gedragsverandering': [
   (3, r'bewustwording|bewust ?(maken|worden|te laten)|gedragsverandering|gedrag ?(veranderen|be[iï]nvloeden)|awareness|voorlichting|mentaliteitsverandering|draagvlak|\btaboe\b|aandacht vragen voor|in beweging (worden gebracht|blijven)|het belang van .{0,30}onder de aandacht'),
 ],
 'Lancering nieuw product of concept': [
   (3, r'lancering|lanceren|\blaunch|introductie van|introduceren|nieuw ?(product|merk|concept|collectie|label|vestiging|locatie)|op de markt brengen|go-?to-?market|in de markt zetten'),
 ],
 'Content & creatieve productie': [
   (3, r'(video|film|animatie|fotografie|magazine|boek|brochure|display|presentatie|podcast) ?(nodig|maken|produceren|ontwikkelen|filmen)|behoefte aan ?(content|video|beeldmateriaal)|contentproductie|beeldmateriaal|geen ?(goede )?(fotos|beelden|content)|productiecapaciteit|nieuwe display|case study filmen'),
 ],
 'Advertenties & campagnes renderen niet': [
   (3, r'campagnes? ?(draaien|draaide|liepen|renderen|stagneren|zonder resultaat|leverden niets)|google ?ads|problemen met google|advertentiebudget|advertenties zonder resultaat|geen ?(duidelijk )?inzicht in de resultaten|geld ?(uitgegeven|verspild) zonder|wisselende ervaringen|slechte ervaring(en)? met|mediaplan|media ?(planning|inkoop)|rendement uit ?(ads|advertenties)|zonder duidelijk inzicht'),
 ],
 'Maatwerk software & efficiëntere processen': [
   (3, r'(proces|processen|workflow) ?(effici[eë]nter|verbeteren|digitaliseren|automatiseren|slimmer)|sneller en effici[eë]nter werken|handmatig|maatwerk ?(software|systeem|platform|applicatie)|systeem ?(verouderd|voldeed niet|koppelen)|koppeling|integratie met|automatiseren|digitalisering|offerte ?(maken|proces)|foutgevoelig|online platform moet'),
 ],
 'Klantbehoud & loyaliteit': [
   (3, r'klantbehoud|retentie|retention|loyaliteit|loyalty|bestaande klanten|terugkerende ?(klanten|deelnemers|bezoekers)|customer ?(experience|journey|lifetime)|klantreis|win-?back|\bchurn\b|klanttevredenheid'),
 ],
 'Groei & nieuwe markten': [
   (3, r'(internationale|verdere|structurele) groei|groeien in|opschalen|scale-?up|nieuwe ?(markt|markten|landen)|marktaandeel|expansie|uitbreiden naar|marktleider worden|next level|concurrerende markt|uitblinken'),
   (2, r'\bgroeien\b|\bgroei\b'),
 ],
 'Events & activaties': [
   (3, r'(event|evenement|beurs|congres|festival|klantendag|activatie) ?(organiseren|promoten|naar een hoger niveau|deelnemers|bezoekers)|ticketverkoop|meer ?(bezoekers|deelnemers) (naar|voor)|beursdeelname|standbezoek|on-?site experience|deelnemers werven voor|na de beurs'),
 ],
}

# ====================================================================== 4/7
# platform / channel — 14 buckets. Tie-break: 3+ tied buckets -> bucket 14
# ("multi-channel"), exactly as the approved list defines it; 2 tied -> first
# mentioned wins.
CHAN = {
 'SEO & organische vindbaarheid': [
   (3, r'\bseo\b|zoekmachine ?optimalisatie|zoekmachineoptimalisatie|zoekmachine ?optimisatie|search ?engine ?optimi|linkbuilding|link ?building|organische ?(vindbaarheid|zichtbaarheid|posities|groei|resultaten)|organisch verkeer|organische verkeer|\bgeo\b|answer ?engine|chatgpt|google my business|online search results'),
   (2, r'vindbaarheid'),
 ],
 'SEA, display & overige paid advertising': [
   (3, r'\bsea\b|google ?ads|adwords|ad ?grants|search ?ads|search engine marketing|\bsem\b|shopping ?(ads|campagne)|display ?(advertising|campagne|banner|html5)|programmatic|bing ?ads|microsoft ?ads|retargeting|remarketing|online adverteren|online advertenties|paid ?(search|advertising|media)|bannercampagne|advertentiecampagne|advertentiebeheer|affiliate marketing|betaald verkeer|media-?inkoop|mediainkoop|google advertenties|advertisement'),
   (2, r'\badvertising\b|adverteren|\bads\b|advertenties'),
 ],
 'Social media organisch': [
   (3, r'social ?media|socialmedia|sociale media|\bsocials\b|community ?management|organisch social|social ?content|influencer|instagram(?! ?ads)|facebook(?! ?ads)|linkedin(?! ?ads)|tiktok(?! ?ads)|youtube|pinterest|snapchat'),
   (2, r'\bsocial\b'),
 ],
 'Social media paid': [
   (3, r'social ?(ads|advertising|adverteren)|paid ?social|adverteren op ?(facebook|instagram|linkedin|tiktok|meta|social)|meta ?(ads|advertenties)|facebook ?ads|instagram ?ads|linkedin ?ads|tiktok ?ads|snapchat ?ads|pinterest ?ads'),
 ],
 'Website & CMS': [
   (3, r'website|webdesign|web ?design|webdevelopment|webontwikkeling|wordpress|webflow|umbraco|drupal|typo3|craft ?cms|joomla|laravel|symfony|\bframer\b|\bcms\b|content ?management ?systeem|headless|landingspagina|corporate site|webhosting'),
   (2, r'\bsite\b|\bweb\b'),
 ],
 'Webshop & e-commerceplatform': [
   (3, r'webshop|webwinkel|e-?commerce|online ?(winkel|store|shop)\b|shopify|woocommerce|magento|shopware|lightspeed|commercetools|prestashop|bigcommerce|ccv ?shop|shopmigratie'),
 ],
 'E-mail, CRM & marketing automation': [
   (3, r'e-?mail|mailmarketing|nieuwsbrie(f|ven)|mailflow|\bmailing|marketing ?automation|\bautomation\b|klaviyo|mailchimp|activecampaign|hubspot|salesforce|pipedrive|\bcrm\b|copernica|spotler|leadinfo|whatsapp|\bsms\b|push ?bericht'),
 ],
 'Content, video & PR': [
   (3, r'video|animatie|\bfilm|fotografie|\bfoto|motion|\b3d\b|\bdrone|podcast|\baudio|livestream|streaming|spotify|webinar|\bpr\b|public ?relations|persbericht|perswoordvoering|publiciteit|redactie|copywriting|\bcontent\b|storytelling|magazine|televisie ?commercial|television ?commercial|contentfeed'),
 ],
 'Offline media & events': [
   (3, r'\btv\b|televisie|\bradio\b|radiospot|\bprint\b|drukwerk|folder|flyer|poster|\babri\b|billboard|out[- ]?of[- ]?home|\bdoh\b|\booh\b|outdoor|direct ?mail|\bpost\b|dagblad|\bkrant|tijdschrift|\bbeurs|beurzen|\bevents?\b|evenement|bioscoop|narrowcasting|belettering|\bsigning\b|sponsoring'),
 ],
 'Apps & custom platforms': [
   (3, r'\bapps?\b|mobiele app|web ?app|applicatie|maatwerk ?(platform|software|systeem)|custom ?(platform|software)|porta(a)?l|intranet|\bapi\b|koppeling|integratie|configurator|booking ?engine|\bar\b|\bvr\b|augmented|virtual ?reality|interactives|\bpwa\b|mobile network'),
   (2, r'\bplatform\b|\bsoftware\b'),
 ],
 'Marktplaatsen & feeds': [
   (3, r'\bbol\b|bol\.com|amazon|marktplaats|marketplace|channable|productfeed|feed ?management|beslist\.nl|zalando'),
 ],
 'Branding, campagne & activatie': [
   (3, r'branding|huisstijl|merkidentiteit|merkstrategie|merkpositionering|brand ?(identity|design|strategy)|campagne|campaigning|creatief concept|\bactivatie|employer ?branding|recruitment ?(marketing|strategie)|arbeidsmarktcommunicatie|wervingscampagne|reclamecampagne|\blogo\b'),
 ],
 'Data, tracking & CRO': [
   (3, r'\bcro\b|conversie ?optimalisatie|conversion ?rate|a/?b ?test|\banalytics\b|google ?analytics|tracking|tag ?manager|data-?analyse|dashboard|rapportage|attributie|server ?side|cookie ?consent|websiteleads'),
 ],
 'Multi-channel & omnichannel': [
   (3, r'omni-?channel|multi-?channel|online marketing|digital marketing|digitale marketing|full ?service digital|alle online kanalen|360 ?graden|cross-?media|across channels|web ?& ?online'),
 ],
}

# ====================================================================== 5/7
# client's money model — 8 buckets. Tie-break from the approved list:
# webshop form > software-as-product > explicit both > audience.
RE_SHOP = re.compile(r'webshop|webwinkel|e-?commerce|ecommerce|online ?(winkel|store|shop)\b|\bd2c\b|\bdtc\b|woocommerce|shopify|magento|shopware|marketplace ?seller|verkoopt online|online verkoop|volledig online|pure ?player|bestelpagina')
RE_B2B = re.compile(r'\bb2b\b|b-?2-?b|business ?-?to-?-? ?business|zakelijke ?(klanten|markt|afnemers|kopers|rijders|dienstverlening)|\bzakelijk\b|bedrijven|ondernemers|professionals|inkopers|\bdealers?\b|installateurs|groothandel|distributeur|\boem\b|corporates|organisaties|afnemers|architecten|machinebouwers|werkgevers|opdrachtgevers|tuinders|agrari[eë]rs|artsen|vakmensen|monteurs|technisch managers|partners')
RE_B2C = re.compile(r'\bb2c\b|b-?2-?c|business ?-?to-?-? ?consumer|consument|particulier|eindgebruiker|shoppers|\bd2c\b|\bdtc\b|huurder|bewoners|ouders van|vrouw tussen|jongeren')
RE_SAAS = re.compile(r'\bsaas\b|software ?(as ?a ?service|platform|product)|het platform is|multisided ?marketplace|marketplace ?(platform|operator)|technologieplatform|platform voor|(hun|ons|eigen|met|via) ?(\w+ ){0,2}platform|empowers organizations|monitor .{0,20}metrics')
RE_PUB = re.compile(r'overheid|\bgemeente\b|gemeenten|ministerie|rijksoverheid|onderwijsinstelling|basisschol|middelbare school|hogeschool|universiteit|scholen\b|zorginstelling|zorgorganisat|zorggroep|zorgaanbieder|ziekenhuis|\bartsen\b|huisartsen|apotheken|vereniging|stichting|non-?profit|goede doel')
RE_SERV = re.compile(r'dienstverlen|uitzendbureau|detachering|consultancy|adviesbureau|accountant|advocaten|makelaar|beveiliging|schoonmaak|installatiebedrijf|opleiding|expertise|kandidaten')
RE_OFF = re.compile(r'horeca|restaurant|caf[eé]|\bhotel|\bwinkel|fysieke ?(winkel|retail)|\bgym\b|sportschool|salon|kapper|wellness|attractiepark|bioscoop|toerist|leisure')
_CONS = r'particulier\w*|consument\w*|b2c|bewoners|huurders|kandidaten|eindgebruikers|leden'
_BIZ = r'zakelijk\w*|bedrijven|b2b|aannemers|installateurs|dealers|werkgevers|professionals|organisaties|architecten|distributeurs|instellingen|woningbouwmaatschappijen|corporaties|verhuurders'
RE_BOTH = re.compile(r'(' + _CONS + r')[^|]{0,55}?\b(en|&|and|als|zowel)\b[^|]{0,55}?(' + _BIZ + r')|('
                     + _BIZ + r')[^|]{0,55}?\b(en|&|and|als|zowel)\b[^|]{0,55}?(' + _CONS + r')|'
                     r'b2b ?(&|en|and|\+) ?b2c|b2c ?(&|en|and|\+) ?b2b')
RE_B2B_TO_B2C = re.compile(r'(stap|overgang|transitie) van b2b naar b2c')

MODEL_ORDER = ['Webshop B2B', 'Webshop consumenten (D2C)', 'SaaS & software',
               'Gemengd', 'Zakelijke afnemers (B2B)', 'Consumentenmarkt offline',
               'Dienstverleners', 'Overheid, zorg & onderwijs']

def map_model(s):
    if RE_B2B_TO_B2C.search(s):
        return 'Zakelijke afnemers (B2B)', 'ruling: b2b->b2c transition stays B2B'
    if RE_SHOP.search(s):                       # form beats audience
        if RE_B2B.search(s) and not RE_B2C.search(s):
            return 'Webshop B2B', 'shop + business buyers named'
        return 'Webshop consumenten (D2C)', 'shop, default D2C'
    if RE_SAAS.search(s):
        return 'SaaS & software', 'client product IS the software/platform'
    if RE_BOTH.search(s):
        return 'Gemengd', 'both business and consumer customers named'
    if RE_PUB.search(s):
        return 'Overheid, zorg & onderwijs', 'public / care / education body'
    if RE_B2B.search(s) and not RE_B2C.search(s):
        return 'Zakelijke afnemers (B2B)', 'business buyers only'
    if RE_B2C.search(s) and not RE_B2B.search(s):
        return 'Consumentenmarkt offline', 'consumer buyers, no shop named'
    if RE_SERV.search(s):
        return 'Dienstverleners', 'sells services/expertise'
    if RE_OFF.search(s):
        return 'Consumentenmarkt offline', 'consumer-facing offline business'
    return None, ''

# ====================================================================== 6/7
# client's size — 6 buckets. Approved ruling: a stated size beats the family
# label; from-to trajectories file under Startup/jong/groeiend.
NUMWORD = r'(twee|drie|vier|vijf|zes|zeven|acht|negen|tien|elf|twaalf|twintig|dertig|veertig|vijftig|honderd|tweehonderd|driehonderd|duizend|two|three|four|five|six|seven|eight|nine|ten)'
RE_FROMTO = re.compile(r'van \d[\d\.\, ]*(naar|tot) ?\d|from \d+ to \d+|gegroeid (van|naar)|uitgegroeid tot|verdubbeld|expanding (its|from)|from a fledg')
UNIT = (r'medewerkers|werknemers|collega|fte|mensen|man\b|adviseurs|leden|deelnemers|'
        r'vestiging|locaties|filialen|winkels|stores|panden|scholen|leerlingen|klanten|'
        r'gasten|kamers|professionals|specialisten|monteurs|employees|people|staff|users|'
        r'gebruikers|volgers|inwoners|landen|countries|fabrieken|factories|m2|tuinen|'
        r'zorgorganisaties|zorgaanbieders|basisscholen|ondernemers|abonnees|bezoekers')
ORD = r'(tweede|derde|vierde|vijfde|zesde|zevende|achtste|negende|tiende)'
# a size in figures needs a NUMBER AND A UNIT. "38 jaar ervaring" is age, not size.
RE_NUM = re.compile(r'\d[\d\.\, ]*\+? ?(?:\w+ ){0,2}(' + UNIT + r')|'
                    + NUMWORD + r' (?:\w+ ){0,1}(' + UNIT + r')|'
                    + ORD + r' (vestiging|locatie|winkel|filiaal|fabriek)')
RE_SMALL = re.compile(r"\bzzp'?er|\bzzp\b|zelfstandige? (ondernemer|professional)|eenmanszaak|tweemanszaak|eigen praktijk|\beigenaar\b|kleine? (onderneming|ondernemer|bedrijf|praktijk|uitgeverij)|klein bedrijf|kleinste|\bsolo\b|freelance|bedrijfje|micro-?onderneming|lokale ondernemer")
RE_MKB = re.compile(r'\bmkb\b|mkb-?(bedrijf|bedrijven|er|ers)|\bsme\b|small-?medium|middelgroot|middelgrote|mid-?market|midden- ?en ?kleinbedrijf')
RE_START = re.compile(r'start-?up|scale-?up|jonge? (bedrijf|onderneming|organisatie)|nieuw bedrijf|net gestart|snelgroeiend|hard groeiend|in (sterke )?groei|groeiende? (bedrijf|onderneming|organisatie)|fledgling|fd ?gazelle|doorgroei|growing fast|fast-?growing|scaling|de start van')
RE_BIG = re.compile(r'\bcorporate\b|enterprise|grootste|marktleider|market ?leader|\bglobal\b|wereldwijd|multinational|beursgenoteerd|grote (bedrijven|onderneming|organisatie|speler|projecten|opdrachtgevers)|\blarge\b|biggest|largest|\bmega\b|toonaangevend|leidend|top ?\d|\bgiant\b|internationale speler|\bconcern\b|de standaard voor|nummer 1|de nummer|publicly listed')
RE_FAM = re.compile(r'familiebedrijf|family ?business|familie-?onderneming|\d+ jaar (bestaan|ervaring|geleden)|sinds (19|20)\d\d|jubileum|\d+-?jarig|\d+e verjaardag|opgericht in (19|20)\d\d|generatie|al \d+ jaar|established in (19|20)\d\d|(19|20)\d\d tot (19|20)\d\d|\d+e editie|' + NUMWORD + r'e editie|\d+ jaar')

def map_stage(s):
    if RE_FROMTO.search(s):
        return 'Startup / jong / groeiend', 'from-to growth trajectory'
    if RE_MKB.search(s):
        return 'MKB / middelgroot', 'SME label'
    if RE_SMALL.search(s):
        return 'Klein / zelfstandig', 'small or solo label'
    if RE_NUM.search(s):
        return 'Omvang in cijfers', 'concrete stated count'
    if RE_BIG.search(s):
        return 'Groot / corporate / marktleider', 'large-scale or market-leader words'
    if RE_START.search(s):
        return 'Startup / jong / groeiend', 'young / growing'
    if RE_FAM.search(s):
        return 'Familiebedrijf / gevestigd met historie', 'only signal is family/age'
    return None, ''

# ====================================================================== 7/7
# where the clients are — 7 buckets, checked most-specific first.
NL_PROVINCES = r"""groningen|frysl[aâ]n|friesland|friese|drenthe|overijssel|flevoland|gelderland|
noord-?holland|zuid-?holland|zeeland|zeeuwse|noord-?brabant|brabant|brabants|limburg|limburgse|
achterhoek|twente|veluwe|betuwe|bollenstreek|westland|kop van noord-?holland|zaanstreek|
kennemerland|het gooi|\bgooi\b|rivierenland|de peel|kempen|liemers|waterland|bommelerwaard|
hoeksche waard|groene hart|randstad|noorden van het land|zuiden van nederland|stedelijk gebied"""

NL_CITIES = r"""amsterdam|amsterdamse|rotterdam|rotterdamse|den haag|s-?gravenhage|the hague|utrecht|
eindhoven|tilburg|almere|breda|nijmegen|nijmeegse|apeldoorn|haarlem|arnhem|arnhemse|enschede|
amersfoort|zaanstad|zaandam|haarlemmermeer|hoofddorp|den bosch|s-?hertogenbosch|zwolle|
zoetermeer|leiden|leidse|leeuwarden|maastricht|dordrecht|\bede\b|alphen aan den rijn|
alkmaar|emmen|delft|venlo|deventer|helmond|\boss\b|hilversum|heerlen|amstelveen|purmerend|
roosendaal|schiedam|lelystad|gouda|spijkenisse|hoorn|vlaardingen|almelo|assen|bergen op zoom|
capelle aan den ijssel|veenendaal|katwijk|zeist|nieuwegein|hengelo|doetinchem|kampen|woerden|
hardenberg|oosterhout|waalwijk|middelburg|vlissingen|terneuzen|goes|sittard|geleen|weert|
roermond|uden|veghel|boxmeer|cuijk|gennep|beuningen|wijchen|elst|zevenaar|winterswijk|lochem|
zutphen|rheden|barneveld|nunspeet|harderwijk|ermelo|putten|nijkerk|bunschoten|soest|baarn|
bussum|naarden|weesp|diemen|uithoorn|aalsmeer|hillegom|lisse|noordwijk|voorschoten|wassenaar|
rijswijk|pijnacker|zoeterwoude|leiderdorp|oegstgeest|sassenheim|hoogeveen|meppel|steenwijk|
sneek|drachten|heerenveen|joure|dokkum|harlingen|franeker|bolsward|workum|stadskanaal|veendam|
winschoten|delfzijl|appingedam|hoogezand|beilen|coevorden|emmeloord|urk|dronten|zeewolde|
huizen|blaricum|laren|eemnes|houten|ijsselstein|vianen|culemborg|tiel|geldermalsen|zaltbommel|
oosterbeek|renkum|wageningen|rhenen|doorn|driebergen|maarssen|breukelen|mijdrecht|vinkeveen|
abcoude|bodegraven|waddinxveen|boskoop|nieuwkoop|alblasserdam|papendrecht|sliedrecht|gorinchem|
leerdam|hardinxveld|zwijndrecht|ridderkerk|barendrecht|rhoon|poortugaal|hellevoetsluis|brielle|
maassluis|naaldwijk|s-?gravenzande|monster|wateringen|de lier|honselersdijk|kwintsheul|berkel|
bleiswijk|bergschenhoek|nootdorp|leidschendam|voorburg|oisterwijk|goirle|dongen|kaatsheuvel|
loon op zand|drunen|heusden|vught|boxtel|schijndel|sint-?oedenrode|best\b|\bson\b|geldrop|mierlo|
nuenen|valkenswaard|bergeijk|eersel|bladel|reusel|hapert|deurne|asten|someren|gemert|bakel|
beek en donk|lieshout|erp\b|volkel|mill|grave|zandvoort|heemstede|bloemendaal|velsen|ijmuiden|
beverwijk|heemskerk|castricum|uitgeest|heiloo|limmen|egmond|schagen|den helder|texel|medemblik|
enkhuizen|volendam|edam|monnickendam|landsmeer|oostzaan|wormerland|beemster|krommenie|
wormerveer|assendelft|tegelen|blerick|panningen|horst|venray|nederweert|maasbracht|echt|
susteren|stein|beek\b|meerssen|valkenburg|gulpen|vaals|kerkrade|landgraaf|brunssum|hoensbroek|
nuth|voerendaal|simpelveld|bocholtz|zevenbergen|etten-?leur|westervoort|duiven|nissewaard|
bronckhorst|budel|kijkduin|bonaire|saba|sint-?eustatius|duinrell|scheveningen|noordwijkerhout|katwijk aan zee|rijnsburg|
valkenburg aan de rijn|nieuw-?vennep|badhoevedorp|hillegersberg|kralingen|delfshaven|
zuidas|jordaan|amstelland|gooise meren|wijk bij duurstede|bunnik|de bilt|zeewolde|
harlingen|terschelling|ameland|vlieland|schiermonnikoog|goeree|overflakkee|tholen|
sluis|hulst|kapelle|reimerswaal|borsele|veere|schouwen|duiveland"""

RE_CITY = re.compile(r'(?<![a-z])(' + NL_CITIES.replace('\n', '') + r')(?![a-z])')
RE_PROV = re.compile(r'(?<![a-z])(' + NL_PROVINCES.replace('\n', '') + r')(?![a-z])')
RE_GEMEENTE = re.compile(r'gemeente\s+\w')
# an area bigger than one town, even when a town is named inside it
RE_AREA = re.compile(r'\bregio\b|\bregio\s|\bomgeving\b|omstreken|\bstreek\b|\blokaal\b|\blokale\b|regionaal|regionale|in de buurt|\bdorp\b|\bgemeentes?\b|gemeenten')
RE_NL_ALL = re.compile(r'heel nederland|landelijk|(?<!inter)nationaal|\bnational\b|door heel nederland|in nederland|van nederland|\bnederland\b|nederlandse|the ?netherlands|\bholland\b|\bnl\b')
RE_NEIGHBOUR = re.compile(r'belgi[eë]|belgium|belgische|duitsland|germany|duitse|german|benelux|vlaanderen|flanders|\bdach\b|\bbe\b|grensregio|brussel|antwerpen|gent|leuven|maaseik|hamburg|berlijn|berlin|m[uü]nchen|keulen|d[uü]sseldorf|frankfurt|ruhrgebied')
RE_EUROPE = re.compile(r'europa|\beurope\b|europese|european|\beu\b|west-?europa|scandinavi|europees')
RE_FOREIGN = re.compile(r"(?<![a-z])(portugal|spanje|spain|frankrijk|france|franse|itali[eë]|italy|verenigd koninkrijk|\buk\b|engeland|england|london|londense|verenigde staten|\busa\b|u\.s\.|united states|amerika|america|amerikaanse|new york|canada|australi[eë]|australia|japan|japanse|china|chinese|india|brazili[eë]|mexico|zuid-?afrika|south africa|dubai|verenigde arabische|zwitserland|switzerland|geneve|gen[eè]ve|oostenrijk|austria|zweden|sweden|noorwegen|norway|denemarken|denmark|finland|polen|poland|polish|tsjechi[eë]|hongarije|griekenland|greece|turkije|turkey|isra[eë]l|singapore|hong ?kong|korea|taiwan|taiwanese|indonesi[eë]|thailand|vietnam|marokko|cura[cç]ao|aruba|suriname|antillen|kenia|tanzania|ghana|nigeria|afrika|africa|asia ?pacific|apac|latijns-?amerika|midden-?oosten|middle east|antarctica|arctic)(?![a-z])")
RE_GLOBAL = re.compile(r'wereldwijd|worldwide|global|internationaal|internationale|international|over de hele wereld|meerdere landen|verschillende landen|\d+ landen|cross-?border|multi-?country|\bwereld\b')

def map_geo(s):
    cities = {m.group(1) for m in RE_CITY.finditer(s)}
    has_prov = RE_PROV.search(s)
    if RE_FOREIGN.search(s):
        return 'Specifiek buitenland', 'named non-neighbour foreign market'
    if RE_EUROPE.search(s):
        return 'Europa', 'Europe as the market'
    if RE_NEIGHBOUR.search(s):
        return 'Nederland plus buurlanden', 'NL together with / into BE-DE-Benelux'
    if RE_GEMEENTE.search(s):
        return 'Nederlandse stad of plaats', 'a named gemeente is one place'
    if RE_AREA.search(s):
        return 'Regionaal (binnen Nederland)', 'an area, not one town'
    if len(cities) >= 2:
        return 'Regionaal (binnen Nederland)', 'several towns named'
    if cities and not RE_NL_ALL.search(s):
        return 'Nederlandse stad of plaats', 'one named Dutch place'
    if has_prov:
        return 'Regionaal (binnen Nederland)', 'Dutch area bigger than one town'
    if RE_NL_ALL.search(s):
        if cities:
            return 'Nederlandse stad of plaats', 'named Dutch place'
        return 'Heel Nederland (landelijk)', 'the whole country as the market'
    if RE_GLOBAL.search(s):
        return 'Internationaal / wereldwijd', 'unspecified multi-country scope'
    return None, ''

# ------------------------------------------------------------ generic scorer
COMPILED = {}
for _axis, _spec in (('clients_business', IND), ('what_they_sell', CRAFT),
                     ('problem_they_fix', JOB), ('platform_or_channel', CHAN)):
    COMPILED[_axis] = [(b, w, re.compile(p)) for b, pats in _spec.items()
                       for w, p in pats]

def score_axis(axis, s):
    """-> (bucket or None, note). None means 'hand it to the tail pass'."""
    best = {}
    for b, w, rx in COMPILED[axis]:
        m = rx.search(s)
        if not m:
            continue
        cur = best.get(b)
        if cur is None or w > cur[0]:
            best[b] = (w, m.start())
    if not best:
        return None, 'no keyword matched'
    top = max(w for w, _ in best.values())
    tied = [(pos, b) for b, (w, pos) in best.items() if w == top]
    if len(tied) == 1:
        return tied[0][1], f'single winner (weight {top})'
    if axis == 'platform_or_channel' and len(tied) >= 3:
        return 'Multi-channel & omnichannel', f'{len(tied)} buckets named, none primary'
    if axis == 'problem_they_fix':
        return None, f'{len(tied)} buckets tied'
    tied.sort()
    return tied[0][1], f'{len(tied)} tied, first mentioned wins'

def map_value(axis, raw):
    s = (raw or '').lower().strip()
    if not s:
        return None, 'empty'
    if axis == 'clients_money_model':
        return map_model(s)
    if axis == 'clients_size':
        return map_stage(s)
    if axis == 'where_clients_are':
        return map_geo(s)
    return score_axis(axis, s)
