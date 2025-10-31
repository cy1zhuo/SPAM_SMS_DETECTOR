"""
Spam detection patterns for the SMS spam detection system.
These patterns are used as fallback when the machine learning model is not available.
"""

# High-confidence spam indicators
SPAM_INDICATORS = [
    # Financial amounts and currency
    r'(?i)(?:₱|php|peso)s?\s*\d{3,}(?:[,\s]?\d{3})*(?:\.\d{1,2})?',
    
    # Urgency and pressure tactics
    r'(?i)\b(?:urgent!?|immediate(?:ly)?!?|last\s*chance|limited\s*time|expiring\s*soon|act\s*now|hurry!?|asap|rush|emergency|alert!?|deadline|ending\s*soon)\b',
    
    # Financial offers and scams
    r'(?i)\b(?:loan|credit|debt|investment|money\s*making|earn\s*[₱$]|double\s*your\s*money|get\s*rich|quick\s*cash|financial\s*freedom|debt\s*relief)\b',
    
    # Common spam CTAs and phrases
    r'(?i)\b(?:click\s*(?:here|now|link)|verify\s*(?:now|account|details)|call\s*(?:now|us|me)\s*[0-9-]{8,}|text\s*(?:now|us|me))\b',
    r'(?i)\b(?:order|buy|shop|apply|start|try|get|sign\s*up|register|join|enroll|subscribe|download|install|update|renew|reactivate|upgrade|claim)\s*now\b',
    
    # Suspicious URLs and domains
    r'(?i)(?:https?:\/\/|www\.|bit\.ly|goo\.gl|tinyurl\.com|t\.co|ow\.ly|is\.gd|v\.gd|cli\.gs|tr\.im|adf\.ly|bc\.vc|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|prettylinkpro\.com|viralurl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net|ph\/|ph-|ph_|ph\.|ph\d|ph\s|ph$|smartp\.bond|gcash-?verify|bpi-?verify|invest-?fast|phlpost-?update|gcash-?secure)[^\s\.]+\.[^\s]{2,}',
    
    # Commercial and promotional content
    r'(?i)\b(?:promo|discount|voucher|coupon|deal|offer|sale|clearance|rebate|reward|bonus|incentive|commission|free\s*(?:delivery|shipping|installment|trial)|limited\s*(?:offer|time|stock|edition)|while\s*(?:supplies|stocks)\s*last)\b',
    
    # Common spam patterns
    r'(?i)\b(?:congrat(?:ulation)?s?[!?]|won!?|winner!?|prize!?|claim\s*(?:now|your)|free\s*(?:money|gift|prize|phone))\b'
]

# Safe message indicators
SAFE_INDICATORS = [
    # Personal communications
    r'(?i)\b(?:hi\b|hello\b|hey\b|thanks\b|thank you\b|please\b|mom\b|dad\b|ate\b|kuya\b|sir\b|ma\'am\b)\b',
    
    # Common in legitimate notifications
    r'(?i)\b(?:your\s+order|delivered|received|payment\s+of|receipt|confirmation|reference\s+number|tracking\s+number)\b',
    
    # Common personal phrases
    r'(?i)\b(?:can you\b|could you\b|would you\b|will you\b|let me know\b|get back to you\b|talk to you\b)\b'
]

# Categories for better classification
MESSAGE_CATEGORIES = {
    'financial': [
        r'\b(?:loan|credit|debt|refinance|mortgage|payday|investment|stock|trading|bitcoin|crypto|forex|binary|option|trading|stock|share|market|fund|money|cash|dollar|euro|pound|peso|php|usd|gbp|eur|income|revenue|profit|rich|wealth|million|billion)\b'
    ],
    'phishing': [
        r'\b(?:verify|confirm|update|account|login|password|username|id|pin|ssn|social security|credit card|bank account|gcash|paymaya|bpi|bdo|metrobank|security code|verification code|otp|one time password)\b'
    ],
    'scam': [
        r'\b(?:scam|fraud|fake|phishing|hack|hacked|compromise|stolen|breach|leak|leaked|exposed|expose|steal|stealing|stole|stolen|hijack|hijacked|malware|virus|trojan|ransomware|spyware|adware|keylogger|rootkit|backdoor|exploit|vulnerability|patch|update|upgrade|security|privacy|secure|protect|protection|safe|safety|trust|trusted|verified|legit|legitimate|official|real|genuine|authentic|authorized|certified|licensed|registered|guaranteed|warranty|warrantied|money back|refund|return|exchange|replacement)\b'
    ]
}

