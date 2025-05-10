"""
Therapist contacts module for suggesting professional mental health resources.
"""

import re
import random

# Patterns to identify therapist contact requests
THERAPIST_REQUEST_PATTERNS = [
    r"(?:find|get|suggest|recommend|give|show|need|want|looking for) (?:a|some|) (?:therapist|psychologist|psychiatrist|counselor|counsellor|mental health professional|mental health provider|mental health specialist)",
    r"(?:find|get|suggest|recommend|give|show|need|want|looking for) (?:therapy|counseling|counselling|psychiatric|psychological|mental health) (?:services|help|support|resources|options|consultation|consultancy|treatment)",
    r"(?:where|how) (?:can|do) (?:i|one|you|we) (?:find|get|seek|access) (?:a|some|) (?:therapist|psychologist|psychiatrist|counselor|counsellor|mental health professional|mental health provider|mental health specialist)",
    r"(?:where|how) (?:can|do) (?:i|one|you|we) (?:find|get|seek|access) (?:therapy|counseling|counselling|psychiatric|psychological|mental health) (?:services|help|support|resources|options|consultation|consultancy|treatment)",
    r"(?:need|want|looking for) (?:professional|medical|clinical) (?:help|support|advice|guidance|assistance|consultation|consultancy) (?:for|with) (?:my|) (?:mental health|depression|anxiety|stress|trauma|grief|addiction|eating disorder|ocd|bipolar|schizophrenia|ptsd|mental illness)",
    r"(?:recommend|suggest) (?:a|some|) (?:good|great|excellent|best|top|reliable|trusted|experienced|qualified|licensed|certified|professional) (?:therapist|psychologist|psychiatrist|counselor|counsellor|mental health professional|mental health provider|mental health specialist)",
    r"(?:wellness|therapy|counseling|counselling|mental health) (?:center|centre|clinic|practice|office|facility|provider|service)",
    r"(?:in-person|online|virtual|remote|telehealth|video) (?:therapy|counseling|counselling|psychiatric|psychological|mental health) (?:services|help|support|resources|options|consultation|consultancy|treatment)",
    r"(?:therapist|psychologist|psychiatrist|counselor|counsellor|mental health professional|mental health provider|mental health specialist) (?:near|around|in|close to) (?:me|my area|my location)",
    r"(?:how|where) (?:to|can i|do i|should i) (?:find|get|seek|access) (?:help|support|treatment) (?:for|with) (?:my|) (?:mental health|depression|anxiety|stress|trauma|grief|addiction|eating disorder|ocd|bipolar|schizophrenia|ptsd|mental illness)",
    r"(?:can you|could you|would you) (?:recommend|suggest|provide|give me|share|tell me about) (?:some|any|a few|) (?:therapist|psychologist|psychiatrist|counselor|counsellor|mental health professional|mental health provider|mental health specialist)(?:s|)",
    r"(?:can you|could you|would you) (?:recommend|suggest|provide|give me|share|tell me about) (?:some|any|a few|) (?:wellness center|therapy center|counseling center|mental health center|mental health clinic|psychological service)(?:s|)"
]

