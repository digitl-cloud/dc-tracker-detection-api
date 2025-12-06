"""
Tech stack detection patterns.
Enhanced with 2800+ patterns from Ghostery TrackerDB.
"""
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Path to Ghostery patterns data
GHOSTERY_PATTERNS_PATH = Path(__file__).parent.parent.parent / "data" / "ghostery_patterns.json"

TECH_CATEGORIES = {
    "orchestration": {
        "display_name": "Orchestration / Marketing Automation",
        "insider_relevance": "high",
        "template_field": "Orchestration",
        "insider_product": "Architect"
    },
    "ab_testing_personalization": {
        "display_name": "A/B Testing & Personalization",
        "insider_relevance": "high",
        "template_field": "A/B Testing & Personalization",
        "insider_product": "Web Suite"
    },
    "cdp": {
        "display_name": "Customer Data Platform (CDP)",
        "insider_relevance": "high",
        "template_field": "Customer Data Platform (CDP)",
        "insider_product": "CDP"
    },
    "analytics": {
        "display_name": "Analytics",
        "insider_relevance": "medium",
        "template_field": "Analytics"
    },
    "tag_manager": {
        "display_name": "Tag Manager",
        "insider_relevance": "low",
        "template_field": "Tag Manager"
    },
    "chatbot": {
        "display_name": "Chatbot",
        "insider_relevance": "medium",
        "template_field": "Chatbot",
        "insider_product": "Conversational AI"
    },
    "email_marketing": {
        "display_name": "Email Marketing",
        "insider_relevance": "high",
        "template_field": "Others",
        "insider_product": "Email Campaigns"
    },
    "web_push": {
        "display_name": "Web Push",
        "insider_relevance": "high",
        "template_field": "Web Push",
        "insider_product": "Web Push"
    },
    "consent_management": {
        "display_name": "Consent Management",
        "insider_relevance": "low",
        "template_field": "Others"
    },
    "crm": {
        "display_name": "CRM",
        "insider_relevance": "medium",
        "template_field": "CRM"
    },
    "ecommerce_platform": {
        "display_name": "E-Commerce Platform",
        "insider_relevance": "low",
        "template_field": "Website / CMS"
    },
    "advertising": {
        "display_name": "Advertising / Retargeting",
        "insider_relevance": "medium",
        "template_field": "Others",
        "insider_product": "Ad Audiences"
    },
    "search": {
        "display_name": "Site Search",
        "insider_relevance": "medium",
        "template_field": "Others",
        "insider_product": "Eureka"
    },
    "payments": {
        "display_name": "Payments",
        "insider_relevance": "low",
        "template_field": "Others"
    }
}

