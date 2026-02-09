import streamlit as st
from modules import image_generator, document_generator

# Page Configuration
st.set_page_config(
    page_title="AI Grant Architect",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MASTER AI PERSONA SYSTEM PROMPT ---
SYSTEM_PROMPT = """
# 🧠 MASTER AI PERSONA: The High-Stakes Business Plan & Grant Architect

**Role:** You are a world-class Professional Business Proposal & Grant Plan Consultant. You have previously served as the Chairman of a grant-giving organization, giving you "insider" knowledge of what funders require. You have helped clients secure over $750M in funding.

**The Objective:**
Your goal is to guide the user through a consultation to produce a **comprehensive, award-winning Business Plan** that strictly follows the provided "Business Plan Template" structure.

**CRITICAL CONSTRAINTS:**
1.  **Volume:** The final Business Plan must be a **MINIMUM of 60 pages**. There is no upper limit. If the user provides extensive details, the plan should expand accordingly to 80, 100, or more pages. You must elaborate, expound, and provide deep market analysis to ensure this volume is met.
2.  **Format:** The final output MUST be provided as a **downloadable .docx file**. You will use your Code Interpreter / Data Analysis tool to write the content into a Word document.
3.  **Sequencing:** You must complete the Business Plan **first**. Only after the user has downloaded, reviewed, and approved the .docx file will you proceed to the Pitch Deck phase.

---

### 📚 THE MANDATED BUSINESS PLAN STRUCTURE
You must ensure the final output covers every single section below. To meet the 60+ page requirement, you must generate extensive content for each:

1.  **Cover Page:** Business Name, Contact Info, Logo placeholder, Brand Slogan.
2.  **Executive Summary:** A snapshot of the core essence, business goals, investment proposition (Funding Amount), and impact/returns.
3.  **Introduction:** Overview, Stage of Business (Idea/Market Entry/Growth), and Progress to date.
4.  **Company Description:** History, Legal Structure, Location/Facilities, Vision (inspiring & timed), Mission, and SMART Objectives.
5.  **The Product & Service:** Product Line, R&D plans, Production Process, Value Proposition, and IP/Trademarks.
6.  **Market Research:** Industry Background (Trends/Players), Market Analysis (Size/Growth), Target Market/Segmentation, Competitive Analysis (SWOT/PESTLE), and Regulatory Environment. *Note: This section requires significant expansion with simulated or real data to add bulk and value.*
7.  **Organization and Management:** Org Structure (Organogram), Management Team & Skills, HR Plan (Hiring/Training).
8.  **Marketing and Sales Strategy:** Marketing Plan, Sales Strategy/Tactics, Pricing Strategy, Advertising/Promotion, Customer Service, Unit Economics (CAC/LTV).
9.  **Operational Plan:** Key Processes, Location/Tech requirements, Supply Chain, Quality Control, Risk Management, Scalability.
10. **Funding Request:** Requirements, Future Needs, Founder’s Equity, Use of Funds (Budget), Expected Outcomes (Impact), Exit/Sustainability Strategy.
11. **Financial Projections:** 3-5 Year Revenue Forecast, Expense Forecast, P&L Statement, Cash Flow, Balance Sheet, Break-even Analysis.
12. **Implementation Plan:** Key Actions (3/6/12 months), Execution Monitoring, KPIs/Milestones.
13. **Appendix:** Resumes, Permits/Licenses, Legal Docs, Product Photos, References.

---

### ⚙️ OPERATIONAL PROTOCOL (The Consultation Process)

You will conduct this consultation in **Phases**.
* **Interaction Rule:** Ask **ONE** question at a time. Wait for the user's answer. Do not overwhelm the user.
* **Tone:** Professional, empathetic, visionary, and thorough.

#### 🗓️ PHASE 1: The Deep-Dive Discovery (Meetings 1-3)
* **Meeting 1 (Foundation):** Establish the Business Name, Legal Structure, Vision, Mission, and **Specific Grant/Funding Details** (Amount, Organization, Purpose).
* **Meeting 2 (Strategy & Operations):** Deep dive into the "Market Research," "Operational Plan," and "Marketing Strategy." *Ask probing questions to gather enough detail to write 10-15 pages for this section alone.*
* **Meeting 3 (Financials & Logic):** Solidify the Budget (based on the Funding Amount), Revenue Projections, and Implementation Timeline.

#### 🗓️ PHASE 2: The Business Plan Generation (Min 60 Pages)
* Once the meetings are done, you will compile the content.
* You will use **Python/Code Interpreter** to generate a **.docx file** containing the full plan.
* **Formatting:** Use professional headers, clear tables for financials, and standard business formatting.
* **Check:** Ask the user to download and review. If they need changes, revise the .docx file.

#### 🗓️ PHASE 3: The Pitch Deck (Post-Approval)
* **Start Condition:** ONLY begin this phase after the user says the Business Plan .docx is approved.
* **Process:** Initiate a new mini-discovery for the deck. Ask about:
    1.  Visual Style (Corporate, Creative, Minimalist).
    2.  Key focus areas for the presentation (Team vs. Product vs. Financials).
* **Generation:** Generate the Pitch Deck content (Slide by Slide) and offer it as a **downloadable .pptx file** (using Python) or a PDF.
"""

# Session State Initialization
if 'plan_generated' not in st.session_state:
    st.session_state['plan_generated'] = False
if 'generated_plan_text' not in st.session_state:
    st.session_state['generated_plan_text'] = ""
if 'generated_images' not in st.session_state:
    st.session_state['generated_images'] = {}
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "assistant", "content": "Hello. I am your Professional Consultant. I acknowledge the strict 60-page minimum requirement. Let's begin Meeting 1. What is the proposed Business Name and the specific nature of your business?"}
    ]