# List of therapist contacts with detailed information
THERAPIST_CONTACTS = [
    {
        "name": "Dr. Jennifer Reynolds",
        "title": "Licensed Clinical Psychologist, Ph.D.",
        "specialties": ["Anxiety Disorders", "Depression", "Trauma Recovery", "PTSD", "Stress Management"],
        "approach": "Cognitive Behavioral Therapy (CBT), EMDR, Mindfulness-Based Cognitive Therapy",
        "contact": {
            "phone": "(212) 555-7890",
            "email": "dr.reynolds@mindfulhealingcenter.com",
            "website": "www.mindfulhealingcenter.com/dr-reynolds"
        },
        "practice": {
            "name": "Mindful Healing Center",
            "address": "1270 Avenue of the Americas, Suite 1505, New York, NY 10020",
            "online": True
        },
        "insurance": "In-network with Blue Cross Blue Shield, Aetna, United Healthcare, Cigna; Out-of-network benefits available",
        "languages": ["English", "French"],
        "education": "Ph.D. Clinical Psychology, Columbia University; Postdoctoral Fellowship, NYU Langone Medical Center",
        "years_experience": 15,
        "session_format": "Individual therapy (50 min), Extended sessions (80 min), Group therapy",
        "session_cost": "$200-250 (individual), sliding scale available"
    },
    {
        "name": "Dr. Marcus Chen, M.D.",
        "title": "Board-Certified Psychiatrist",
        "specialties": ["Medication Management", "Treatment-Resistant Depression", "Bipolar Disorder", "Anxiety Disorders", "ADHD"],
        "approach": "Integrative Psychiatry, Psychopharmacology, Supportive Psychotherapy, TMS Therapy",
        "contact": {
            "phone": "(415) 555-3421",
            "email": "dr.chen@bayareapsychiatry.com",
            "website": "www.bayareapsychiatry.com"
        },
        "practice": {
            "name": "Bay Area Psychiatric Associates",
            "address": "450 Sutter Street, Suite 840, San Francisco, CA 94108",
            "online": True
        },
        "insurance": "In-network with Anthem Blue Cross, Cigna, Aetna; Medicare accepted",
        "languages": ["English", "Mandarin", "Cantonese"],
        "education": "M.D. Stanford University School of Medicine; Residency, UCSF Medical Center",
        "years_experience": 12,
        "session_format": "Psychiatric evaluation (60 min), Medication follow-up (30 min)",
        "session_cost": "$350 (initial evaluation), $175 (follow-up)"
    },
    {
        "name": "Sophia Rodriguez, LMFT",
        "title": "Licensed Marriage and Family Therapist",
        "specialties": ["Couples Therapy", "Relationship Issues", "Premarital Counseling", "Divorce Recovery", "Family Systems"],
        "approach": "Emotionally Focused Therapy (EFT), Gottman Method (Level 3 Trained), Attachment-Based Therapy",
        "contact": {
            "phone": "(310) 555-9876",
            "email": "sophia@relationshiprenewal.com",
            "website": "www.relationshiprenewal.com"
        },
        "practice": {
            "name": "Relationship Renewal Center",
            "address": "11500 W. Olympic Blvd, Suite 400, Los Angeles, CA 90064",
            "online": True
        },
        "insurance": "Out-of-network provider, superbills provided for reimbursement, sliding scale available",
        "languages": ["English", "Spanish"],
        "education": "M.A. in Clinical Psychology, Pepperdine University; Certified EFT Therapist",
        "years_experience": 9,
        "session_format": "Couples sessions (80 min), Individual sessions (50 min), Intensive couples retreats",
        "session_cost": "$225 (couples), $175 (individual)"
    },
    {
        "name": "Dr. Jamal Washington",
        "title": "Clinical Psychologist, Addiction Specialist",
        "specialties": ["Substance Use Disorders", "Alcohol Addiction", "Dual Diagnosis", "Recovery Maintenance", "Process Addictions"],
        "approach": "Motivational Interviewing, CBT for Addiction, Harm Reduction, Relapse Prevention, 12-Step Facilitation",
        "contact": {
            "phone": "(312) 555-4567",
            "email": "dr.washington@recoverypathways.org",
            "website": "www.recoverypathways.org"
        },
        "practice": {
            "name": "Recovery Pathways Institute",
            "address": "211 E. Ontario Street, Suite 1100, Chicago, IL 60611",
            "online": True
        },
        "insurance": "In-network with Blue Cross Blue Shield, Cigna, Humana, Magellan",
        "languages": ["English"],
        "education": "Psy.D. Clinical Psychology, Chicago School of Professional Psychology; Certified Addiction Professional",
        "years_experience": 18,
        "session_format": "Individual therapy (50 min), Intensive outpatient program, Group therapy",
        "session_cost": "$185 (individual), Insurance copay varies"
    },
    {
        "name": "Dr. Priya Sharma",
        "title": "Neuropsychologist & Clinical Psychologist",
        "specialties": ["Neuropsychological Assessment", "ADHD", "Learning Disabilities", "Cognitive Rehabilitation", "Executive Functioning"],
        "approach": "Comprehensive Neuropsychological Testing, Evidence-Based Interventions, Cognitive-Behavioral Therapy",
        "contact": {
            "phone": "(617) 555-2345",
            "email": "dr.sharma@cognitivehealthpartners.com",
            "website": "www.cognitivehealthpartners.com"
        },
        "practice": {
            "name": "Cognitive Health Partners",
            "address": "1330 Boylston Street, Suite 500, Boston, MA 02215",
            "online": False
        },
        "insurance": "In-network with Blue Cross Blue Shield, Harvard Pilgrim, Tufts; Out-of-network benefits available",
        "languages": ["English", "Hindi", "Punjabi"],
        "education": "Ph.D. Clinical Psychology, Boston University; Fellowship in Neuropsychology, Massachusetts General Hospital",
        "years_experience": 14,
        "session_format": "Comprehensive neuropsychological assessment (6-8 hours), Feedback sessions (60 min), Therapy sessions (45 min)",
        "session_cost": "$2,800-3,500 (full assessment), $200 (therapy session)"
    },
    {
        "name": "David Kim, LCSW",
        "title": "Licensed Clinical Social Worker, Trauma Specialist",
        "specialties": ["Complex Trauma", "PTSD", "Grief and Loss", "Cultural Identity", "Intergenerational Trauma"],
        "approach": "EMDR, Somatic Experiencing, Internal Family Systems, Trauma-Focused CBT, Culturally-Responsive Care",
        "contact": {
            "phone": "(206) 555-7654",
            "email": "david@healingpathways.net",
            "website": "www.healingpathways.net"
        },
        "practice": {
            "name": "Healing Pathways Trauma Center",
            "address": "1700 7th Avenue, Suite 2100, Seattle, WA 98101",
            "online": True
        },
        "insurance": "In-network with Premera, Regence, Kaiser Permanente; Sliding scale available",
        "languages": ["English", "Korean"],
        "education": "MSW, University of Washington; Certified EMDR Therapist; Somatic Experiencing Practitioner",
        "years_experience": 11,
        "session_format": "Individual therapy (50 min), EMDR sessions (80 min), Group therapy",
        "session_cost": "$150-180 (individual), sliding scale $90-140"
    },
    {
        "name": "Dr. Gabriela Morales",
        "title": "Child & Adolescent Psychologist",
        "specialties": ["Child Development", "Adolescent Mental Health", "Anxiety in Children", "Behavioral Issues", "Parenting Support"],
        "approach": "Play Therapy, Cognitive-Behavioral Therapy for Children, Parent-Child Interaction Therapy, Family Systems",
        "contact": {
            "phone": "(303) 555-8765",
            "email": "dr.morales@growingminds.org",
            "website": "www.growingminds.org"
        },
        "practice": {
            "name": "Growing Minds Child Psychology Center",
            "address": "950 S. Cherry Street, Suite 1030, Denver, CO 80246",
            "online": True
        },
        "insurance": "In-network with Anthem Blue Cross, United Healthcare, Aetna, Cigna",
        "languages": ["English", "Spanish"],
        "education": "Ph.D. Child Clinical Psychology, University of Denver; Internship, Children's Hospital Colorado",
        "years_experience": 13,
        "session_format": "Child therapy (45 min), Parent consultations (50 min), Family sessions (60 min)",
        "session_cost": "$175 (individual), $200 (family)"
    },
    {
        "name": "Dr. Richard Thompson",
        "title": "Geriatric Psychiatrist & Neuropsychiatrist",
        "specialties": ["Geriatric Mental Health", "Neurocognitive Disorders", "Late-life Depression", "Anxiety in Older Adults", "Caregiver Support"],
        "approach": "Integrative Geriatric Psychiatry, Medication Management, Supportive Therapy, Family Consultation",
        "contact": {
            "phone": "(404) 555-3210",
            "email": "dr.thompson@seniorwellnessclinic.com",
            "website": "www.seniorwellnessclinic.com"
        },
        "practice": {
            "name": "Senior Wellness Psychiatric Clinic",
            "address": "2200 Peachtree Road NW, Suite 250, Atlanta, GA 30309",
            "online": True
        },
        "insurance": "Medicare, Aetna Medicare, Humana Medicare, Blue Cross Blue Shield Medicare Advantage",
        "languages": ["English"],
        "education": "M.D. Emory University School of Medicine; Fellowship in Geriatric Psychiatry, Johns Hopkins",
        "years_experience": 25,
        "session_format": "Psychiatric evaluation (60 min), Medication management (30 min), Family consultations (45 min)",
        "session_cost": "Medicare rates, most patients pay only copay with accepted insurance"
    },
    {
        "name": "Zara Jackson, LPC",
        "title": "Licensed Professional Counselor, Women's Health Specialist",
        "specialties": ["Women's Mental Health", "Reproductive Mental Health", "Trauma Recovery", "Racial Identity", "Self-Esteem"],
        "approach": "Feminist Therapy, Trauma-Informed Care, Strengths-Based Approach, Mindfulness, ACT",
        "contact": {
            "phone": "(713) 555-9087",
            "email": "zara@womenshealingcollective.com",
            "website": "www.womenshealingcollective.com"
        },
        "practice": {
            "name": "Women's Healing Collective",
            "address": "3700 Buffalo Speedway, Suite 600, Houston, TX 77098",
            "online": True
        },
        "insurance": "Out-of-network provider, superbills provided, sliding scale available",
        "languages": ["English"],
        "education": "M.A. Clinical Mental Health Counseling, University of Houston; Certified in Perinatal Mental Health",
        "years_experience": 8,
        "session_format": "Individual therapy (50 min), Women's support groups, Workshops",
        "session_cost": "$165 (individual), sliding scale $95-145, group rates vary"
    },
    {
        "name": "Dr. Noah Goldstein",
        "title": "Clinical Psychologist, Anxiety & OCD Specialist",
        "specialties": ["OCD", "Panic Disorder", "Social Anxiety", "Phobias", "Generalized Anxiety Disorder"],
        "approach": "Exposure and Response Prevention (ERP), Acceptance and Commitment Therapy (ACT), Cognitive-Behavioral Therapy",
        "contact": {
            "phone": "(215) 555-6543",
            "email": "dr.goldstein@anxietyspecialists.com",
            "website": "www.anxietyspecialists.com"
        },
        "practice": {
            "name": "Anxiety Treatment Center of Philadelphia",
            "address": "1845 Walnut Street, Suite 1300, Philadelphia, PA 19103",
            "online": True
        },
        "insurance": "In-network with Independence Blue Cross, Aetna, Cigna, United Healthcare",
        "languages": ["English", "Hebrew"],
        "education": "Psy.D. Clinical Psychology, Widener University; OCD Foundation Behavior Therapy Training Institute Graduate",
        "years_experience": 16,
        "session_format": "Individual therapy (50 min), Intensive outpatient treatment, Group therapy",
        "session_cost": "$190 (individual), Insurance copay varies"
    }
]