# Safe message indicators
SAFE_INDICATORS = [
    # Common in personal messages
    r'\b(?:hi\b|hello\b|hey\b|thanks\b|thank you\b|please\b|can you\b|could you\b|would you\b|will you\b|mom\b|dad\b|ate\b|kuya\b|sir\b|ma\'am\b|miss\b|mister\b|mr\.?\b|mrs\.?\b|ms\.?\b|dr\.?\b|prof\.?\b|atty\.?\b)\b',
    
    # Common in legitimate notifications
    r'\b(?:your\s+order|delivered|received|payment\s+of|receipt|confirmation|reference\s+number|tracking\s+number|order\s+number|transaction\s+id|transaction\s+number|transaction\s+reference)\b',
    
    # Common in personal transactions
    r'\b(?:lunch|dinner|breakfast|merienda|snack|food|eat|restaurant|cafe|karinderya|carinderia|kainan|tambayan|tambay|grocery|groceries|shopping|market|palengke|mall|department store|supermarket|convenience store|sari-sari store|tindahan|bakery|bakeshop|baker|baker\'s|bakeries|bakerys|bakeryshop|bakeryshops|bakery shop|bakery shops|bakery store|bakery stores|bakery outlet|bakery outlets|bakery house|bakery houses|bakery cafe|bakery cafes|bakery restaurant|bakery restaurants|bakery bakeshop|bakery bakeshops|bakery and cafe|bakery and cafes|bakery and restaurant|bakery and restaurants|bakery and bakeshop|bakery and bakeshops|bakery, cafe|bakery, cafes|bakery, restaurant|bakery, restaurants|bakery, bakeshop|bakery, bakeshops|bakery & cafe|bakery & cafes|bakery & restaurant|bakery & restaurants|bakery & bakeshop|bakery & bakeshops|bakery/cafe|bakery/restaurant|bakery/bakeshop|bakery\s*[&, ]\s*cafe|bakery\s*[&, ]\s*restaurant|bakery\s*[&, ]\s*bakeshop)\b'
]

