from Import_Libraries_and_Set_Up_Your_Environment import *
from Knowledge_Base import setup_knowledge_base
# from main import process_and_create_knowledge_base



# from Import_Libraries_and_Set_Up_Your_Environment import *
# from Sales_conversation_stages import *
# from Knowledge_Base import *




def get_tools():
    # query to get_tools can be used to be embedded and relevant tools found
    # see here: https://langchain-langchain.vercel.app/docs/use_cases/agents/custom_agent_with_plugin_retrieval#tool-retriever

    # we only use one tool for now, but this is highly extensible!
    # knowledge_base = process_and_create_knowledge_base()
    knowledge_base = setup_knowledge_base
    tools = [
        Tool(
            name="RoomSearch",
            # func=knowledge_base.run,
            func=knowledge_base.invoke,
            description="useful for when you need to answer questions about product information or services offered, availability and their costs.",
        ),
        # Tool(
        #     name="GeneratePaymentLink",
        #     func=generate_stripe_payment_link,
        #     description="useful to close a transaction with a customer. You need to include product name and quantity and customer name in the query input.",
        # ),
    ]

    return tools