# Additional resources for mental health support
ADDITIONAL_RESOURCES = {
    "crisis_lines": [
        {
            "name": "988 Suicide & Crisis Lifeline",
            "contact": "Call or text 988",
            "website": "988lifeline.org",
            "hours": "24/7"
        },
        {
            "name": "Crisis Text Line",
            "contact": "Text HOME to 741741",
            "website": "crisistextline.org",
            "hours": "24/7"
        },
        {
            "name": "SAMHSA's National Helpline",
            "contact": "1-800-662-HELP (4357)",
            "website": "samhsa.gov/find-help/national-helpline",
            "hours": "24/7"
        },
        {
            "name": "Veterans Crisis Line",
            "contact": "Call 988, then press 1, or text 838255",
            "website": "veteranscrisisline.net",
            "hours": "24/7"
        },
        {
            "name": "Trevor Project (LGBTQ+ Youth)",
            "contact": "1-866-488-7386 or text START to 678678",
            "website": "thetrevorproject.org",
            "hours": "24/7"
        }
    ],
    "online_directories": [
        {
            "name": "Psychology Today Therapist Directory",
            "website": "psychologytoday.com/us/therapists",
            "description": "Comprehensive database of therapists searchable by location, specialty, insurance, and more."
        },
        {
            "name": "Therapy for Black Girls Directory",
            "website": "therapyforblackgirls.com/therapist-directory",
            "description": "Find culturally competent therapists for Black women and girls."
        },
        {
            "name": "Inclusive Therapists",
            "website": "inclusivetherapists.com",
            "description": "Directory focused on culturally responsive, social justice-oriented care."
        },
        {
            "name": "Asian Mental Health Collective",
            "website": "asianmhc.org/therapist-directory",
            "description": "Directory of AAPI therapists and therapists experienced in AAPI issues."
        },
        {
            "name": "National Queer and Trans Therapists of Color Network",
            "website": "nqttcn.com/directory",
            "description": "Directory of queer and trans therapists of color."
        },
        {
            "name": "Open Path Psychotherapy Collective",
            "website": "openpathcollective.org",
            "description": "Affordable therapy options ($30-60 per session) for individuals, couples, and families."
        }
    ],
    "telehealth_platforms": [
        {
            "name": "BetterHelp",
            "website": "betterhelp.com",
            "description": "Online counseling platform with over 25,000 licensed therapists, starting at $60-$90 per week."
        },
        {
            "name": "Talkspace",
            "website": "talkspace.com",
            "description": "Text, audio, and video therapy with licensed providers, starting at $69 per week."
        },
        {
            "name": "Alma",
            "website": "helloalma.com",
            "description": "Network of therapists with in-person and virtual options, many accepting insurance."
        },
        {
            "name": "Cerebral",
            "website": "cerebral.com",
            "description": "Online mental health care with therapy and medication management options."
        },
        {
            "name": "Headway",
            "website": "headway.co",
            "description": "Platform connecting patients with therapists who accept insurance, with transparent pricing."
        }
    ],
    "specialized_resources": [
        {
            "name": "National Alliance on Mental Illness (NAMI)",
            "website": "nami.org",
            "description": "Advocacy, education, support and public awareness for individuals and families affected by mental illness."
        },
        {
            "name": "Mental Health America",
            "website": "mhanational.org",
            "description": "Community-based nonprofit offering resources, tools, and support for mental health."
        },
        {
            "name": "Anxiety and Depression Association of America",
            "website": "adaa.org",
            "description": "Information, resources, and support for anxiety, depression, and related disorders."
        },
        {
            "name": "Postpartum Support International",
            "website": "postpartum.net",
            "description": "Resources for pregnancy and postpartum mental health, including a helpline: 1-800-944-4773."
        },
        {
            "name": "International OCD Foundation",
            "website": "iocdf.org",
            "description": "Resources, support groups, and treatment provider directory for OCD and related disorders."
        }
    ]
}

