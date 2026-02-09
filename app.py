import streamlit as st
from modules import image_generator, document_generator

# Page Configuration
st.set_page_config(
    page_title="AI Grant Architect",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session State Initialization
if 'plan_generated' not in st.session_state:
    st.session_state['plan_generated'] = False
if 'generated_plan_text' not in st.session_state:
    st.session_state['generated_plan_text'] = ""
if 'generated_images' not in st.session_state:
    st.session_state['generated_images'] = {}

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
