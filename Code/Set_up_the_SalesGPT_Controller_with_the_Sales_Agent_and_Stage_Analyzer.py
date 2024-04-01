from Import_Libraries_and_Set_Up_Your_Environment import *
from Sales_conversation_stages import conversation_stage_dict, StageAnalyzerChain, SalesConversationChain
from Setup_agent_tools import get_tools

# from Import_Libraries_and_Set_Up_Your_Environment import *
# from Sales_conversation_stages import *
# from Knowledge_Base import *
# from Setup_agent_tools import *




# Define a Custom Prompt Template

class CustomPromptTemplateForTools(StringPromptTemplate):
    # The template to use
    template: str
    ############## NEW ######################
    # The list of tools available
    tools_getter: Callable

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        ############## NEW ######################
        tools = self.tools_getter(kwargs["input"])
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in tools]
        )
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in tools])
        return self.template.format(**kwargs)




# Define a custom Output Parser

class SalesConvoOutputParser(AgentOutputParser):
    ai_prefix: str = "AI"  # change for salesperson_name
    verbose: bool = False

    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        if self.verbose:
            print("TEXT")
            print(text)
            print("-------")
        regex = r"Action: (.*?)[\n]*Action Input: (.*)"
        match = re.search(regex, text)
        if not match:
            return AgentFinish(
                {"output": text.split(f"{self.ai_prefix}:")[-1].strip()}, text
            )
            # raise OutputParserException(f"Could not parse LLM output: `{text}`")
        action = match.group(1)
        action_input = match.group(2)
        return AgentAction(action.strip(), action_input.strip(" ").strip('"'), text)

    @property
    def _type(self) -> str:
        return "sales-agent"
    


SALES_AGENT_TOOLS_PROMPT = """
Never forget your name is {salesperson_name}. You work as a {salesperson_role}.
You work at company named {company_name}. {company_name}'s business is the following: {company_business}.
Company values are the following. {company_values}
You are contacting a potential prospect in order to {conversation_purpose}
Your means of contacting the prospect is {conversation_type}

If you're asked about where you got the user's contact information, say that you got it from public records.
Keep your responses in short length to retain the user's attention. Never produce lists, just answers.
Start the conversation by just a greeting and how is the prospect doing without pitching in your first turn.
When the conversation is over, output <END_OF_CALL>
Always think about at which conversation stage you are at before answering:

1: Introduction: Start the conversation by introducing yourself and your company. Be polite and respectful while keeping the tone of the conversation professional. Your greeting should be welcoming. Always clarify in your greeting the reason why you are calling.
2: Qualification: Qualify the prospect by confirming if they are the right person to talk to regarding your product/service. Ensure that they have the authority to make purchasing decisions.
3: Value proposition: Briefly explain how your product/service can benefit the prospect. Focus on the unique selling points and value proposition of your product/service that sets it apart from competitors.
4: Needs analysis: Ask open-ended questions to uncover the prospect's needs and pain points. Listen carefully to their responses and take notes.
5: Solution presentation: Based on the prospect's needs, present your product/service as the solution that can address their pain points.
6: Objection handling: Address any objections that the prospect may have regarding your product/service. Be prepared to provide evidence or testimonials to support your claims.
7: Close: Ask for the sale by proposing a next step. This could be a demo, a trial or a meeting with decision-makers. Ensure to summarize what has been discussed and reiterate the benefits.
8: End conversation: The prospect has to leave to call, the prospect is not interested, or next steps where already determined by the sales agent.

TOOLS:
------

{salesperson_name} has access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of {tools}
Action Input: the input to the action, always a simple string input
Observation: the result of the action
```

If the result of the action is "I don't know." or "Sorry I don't know", then you have to say that to the user as described in the next sentence.
When you have a response to say to the Human, or if you do not need to use a tool, or if tool did not help, you MUST use the format:

```
Thought: Do I need to use a tool? No
{salesperson_name}: [your response here, if previously used a tool, rephrase latest observation, if unable to find the answer, say it]
```

You must respond according to the previous conversation history and the stage of the conversation you are at.
Only generate one response at a time and act as {salesperson_name} only!

Begin!

Previous conversation history:
{conversation_history}

Thought:
{agent_scratchpad}
"""