def detect_therapist_request(text):
    """
    Detect if the text contains a request for therapist contacts.

    Args:
        text (str): The user's message

    Returns:
        dict: Detection results including matched patterns
    """
    text = text.lower()

    # Check for therapist request patterns
    matches = []
    for pattern in THERAPIST_REQUEST_PATTERNS:
        if re.search(pattern, text):
            matches.append(pattern)

    if not matches:
        return {"is_therapist_request": False}

    return {
        "is_therapist_request": True,
        "matches": matches
    }

def get_therapist_recommendations(num_recommendations=3):
    """
    Get therapist recommendations.

    Args:
        num_recommendations (int): Number of therapist contacts to recommend

    Returns:
        list: List of recommended therapist contacts
    """
    # Ensure we don't recommend more therapists than we have
    num_recommendations = min(num_recommendations, len(THERAPIST_CONTACTS))

    # Randomly select therapists without replacement
    recommended_therapists = random.sample(THERAPIST_CONTACTS, num_recommendations)

    return recommended_therapists

def format_therapist_recommendations(therapists, include_additional_resources=True):
    """
    Format therapist recommendations into a user-friendly response.

    Args:
        therapists (list): List of therapist contacts to format
        include_additional_resources (bool): Whether to include additional resources

    Returns:
        str: Formatted response with therapist recommendations
    """
    response = "# Mental Health Professional Recommendations\n\n"
    response += "Here are some therapists who might be able to help you:\n\n"

    for i, therapist in enumerate(therapists, 1):
        response += f"## {i}. {therapist['name']}, {therapist['title']}\n\n"
        response += f"**Specialties**: {', '.join(therapist['specialties'])}\n\n"
        response += f"**Approach**: {therapist['approach']}\n\n"
        response += f"**Education**: {therapist['education']}\n\n"
        response += f"**Years of Experience**: {therapist['years_experience']}\n\n"
        response += f"**Practice**: {therapist['practice']['name']}, {therapist['practice']['address']}\n\n"

        if therapist['practice']['online']:
            response += "**Offers virtual/online sessions**: Yes\n\n"

        response += f"**Session Format**: {therapist['session_format']}\n\n"
        response += f"**Session Cost**: {therapist['session_cost']}\n\n"

        response += f"**Contact**:\n"
        response += f"- Phone: {therapist['contact']['phone']}\n"
        response += f"- Email: {therapist['contact']['email']}\n"
        response += f"- Website: {therapist['contact']['website']}\n\n"

        response += f"**Insurance**: {therapist['insurance']}\n\n"
        response += f"**Languages**: {', '.join(therapist['languages'])}\n\n"

    if include_additional_resources:
        response += "## Additional Resources\n\n"

        response += "### Crisis Support (Available 24/7)\n\n"
        for resource in ADDITIONAL_RESOURCES["crisis_lines"]:
            response += f"- **{resource['name']}**: {resource['contact']} | {resource['website']}\n"

        response += "\n### Find More Therapists\n\n"
        for directory in ADDITIONAL_RESOURCES["online_directories"]:
            response += f"- **{directory['name']}**: {directory['website']}\n"

        response += "\n### Online Therapy Platforms\n\n"
        for platform in ADDITIONAL_RESOURCES["telehealth_platforms"]:
            response += f"- **{platform['name']}**: {platform['website']}\n"

        response += "\n### Specialized Mental Health Resources\n\n"
        for resource in ADDITIONAL_RESOURCES["specialized_resources"]:
            response += f"- **{resource['name']}**: {resource['website']} - {resource['description']}\n"

    response += "\n*Contact these professionals directly to confirm their current availability, fees, and whether they're accepting new clients.*"

    return response

def process_therapist_request(text):
    """
    Process text to detect therapist requests and generate recommendations.

    Args:
        text (str): The user's message

    Returns:
        dict: Processing results including detection and response
    """
    request_info = detect_therapist_request(text)

    if not request_info.get("is_therapist_request", False):
        return {"is_therapist_request": False}

    # Get 3 random therapist recommendations
    recommended_therapists = get_therapist_recommendations(3)
    response = format_therapist_recommendations(recommended_therapists)

    return {
        "is_therapist_request": True,
        "recommended_therapists": recommended_therapists,
        "response": response
    }