# Categories for better classification
MESSAGE_CATEGORIES = {
    'financial': [
        r'\b(?:loan|credit|debt|refinance|mortgage|payday|investment|stock|trading|bitcoin|crypto|forex|binary|option|trading|stock|share|market|fund|money|cash|dollar|euro|pound|peso|php|usd|gbp|eur|income|revenue|profit|rich|wealth|million|billion)\b'
    ],
    'phishing': [
        r'\b(?:verify|confirm|update|account|login|password|username|id|pin|ssn|social security|credit card|bank account|gcash|paymaya|bpi|bdo|metrobank|security code|verification code|otp|one time password)\b'
    ],
    'scam': [
        r'\b(?:scam|fraud|fake|phishing|hack|hacked|compromise|stolen|breach|leak|leaked|exposed|expose|steal|stealing|stole|stolen|hijack|hijacked|malware|virus|trojan|ransomware|spyware|adware|keylogger|rootkit|backdoor|exploit|vulnerability|patch|update|upgrade|security|privacy|secure|protect|protection|safe|safety|trust|trusted|verified|legit|legitimate|official|real|genuine|authentic|authorized|certified|licensed|registered|guaranteed|warranty|warrantied|money back|refund|return|exchange|replacement)\b'
    ],
    'commercial': [
        r'\b(?:commercial\s*(?:lot|property|space|unit|area|estate|building|development)|sqm?\b|sq\.?\s*m|square\s*meter|price\s*range|per\s*sqm?|pre-?selling|master-?planned|CBD|commercial\s*district|lot\s*size|floor\s*area|FAR|floor\s*area\s*ratio|commercial\s*space|for\s*lease|for\s*rent|for\s*sale|leasing|investment\s*property|real\s*estate|property\s*investment)\b',
        r'\b(?:estate\s*lot|residential\s*lot|housing\s*project|condo|condominium|townhouse|house\s*and\s*lot|house\s*for\s*sale|house\s*for\s*rent|apartment|apartment\s*for\s*rent|apartment\s*for\s*sale|commercial\s*space|office\s*space|retail\s*space|warehouse|industrial\s*space|industrial\s*lot|industrial\s*estate|industrial\s*park|business\s*park|IT\s*park|technology\s*park|science\s*park|eco-?park|eco-?zone|special\s*economic\s*zone|PEZA|economic\s*zone|freeport|freeport\s*zone|tourism\s*estate|tourism\s*zone|tourism\s*park|tourism\s*area|tourism\s*destination|tourism\s*spot|tourism\s*circuit|tourism\s*circuit\s*area|tourism\s*circuit\s*zone|tourism\s*circuit\s*park|tourism\s*circuit\s*estate|tourism\s*circuit\s*project|tourism\s*circuit\s*development|tourism\s*circuit\s*area|tourism\s*circuit\s*zone|tourism\s*circuit\s*park|tourism\s*circuit\s*estate|tourism\s*circuit\s*project|tourism\s*circuit\s*development)\b'
    ],
    'promotional': [
        r'\b(?:promo|promotion|discount|voucher|coupon|deal|offer|bargain|sale|clearance|rebate|reward|bonus|incentive|commission|free\s*delivery|free\s*shipping|free\s*installment|free\s*service|free\s*check-?up|free\s*consultation|free\s*estimate|free\s*quote|free\s*trial|free\s*assessment|free\s*inspection|free\s*evaluation|free\s*appraisal|free\s*diagnostic|free\s*scan|free\s*test|free\s*examination|free\s*check-?up|free\s*consultation|free\s*estimate|free\s*quote|free\s*trial|free\s*assessment|free\s*inspection|free\s*evaluation|free\s*appraisal|free\s*diagnostic|free\s*scan|free\s*test|free\s*examination)\b',
        r'\b(?:limited\s*offer|limited\s*time|limited\s*period|limited\s*stock|limited\s*edition|limited\s*availability|limited\s*seats|limited\s*slots|limited\s*quantities|while\s*supplies\s*last|while\s*stocks\s*last|hurry|rush|urgent|immediate|asap|as\s*soon\s*as\s*possible|don\'t\s*miss|don\'t\s*miss\s*out|don\'t\s*miss\s*this|don\'t\s*miss\s*it|don\'t\s*miss\s*your|don\'t\s*miss\s*this\s*chance|don\'t\s*miss\s*this\s*opportunity|don\'t\s*miss\s*this\s*offer|don\'t\s*miss\s*this\s*deal|don\'t\s*miss\s*this\s*promo|don\'t\s*miss\s*this\s*promotion|don\'t\s*miss\s*this\s*discount|don\'t\s*miss\s*this\s*voucher|don\'t\s*miss\s*this\s*coupon|don\'t\s*miss\s*this\s*bargain|don\'t\s*miss\s*this\s*sale|don\'t\s*miss\s*this\s*clearance|don\'t\s*miss\s*this\s*rebate|don\'t\s*miss\s*this\s*reward|don\'t\s*miss\s*this\s*bonus|don\'t\s*miss\s*this\s*incentive|don\'t\s*miss\s*this\s*commission|don\'t\s*miss\s*this\s*chance\s*to\s*win|don\'t\s*miss\s*this\s*opportunity\s*to\s*win|don\'t\s*miss\s*this\s*offer\s*to\s*win|don\'t\s*miss\s*this\s*deal\s*to\s*win|don\'t\s*miss\s*this\s*promo\s*to\s*win|don\'t\s*miss\s*this\s*promotion\s*to\s*win|don\'t\s*miss\s*this\s*discount\s*to\s*win|don\'t\s*miss\s*this\s*voucher\s*to\s*win|don\'t\s*miss\s*this\s*coupon\s*to\s*win|don\'t\s*miss\s*this\s*bargain\s*to\s*win|don\'t\s*miss\s*this\s*sale\s*to\s*win|don\'t\s*miss\s*this\s*clearance\s*to\s*win|don\'t\s*miss\s*this\s*rebate\s*to\s*win|don\'t\s*miss\s*this\s*reward\s*to\s*win|don\'t\s*miss\s*this\s*bonus\s*to\s*win|don\'t\s*miss\s*this\s*incentive\s*to\s*win|don\'t\s*miss\s*this\s*commission\s*to\s*win)\b'
    ]
}