TECH_PATTERNS = {
    "orchestration": [
        {"name": "Braze", "domains": ["braze.com", "appboycdn.com"], "patterns": ["appboy", "braze.init"], "competitor_priority": "high"},
        {"name": "Klaviyo", "domains": ["klaviyo.com"], "patterns": ["klaviyo", "_learnq"], "competitor_priority": "high"},
        {"name": "Iterable", "domains": ["iterable.com"], "patterns": ["iterable", "_iaq"], "competitor_priority": "high"},
        {"name": "Customer.io", "domains": ["customer.io"], "patterns": ["_cio", "cio.identify"], "competitor_priority": "high"},
        {"name": "Salesforce Marketing Cloud", "domains": ["exacttarget.com"], "patterns": ["exacttarget", "sfmc"], "competitor_priority": "high"},
        {"name": "HubSpot", "domains": ["hubspot.com", "hs-scripts.com"], "patterns": ["hubspot", "_hsq"], "competitor_priority": "medium"},
        {"name": "Emarsys", "domains": ["emarsys.com"], "patterns": ["emarsys", "scarab"], "competitor_priority": "high"},
        {"name": "Mailchimp", "domains": ["mailchimp.com", "chimpstatic.com"], "patterns": ["mailchimp", "mc4wp"], "competitor_priority": "medium"},
        {"name": "ActiveCampaign", "domains": ["activecampaign.com"], "patterns": ["activecampaign", "trackcmp"], "competitor_priority": "medium"},
        {"name": "Marketo", "domains": ["marketo.com", "mktoresp.com"], "patterns": ["mkto", "munchkin"], "competitor_priority": "medium"},
        {"name": "Moengage", "domains": ["moengage.com"], "patterns": ["moengage"], "competitor_priority": "high"},
        {"name": "CleverTap", "domains": ["clevertap.com", "wzrkt.com"], "patterns": ["clevertap", "wzrkt"], "competitor_priority": "high"},
        {"name": "Insider", "domains": ["useinsider.com", "insnw.net"], "patterns": ["useinsider", "Insider.init"], "competitor_priority": "self"},
    ],
    "ab_testing_personalization": [
        {"name": "Optimizely", "domains": ["optimizely.com"], "patterns": ["optimizely", "window.optimizely"], "competitor_priority": "high"},
        {"name": "VWO", "domains": ["vwo.com", "visualwebsiteoptimizer.com"], "patterns": ["vwo", "_vis_opt"], "competitor_priority": "high"},
        {"name": "AB Tasty", "domains": ["abtasty.com"], "patterns": ["abtasty", "ABTasty"], "competitor_priority": "high"},
        {"name": "Dynamic Yield", "domains": ["dynamicyield.com"], "patterns": ["dynamicyield", "DY.API"], "competitor_priority": "high"},
        {"name": "Monetate", "domains": ["monetate.net"], "patterns": ["monetate"], "competitor_priority": "high"},
        {"name": "Kameleoon", "domains": ["kameleoon.com"], "patterns": ["kameleoon"], "competitor_priority": "high"},
        {"name": "Google Optimize", "domains": ["optimize.google.com"], "patterns": ["google_optimize", "OPT-"], "competitor_priority": "medium"},
        {"name": "Adobe Target", "domains": ["tt.omtrdc.net"], "patterns": ["adobe.target", "mbox", "at.js"], "competitor_priority": "high"},
    ],
    "cdp": [
        {"name": "Segment", "domains": ["segment.com", "segment.io"], "patterns": ["analytics.js", "segment", "analytics.identify"], "competitor_priority": "high"},
        {"name": "mParticle", "domains": ["mparticle.com"], "patterns": ["mparticle", "mParticle"], "competitor_priority": "high"},
        {"name": "Tealium AudienceStream", "domains": ["tealium.com", "tiqcdn.com"], "patterns": ["tealium", "utag", "audiencestream"], "competitor_priority": "high"},
        {"name": "BlueConic", "domains": ["blueconic.com"], "patterns": ["blueconic", "blueConicClient"], "competitor_priority": "high"},
        {"name": "Treasure Data", "domains": ["treasuredata.com"], "patterns": ["treasuredata", "td.js"], "competitor_priority": "medium"},
        {"name": "RudderStack", "domains": ["rudderstack.com"], "patterns": ["rudderanalytics", "rudderstack"], "competitor_priority": "medium"},
    ],
    "analytics": [
        {"name": "Google Analytics 4", "domains": ["google-analytics.com", "googletagmanager.com"], "patterns": ["gtag(", "G-"], "competitor_priority": "low"},
        {"name": "Adobe Analytics", "domains": ["omniture.com", "2o7.net"], "patterns": ["s_code", "AppMeasurement", "s.t()"], "competitor_priority": "medium"},
        {"name": "Mixpanel", "domains": ["mixpanel.com"], "patterns": ["mixpanel", "mixpanel.init"], "competitor_priority": "low"},
        {"name": "Amplitude", "domains": ["amplitude.com"], "patterns": ["amplitude", "amplitude.init"], "competitor_priority": "low"},
        {"name": "Heap", "domains": ["heap.io", "heapanalytics.com"], "patterns": ["heap", "heap.load"], "competitor_priority": "low"},
        {"name": "Hotjar", "domains": ["hotjar.com"], "patterns": ["hotjar", "hj(", "_hjSettings"], "competitor_priority": "low"},
        {"name": "FullStory", "domains": ["fullstory.com"], "patterns": ["fullstory", "FS.identify"], "competitor_priority": "low"},
        {"name": "Contentsquare", "domains": ["contentsquare.com"], "patterns": ["contentsquare", "CS_CONF"], "competitor_priority": "low"},
        {"name": "PostHog", "domains": ["posthog.com"], "patterns": ["posthog", "posthog.init"], "competitor_priority": "low"},
    ],
    "tag_manager": [
        {"name": "Google Tag Manager", "domains": ["googletagmanager.com"], "patterns": ["gtm.js", "GTM-", "dataLayer"], "competitor_priority": "low"},
        {"name": "Tealium iQ", "domains": ["tealium.com", "tiqcdn.com"], "patterns": ["utag.js", "tealium"], "competitor_priority": "low"},
        {"name": "Adobe Launch", "domains": ["adobedtm.com"], "patterns": ["launch-", "satelliteLib"], "competitor_priority": "low"},
    ],
    "chatbot": [
        {"name": "Intercom", "domains": ["intercom.io", "intercomcdn.com"], "patterns": ["intercom", "Intercom("], "competitor_priority": "medium"},
        {"name": "Zendesk Chat", "domains": ["zendesk.com", "zopim.com"], "patterns": ["zendesk", "zopim", "$zopim"], "competitor_priority": "medium"},
        {"name": "Drift", "domains": ["drift.com", "driftt.com"], "patterns": ["drift", "driftt"], "competitor_priority": "medium"},
        {"name": "LiveChat", "domains": ["livechat.com", "livechatinc.com"], "patterns": ["livechat", "__lc"], "competitor_priority": "medium"},
        {"name": "Freshchat", "domains": ["freshchat.com"], "patterns": ["freshchat", "fcWidget"], "competitor_priority": "medium"},
        {"name": "Tidio", "domains": ["tidio.co"], "patterns": ["tidio", "tidioChatCode"], "competitor_priority": "low"},
        {"name": "Tawk.to", "domains": ["tawk.to"], "patterns": ["tawk", "Tawk_API"], "competitor_priority": "low"},
    ],
    "web_push": [
        {"name": "OneSignal", "domains": ["onesignal.com"], "patterns": ["onesignal", "OneSignal.init"], "competitor_priority": "high"},
        {"name": "Pushwoosh", "domains": ["pushwoosh.com"], "patterns": ["pushwoosh", "Pushwoosh"], "competitor_priority": "high"},
        {"name": "PushEngage", "domains": ["pushengage.com"], "patterns": ["pushengage", "_pe"], "competitor_priority": "medium"},
        {"name": "VWO Engage", "domains": ["pushcrew.com"], "patterns": ["pushcrew", "_pcq"], "competitor_priority": "medium"},
    ],
    "consent_management": [
        {"name": "OneTrust", "domains": ["onetrust.com", "cookielaw.org"], "patterns": ["onetrust", "OptanonWrapper"], "competitor_priority": "low"},
        {"name": "Cookiebot", "domains": ["cookiebot.com"], "patterns": ["cookiebot", "Cookiebot"], "competitor_priority": "low"},
        {"name": "Didomi", "domains": ["didomi.io"], "patterns": ["didomi", "Didomi."], "competitor_priority": "low"},
        {"name": "Usercentrics", "domains": ["usercentrics.com"], "patterns": ["usercentrics", "UC_UI"], "competitor_priority": "low"},
    ],
    "ecommerce_platform": [
        {"name": "Shopify", "domains": ["shopify.com", "cdn.shopify.com"], "patterns": ["shopify", "Shopify."], "competitor_priority": "low"},
        {"name": "WooCommerce", "domains": ["woocommerce.com"], "patterns": ["woocommerce", "wc-"], "competitor_priority": "low"},
        {"name": "Magento", "domains": ["magento.com"], "patterns": ["magento", "Mage."], "competitor_priority": "low"},
        {"name": "Salesforce Commerce Cloud", "domains": ["demandware.net"], "patterns": ["demandware", "sfcc"], "competitor_priority": "low"},
        {"name": "VTEX", "domains": ["vtex.com", "vtexassets.com"], "patterns": ["vtex"], "competitor_priority": "low"},
        {"name": "Shopware", "domains": ["shopware.com"], "patterns": ["shopware"], "competitor_priority": "low"},
    ],
    "advertising": [
        {"name": "Google Ads", "domains": ["googleadservices.com"], "patterns": ["googleads", "adsbygoogle"], "competitor_priority": "low"},
        {"name": "Facebook Pixel", "domains": ["facebook.com", "connect.facebook.net"], "patterns": ["fbq(", "fbevents.js"], "competitor_priority": "low"},
        {"name": "TikTok Pixel", "domains": ["tiktok.com", "analytics.tiktok.com"], "patterns": ["ttq.", "tiktok"], "competitor_priority": "low"},
        {"name": "Criteo", "domains": ["criteo.com", "criteo.net"], "patterns": ["criteo", "Criteo"], "competitor_priority": "medium"},
        {"name": "AdRoll", "domains": ["adroll.com"], "patterns": ["adroll", "__adroll"], "competitor_priority": "medium"},
    ],
    "search": [
        {"name": "Algolia", "domains": ["algolia.com", "algolianet.com"], "patterns": ["algolia", "algoliasearch"], "competitor_priority": "medium"},
        {"name": "Searchspring", "domains": ["searchspring.com"], "patterns": ["searchspring"], "competitor_priority": "medium"},
        {"name": "Klevu", "domains": ["klevu.com"], "patterns": ["klevu"], "competitor_priority": "medium"},
        {"name": "Constructor.io", "domains": ["constructor.io"], "patterns": ["constructor.io", "cnstrc"], "competitor_priority": "medium"},
    ],
    "payments": [
        {"name": "Stripe", "domains": ["stripe.com", "js.stripe.com"], "patterns": ["stripe", "Stripe("], "competitor_priority": "low"},
        {"name": "PayPal", "domains": ["paypal.com", "paypalobjects.com"], "patterns": ["paypal", "PayPal"], "competitor_priority": "low"},
        {"name": "Klarna", "domains": ["klarna.com"], "patterns": ["klarna", "Klarna."], "competitor_priority": "low"},
        {"name": "Adyen", "domains": ["adyen.com"], "patterns": ["adyen", "AdyenCheckout"], "competitor_priority": "low"},
    ],
    "crm": [
        {"name": "Salesforce", "domains": ["salesforce.com", "force.com"], "patterns": ["salesforce", "sfdc"], "competitor_priority": "low"},
        {"name": "HubSpot CRM", "domains": ["hubspot.com"], "patterns": ["hubspot", "_hsq"], "competitor_priority": "low"},
        {"name": "Pipedrive", "domains": ["pipedrive.com"], "patterns": ["pipedrive"], "competitor_priority": "low"},
        {"name": "Zoho CRM", "domains": ["zoho.com"], "patterns": ["zoho", "zohocdn"], "competitor_priority": "low"},
    ],
}