def main():
    st.title("AI Grant Architect")
    st.subheader("Your AI-Powered Business Plan & Grant Consultant")
    
    # --- API Key Management ---
    api_key = None
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        # Fallback for when running locally without secrets.toml or if specific key is desired
        with st.sidebar:
            st.warning("⚠️ No API Key found in secrets.")
            api_key = st.text_input("Enter Google API Key:", type="password")
            if not api_key:
                st.info("Please enter your Google API Key to proceed.")
                st.stop()

    # Sidebar: Navigation & Design Studio
    with st.sidebar:
        st.header("Navigation")
        # Placeholder for future navigation (Discovery, Strategy, Financials)
        step = st.radio("Go to:", ["Consultation", "Review Plan", "Export"], index=0)

        # Design Studio - Only appears if plan is generated (or for testing purposes, we can toggle it)
        # Check requirement: "This should only appear after the Business Plan text is fully generated."
        if st.session_state['plan_generated']:
            st.markdown("---")
            st.header("🎨 Design Studio")
            st.markdown("Customize your document aesthetics.")

            # Color Theme Selector
            theme_color = st.selectbox(
                "Color Theme",
                ["Corporate Blue", "Eco Green", "Modern Minimalist (Black/White)", "Vibrant Startup"],
                key="theme_color"
            )

            # Font Style Selector
            font_style = st.selectbox(
                "Font Style",
                ["Serif (Classic)", "Sans-Serif (Modern)", "Slab (Bold)"],
                key="font_style"
            )

            # Visual Style Selector (AI Image Style)
            visual_style = st.selectbox(
                "Visual Style",
                ["Photorealistic", "3D Rendered Isometric", "Abstract Line Art"],
                key="visual_style"
            )

            # 3D Asset Toggle
            use_3d_assets = st.checkbox(
                "Generate 3D-style charts and icons",
                value=False,
                key="use_3d_assets"
            )
        else:
            st.info("Complete the consultation phase to unlock the Design Studio.")

    # Main Content Area
    if step == "Consultation":
        st.write("## 1. Consultation Phase")
        st.write("Chat with the AI to build your plan.")

        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("Describe your business idea..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                if api_key:
                    try:
                        import google.generativeai as genai
                        genai.configure(api_key=api_key)
                        # Use gemini-1.5-flash-latest or gemini-pro to avoid 404 errors
                        # Passing system_instruction here (supported in newer library versions)
                        model = genai.GenerativeModel('gemini-1.5-flash-latest', system_instruction=SYSTEM_PROMPT)
                        
                        # Prepare context for the model
                        # We limit history to avoid token limits in this simple implementation
                        chat_history = []
                        for msg in st.session_state.messages[-10:]: # Last 10 messages
                            role = "user" if msg["role"] == "user" else "model"
                            chat_history.append({"role": role, "parts": [msg["content"]]})
                        
                        # Generate response
                        response = model.generate_content(chat_history, stream=True)
                        
                        for chunk in response:
                            if chunk.text:
                                full_response += chunk.text
                                message_placeholder.markdown(full_response + "▌")
                        
                        message_placeholder.markdown(full_response)
                        
                        # Check if the plan is ready (heuristic)
                        if "BUSINESS PLAN GENERATED" in full_response:
                             st.session_state['plan_generated'] = True
                             # Extract plan text logic could go here
                             st.session_state['generated_plan_text'] = full_response # Simplified for now

                    except Exception as e:
                        full_response = f"I encountered an error: {str(e)}"
                        message_placeholder.error(full_response)
                else:
                    full_response = "Please provide an API Key to chat."
                    message_placeholder.warning(full_response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Temporary button to simulate plan generation for testing the UI
        if st.button("Simulate Plan Generation (Dev Only)"):
            st.session_state['plan_generated'] = True
            st.session_state['generated_plan_text'] = """
# Execution Summary
This is the executive summary of the business plan.

## Mission Statement
To revolutionize the grant writing process.

# The Cover Page
(This section implies a cover page image)

# Financial Highlights
Our financial projections are robust.

# Operational Plan
We plan to operate globally.
"""
            st.rerun()

    elif step == "Review Plan":
        st.write("## 2. Review Your Plan")
        if st.session_state['plan_generated']:
            st.success("Plan Generated Successfully!")
            st.text_area("Draft Plan", value=st.session_state['generated_plan_text'], height=300)
            
            # Button to trigger image generation from Design Studio settings
            st.markdown("### 🖼️ Visual Assets")
            if st.button("Generate Visual Assets"):
                # Use current visual style from session state (via key='visual_style')
                current_style = st.session_state.get("visual_style", "Photorealistic")
                
                # Progress bar
                progress_bar = st.progress(0, text="Starting visual generation...")
                
                # Callback to update progress bar
                def update_progress(p, text):
                    progress_bar.progress(p, text=text)
                
                # Call the background function
                with st.spinner("AI is analyzing your plan and creating images..."):
                    images = image_generator.analyze_and_generate_visuals(
                        st.session_state['generated_plan_text'],
                        current_style,
                        api_key=api_key,
                        progress_callback=update_progress
                    )
                
                # Save to session state
                st.session_state['generated_images'] = images
                st.success(f"Generated {len(images)} images!")
            
            # Display generated images if they exist - GALLERY PREVIEW
            if st.session_state['generated_images']:
                st.markdown("### 🖼️ Asset Gallery Preview")
                st.info("Review your generated assets before exporting.")
                
                # Create a grid layout for images
                images_list = list(st.session_state['generated_images'].items())
                
                # Display in rows of 3
                for i in range(0, len(images_list), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i + j < len(images_list):
                            section_name, img_obj = images_list[i+j]
                            with cols[j]:
                                st.image(img_obj, caption=section_name, use_container_width=True)

        else:
            st.warning("No plan generated yet. Go to Consultation.")

    elif step == "Export":
        st.write("## 3. Export Documents")
        if st.session_state['plan_generated']:
            st.write("Ready to export.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Business Plan (.docx)")
                if st.button("Compile & Download Business Plan"):
                    # Gather inputs
                    business_name = "My Startup" # Placeholder or from session state if available
                    slogan = "Innovating the Future" 
                    
                    with st.spinner("Compiling document..."):
                        docx_file = document_generator.generate_docx(
                            business_name=business_name,
                            slogan=slogan,
                            plan_text=st.session_state['generated_plan_text'],
                            theme_color=st.session_state.get('theme_color', 'Corporate Blue'),
                            generated_images=st.session_state.get('generated_images', {}),
                            use_3d_assets=st.session_state.get('use_3d_assets', False)
                        )
                        
                    st.download_button(
                        label="Download .docx",
                        data=docx_file,
                        file_name="Business_Plan.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

            with col2:
                st.subheader("Pitch Deck (.pptx)")
                st.button("Download .pptx", disabled=True, help="Coming in Phase 5")

        else:
            st.warning("Generate a plan first.")

if __name__ == "__main__":
    main()
