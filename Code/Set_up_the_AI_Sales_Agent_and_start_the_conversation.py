from Import_Libraries_and_Set_Up_Your_Environment import *
from Set_up_the_SalesGPT_Controller_with_the_Sales_Agent_and_Stage_Analyzer import SalesGPT
from Sales_conversation_stages import llm

# from Import_Libraries_and_Set_Up_Your_Environment import *
# from Sales_conversation_stages import *
# from Knowledge_Base import *
# from Setup_agent_tools import *
# from Set_up_the_SalesGPT_Controller_with_the_Sales_Agent_and_Stage_Analyzer import *






# Set up of your agent

# Conversation stages - can be modified
conversation_stages = {
# '1' : "Introduction: Start the conversation by introducing yourself and your company. Be polite and respectful while keeping the tone of the conversation professional. Your greeting should be welcoming. Always clarify in your greeting the reason why you are contacting the prospect.",
# '2': "Qualification: Qualify the prospect by confirming if they are the right person to talk to regarding your product/service. Ensure that they have the authority to make purchasing decisions.",
# '3': "Value proposition: Briefly explain how your product/service can benefit the prospect. Focus on the unique selling points and value proposition of your product/service that sets it apart from competitors.",
# '4': "Needs analysis: Ask open-ended questions to uncover the prospect's needs and pain points. Listen carefully to their responses and take notes.",
# '5': "Solution presentation: Based on the prospect's needs, present your product/service as the solution that can address their pain points.",
# '6': "Objection handling: Address any objections that the prospect may have regarding your product/service. Be prepared to provide evidence or testimonials to support your claims.",
# '7': "Close: Ask for the sale by proposing a next step. This could be a demo, a trial or a meeting with decision-makers. Ensure to summarize what has been discussed and reiterate the benefits."
    
    '1': "Introduction: Start the conversation by introducing yourself and your company. Be polite and respectful while keeping the tone of the conversation professional. Your greeting should be welcoming. Always clarify in your greeting the reason why you are contacting the prospect.",
    '2': "Travel Details: Gather information about the customer's travel plans, such as desired location, travel dates, and budget.",
    '3': "Room Preferences: Understand the customer's room preferences, such as room type, amenities, and any special requests.",
    '4': "Hotel Search: Present hotel options that match the customer's preferences and requirements.",
    '5': "Hotel Information: Provide detailed information about the selected hotel, including room details, facilities, nearby amenities, and any additional relevant information.",
    '6': "Objection Handling: Address any objections or concerns the customer may have regarding the hotel or booking process.",
    '7': "Close: Assist the customer in completing the booking process and closing the sale."

}

# Agent characteristics - can be modified
config = dict(
    # salesperson_name = "Julia Goldsmith",
    # salesperson_role = "Sales Executive",
    # company_name = "Golden Pens",
    # company_business = "Golden Pens is a premium pen company that offers a range of high-quality, gold-plated pens. Our pens are designed to be stylish, functional, and long-lasting, making them perfect for professionals who want to make a lasting impression.",
    # company_values = "At Golden Pens, we believe that the right pen can make all the difference in the world. We are passionate about providing our customers with the best possible writing experience, and we are committed to excellence in everything we do.",
    # conversation_purpose = "find out if the customer is interested in purchasing a premium gold-plated pen.",
    # conversation_history = [],
    # conversation_type = "chat",
    # conversation_stage = conversation_stages.get('1', "Introduction: Start the conversation by introducing yourself and your company. Be polite and respectful while keeping the tone of the conversation professional.")

    salesperson_name="Devel",
    salesperson_role="Business Development Representative",
    company_name="Room Retreat",
    company_business="Room Retreat specializes in providing premium accommodations for travelers seeking comfort and luxury during their stays. We offer a variety of rooms and amenities tailored to meet the unique needs of our guests, ensuring a memorable and enjoyable experience.",
    company_values="At Room Retreat, we are dedicated to providing exceptional hospitality and personalized service to every guest. Our mission is to create a home away from home for travelers, offering comfort, convenience, and relaxation in every stay.",
    conversation_purpose="help travelers find the perfect accommodations for their upcoming trips.",
    conversation_history=[],
    conversation_type="chat",
    conversation_stage=conversation_stages.get(
        '1', "Introduction: Start the conversation by introducing yourself and your company. Be polite and respectful while keeping the tone of the conversation professional."
    ),  
    use_tools=True,
    # product_catalog="sample_product_catalog.txt",
)





sales_agent = SalesGPT.from_llm(llm, verbose=False, **config)
# init sales agent
sales_agent.seed_agent()

while True:
    sales_agent.determine_conversation_stage()
    sleep(2)
    sales_agent.step()

    human = input("\nUser Input =>  ")
    if human:
        sales_agent.human_step(human)
        sleep(2)
        print("\n")