# Mapping from Tech Categories to Discovery Template fields
DISCOVERY_TEMPLATE_MAPPING = {
    "Orchestration": ["orchestration"],
    "A/B Testing & Personalization": ["ab_testing_personalization"],
    "Customer Data Platform (CDP)": ["cdp"],
    "Web Push": ["web_push"],
    "Chatbot": ["chatbot"],
    "Website / CMS": ["ecommerce_platform"],
    "CRM": ["crm"],
    "Analytics": ["analytics", "ghostery_analytics"],
    "Tag Manager": ["tag_manager"],
    "Others": ["email_marketing", "consent_management", "advertising", "search", "payments",
               "ghostery_advertising", "ghostery_customer_interaction", "ghostery_consent", "ghostery_social_media"]
}


# Mapping from Ghostery categories to our internal categories
GHOSTERY_CATEGORY_MAPPING = {
    "site_analytics": "ghostery_analytics",
    "advertising": "ghostery_advertising",
    "customer_interaction": "ghostery_customer_interaction",
    "consent": "ghostery_consent",
    "social_media": "ghostery_social_media"
}


def _load_ghostery_patterns() -> dict[str, list[dict]]:
    """
    Load and transform Ghostery patterns into our format.
    Returns dict of category -> list of tool patterns.
    """
    if not GHOSTERY_PATTERNS_PATH.exists():
        logger.warning(f"Ghostery patterns not found at {GHOSTERY_PATTERNS_PATH}")
        return {}

    try:
        with open(GHOSTERY_PATTERNS_PATH, "r") as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load Ghostery patterns: {e}")
        return {}

    # Track names we already have to avoid duplicates
    existing_names = set()
    for category_tools in TECH_PATTERNS.values():
        for tool in category_tools:
            existing_names.add(tool["name"].lower())

    ghostery_patterns: dict[str, list[dict]] = {
        "ghostery_analytics": [],
        "ghostery_advertising": [],
        "ghostery_customer_interaction": [],
        "ghostery_consent": [],
        "ghostery_social_media": []
    }

    patterns = data.get("patterns", [])
    for pattern in patterns:
        name = pattern.get("name")
        ghostery_category = pattern.get("category")
        domains = pattern.get("domains", [])

        if not name or not ghostery_category:
            continue

        # Skip if we already have this tool in our curated list
        if name.lower() in existing_names:
            continue

        # Map to our category
        our_category = GHOSTERY_CATEGORY_MAPPING.get(ghostery_category)
        if not our_category:
            continue

        # Extract patterns from filters (adblock syntax)
        extracted_patterns = []
        for f in pattern.get("filters", []):
            # Extract domain/path from adblock filter syntax
            # Format: ||domain.com/path^$3p or ||domain.com^
            if f.startswith("||"):
                # Remove || prefix and any suffixes
                clean = f[2:].split("^")[0].split("$")[0]
                if "/" in clean:
                    # Has path - use the full path as pattern
                    extracted_patterns.append(clean)
                else:
                    # Just domain - add to domains if not there
                    if clean and clean not in domains:
                        domains.append(clean)

        # Create tool entry
        tool_entry = {
            "name": name,
            "domains": domains,
            "patterns": extracted_patterns[:5] if extracted_patterns else [],  # Limit patterns
            "competitor_priority": "low",  # Default for Ghostery patterns
            "source": "ghostery"
        }

        ghostery_patterns[our_category].append(tool_entry)
        existing_names.add(name.lower())

    # Log stats
    total = sum(len(v) for v in ghostery_patterns.values())
    logger.info(f"Loaded {total} additional patterns from Ghostery TrackerDB")
    for cat, tools in ghostery_patterns.items():
        if tools:
            logger.debug(f"  {cat}: {len(tools)} patterns")

    return ghostery_patterns