class SalesGPT(Chain):
    """Controller model for the Sales Agent."""

    conversation_history: List[str] = []
    current_conversation_stage: str = '1'
    stage_analyzer_chain: StageAnalyzerChain = Field(...)
    sales_conversation_utterance_chain: SalesConversationChain = Field(...)

    sales_agent_executor: Union[AgentExecutor, None] = Field(...)
    use_tools: bool = False


    # conversation_stage_dict: Dict = {
    #     '1' : "Introduction: Start the conversation by introducing yourself and your company. Be polite and respectful while keeping the tone of the conversation professional. Your greeting should be welcoming. Always clarify in your greeting the reason why you are contacting the prospect.",
    #     '2': "Qualification: Qualify the prospect by confirming if they are the right person to talk to regarding your product/service. Ensure that they have the authority to make purchasing decisions.",
    #     '3': "Value proposition: Briefly explain how your product/service can benefit the prospect. Focus on the unique selling points and value proposition of your product/service that sets it apart from competitors.",
    #     '4': "Needs analysis: Ask open-ended questions to uncover the prospect's needs and pain points. Listen carefully to their responses and take notes.",
    #     '5': "Solution presentation: Based on the prospect's needs, present your product/service as the solution that can address their pain points.",
    #     '6': "Objection handling: Address any objections that the prospect may have regarding your product/service. Be prepared to provide evidence or testimonials to support your claims.",
    #     '7': "Close: Ask for the sale by proposing a next step. This could be a demo, a trial or a meeting with decision-makers. Ensure to summarize what has been discussed and reiterate the benefits."
    #     }

    conversation_stage_dict: Dict = conversation_stage_dict

    salesperson_name: str = "Devel"
    salesperson_role: str = "Business Development Representative"
    company_name: str = "Room Retreat"
    company_business: str = "Room Retreat specializes in providing premium accommodations for travelers seeking comfort and luxury during their stays. We offer a variety of rooms and amenities tailored to meet the unique needs of our guests, ensuring a memorable and enjoyable experience."
    company_values: str = "At Room Retreat, we are dedicated to providing exceptional hospitality and personalized service to every guest. Our mission is to create a home away from home for travelers, offering comfort, convenience, and relaxation in every stay."
    conversation_purpose: str = "help travelers find the perfect accommodations for their upcoming trips."
    conversation_type: str = "chat"

    def retrieve_conversation_stage(self, key):
        return self.conversation_stage_dict.get(key, '1')
    
    @property
    def input_keys(self) -> List[str]:
        return []

    @property
    def output_keys(self) -> List[str]:
        return []

    def seed_agent(self):
        # Step 1: seed the conversation
        self.current_conversation_stage= self.retrieve_conversation_stage('1')
        self.conversation_history = []

    def determine_conversation_stage(self):
        conversation_stage_id = self.stage_analyzer_chain.run(
        # conversation_stage_id = self.stage_analyzer_chain.invoke(
            conversation_history='"\n"'.join(self.conversation_history), 
            current_conversation_stage=self.current_conversation_stage,        )

        self.current_conversation_stage = self.retrieve_conversation_stage(
            conversation_stage_id
        )
  
        print(f"\n<Conversation Stage>: {self.current_conversation_stage}\n")
        
    def human_step(self, human_input):
        # process human input
        human_input = human_input + '<END_OF_TURN>'
        self.conversation_history.append(human_input)

    def step(self):
        self._call(inputs={})

    def _call(self, inputs: Dict[str, Any]) -> None:
        """Run one step of the sales agent."""

        # Generate agent's utterance
        if self.use_tools:
            # ai_message = self.sales_conversation_utterance_chain.run(
            ai_message = self.sales_agent_executor.run(
            # ai_message = self.sales_agent_executor.invoke(
                input="",
                salesperson_name = self.salesperson_name,
                salesperson_role= self.salesperson_role,
                company_name=self.company_name,
                company_business=self.company_business,
                company_values = self.company_values,
                conversation_purpose = self.conversation_purpose,
                conversation_history="\n".join(self.conversation_history),
                conversation_stage = self.current_conversation_stage,
                conversation_type=self.conversation_type
            )
        else:
            ai_message = self.sales_conversation_utterance_chain.run(
            # ai_message = self.sales_conversation_utterance_chain.invoke(
                salesperson_name = self.salesperson_name,
                salesperson_role= self.salesperson_role,
                company_name=self.company_name,
                company_business=self.company_business,
                company_values = self.company_values,
                conversation_purpose = self.conversation_purpose,
                conversation_history="\n".join(self.conversation_history),
                conversation_stage = self.current_conversation_stage,
                conversation_type=self.conversation_type
            )
        
        
        # Add agent's response to conversation history
        print(f'\n{self.salesperson_name}: ', ai_message.rstrip('<END_OF_TURN>'))

        agent_name = self.salesperson_name
        ai_message = agent_name + ": " + ai_message
        if "<END_OF_TURN>" not in ai_message:
            ai_message += " <END_OF_TURN>"
        
        self.conversation_history.append(ai_message)
        return {}

    @classmethod
    def from_llm(
        cls, llm: BaseLLM, verbose: bool = False, **kwargs
    ) -> "SalesGPT":
        """Initialize the SalesGPT Controller."""
        stage_analyzer_chain = StageAnalyzerChain.from_llm(llm, verbose=verbose)
        sales_conversation_utterance_chain = SalesConversationChain.from_llm(
            llm, verbose=verbose
        )


        if "use_tools" in kwargs.keys() and kwargs["use_tools"] is False:
            sales_agent_executor = None

        else:
            # product_catalog = kwargs["product_catalog"]
            tools = get_tools()

            prompt = CustomPromptTemplateForTools(
                template=SALES_AGENT_TOOLS_PROMPT,
                tools_getter=lambda x: tools,
                # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
                # This includes the `intermediate_steps` variable because that is needed
                input_variables=[
                    "input",
                    "intermediate_steps",
                    "salesperson_name",
                    "salesperson_role",
                    "company_name",
                    "company_business",
                    "company_values",
                    "conversation_purpose",
                    "conversation_type",
                    "conversation_history",
                ],
            )
            llm_chain = LLMChain(llm=llm, prompt=prompt, verbose=verbose)

            tool_names = [tool.name for tool in tools]

            # WARNING: this output parser is NOT reliable yet
            ## It makes assumptions about output from LLM which can break and throw an error
            output_parser = SalesConvoOutputParser(
                ai_prefix=kwargs["salesperson_name"], verbose=verbose
            )

            sales_agent_with_tools = LLMSingleActionAgent(
                llm_chain=llm_chain,
                output_parser=output_parser,
                stop=["\nObservation:"],
                allowed_tools=tool_names,
                verbose=verbose,
            )

            sales_agent_executor = AgentExecutor.from_agent_and_tools(
                agent=sales_agent_with_tools, tools=tools, verbose=verbose
            )


        return cls(
            stage_analyzer_chain=stage_analyzer_chain,
            sales_conversation_utterance_chain=sales_conversation_utterance_chain,
            sales_agent_executor=sales_agent_executor,
            verbose=verbose,
            **kwargs,
        )