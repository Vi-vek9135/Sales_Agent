from Import_Libraries_and_Set_Up_Your_Environment import *
from Set_up_the_SalesGPT_Controller_with_the_Sales_Agent_and_Stage_Analyzer import *
from Sales_conversation_stages import llm

# Paste the contents of paste.txt here

# Define the FastAPI app
app = FastAPI(title="Upload documents using FastAPI")
pdfs_directory = "uploads"
os.makedirs(pdfs_directory, exist_ok=True)
print("Directory 'uploads' created successfully")
uploaded_files = []




# Conversation stages - can be modified
conversation_stages = {

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
    
)





# Endpoint for uploading text files
@app.post("/upload/")
async def upload_file(files: list[UploadFile] = File(...)):
    """
    This endpoint allows users to upload text files.
    Args:
        file (UploadFile): The uploaded file.
    Returns:
        dict: Message indicating the success or failure of the upload.
    """
    for file in files:
        file_path = os.path.join(pdfs_directory, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        uploaded_files.append(file_path)

    

    # sales_agent = SalesGPT.from_llm(llm, verbose=False, **config)
    # sales_agent.seed_agent()

    # while True:
    #     sales_agent.determine_conversation_stage()
    #     sleep(2)
    #     sales_agent.step()

    return {"message": "Files uploaded successfully"}








@app.post("/user_input/")
async def user_input(input_text: str):
    sales_agent = SalesGPT.from_llm(llm, verbose=False, **config)
    sales_agent.seed_agent()

    while True:
        sales_agent.determine_conversation_stage()
        sleep(2)
        sales_agent.step()
        sales_agent.human_step(input_text)
        response = sales_agent.get_response()
        return {"response": response}
















if __name__ == "__main__":
    # sales_agent = SalesGPT.from_llm(llm, verbose=False, **config)
    # sales_agent.seed_agent()

    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

    # while True:
    #     sales_agent.determine_conversation_stage()
    #     sleep(2)
    #     sales_agent.step()


    # sales_agent = SalesGPT.from_llm(llm, verbose=False, **config)
    # # init sales agent
    # sales_agent.seed_agent()

    # while True:
    #     sales_agent.determine_conversation_stage()
    #     sleep(2)
    #     sales_agent.step()

    #     human = input("\nUser Input =>  ")
    #     if human:
    #         sales_agent.human_step(human)
    #         sleep(2)
    #         print("\n")