def get_all_patterns() -> dict[str, list[dict]]:
    """
    Get all tech patterns including Ghostery enhancements.
    Returns combined TECH_PATTERNS + Ghostery patterns.
    """
    all_patterns = dict(TECH_PATTERNS)

    # Add Ghostery patterns
    ghostery = _load_ghostery_patterns()
    for category, tools in ghostery.items():
        if category in all_patterns:
            all_patterns[category].extend(tools)
        else:
            all_patterns[category] = tools

    return all_patterns


# Initialize extended categories metadata for Ghostery categories
TECH_CATEGORIES["ghostery_analytics"] = {
    "display_name": "Analytics (Extended)",
    "insider_relevance": "low",
    "template_field": "Analytics"
}
TECH_CATEGORIES["ghostery_advertising"] = {
    "display_name": "Advertising (Extended)",
    "insider_relevance": "low",
    "template_field": "Others"
}
TECH_CATEGORIES["ghostery_customer_interaction"] = {
    "display_name": "Customer Interaction (Extended)",
    "insider_relevance": "medium",
    "template_field": "Others"
}
TECH_CATEGORIES["ghostery_consent"] = {
    "display_name": "Consent Management (Extended)",
    "insider_relevance": "low",
    "template_field": "Others"
}
TECH_CATEGORIES["ghostery_social_media"] = {
    "display_name": "Social Media (Extended)",
    "insider_relevance": "low",
    "template_field": "Others"
}
