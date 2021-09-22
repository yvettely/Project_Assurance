### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta

### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }

def validate_data(member_ID, intent_request):
    """
    Validates the data provided by the user.
    """

        # Validate the donation amount, it should be => 10000
    #if donation_amount is not None:
        #donation_amount = int(
            #donation_amount
        #)  # Since parameters are strings it's important to cast values
        #if donation_amount < 10000:
            #return build_validation_result(
                #False,
                #"donationAmount",
                #"The donation amount to should be equal to or greater than $10,000, "
                #"please provide a new donation amount.",
            #)

    # A True results is returned if age or amount are valid
    return build_validation_result(True, None, None)

### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    print(intent_request)
    return intent_request["currentIntent"]["slots"]
    


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response


### Intents Handlers ###
def donation_proceeds(intent_request):
    """
    Performs dialog management and fulfillment for showing donation proceeds.
    """

    member_ID = get_slots(intent_request)["MemberID"]
    charity_name = get_slots(intent_request)["charityName"]
    donationTier = get_slots(intent_request)["donationTier"]
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt
        # for the first violation detected.

        # Gets all the slots
        slots = get_slots(intent_request)

        # Validates user's input using the validate_data function
        validation_result = validate_data(donationTier, intent_request)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )
        # Fetch current session attibutes
        output_session_attributes = intent_request["sessionAttributes"]

        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the initial investment recommendation

    def initial_recommendation(donationTier):
        
        if donationTier == "First Tier":
            return("between $10,000 - $25, 000 to provide local animal boarding to prevent animals from being euthanized.")
            
        if donationTier == "Second Tier":
            return("between $25,001 - $50,000 to pay for major surgeries for injured animals.")
            
        if donationTier == "Third Tier":
            return("between $50,001 - $100,000 to charter a plane to rescue pets from disaster areas.")
            
        
    # Return a message with the initial recommendation based on the donation tier.
    
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """{} , based on your selection, we will need {}
            """.format(
                member_ID, initial_recommendation(donationTier)
            ),
        },
    )

### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "CharitableDonations":
        return donation_proceeds(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)